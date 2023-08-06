from jsonschema import Draft4Validator, RefResolver
from jsonschema.exceptions import ValidationError
from exceptions import ImportPublicationError, DoubleFoundException
from eulfedora.server import Repository
from eulfedora.api import API_A_LITE
from model import DialObject
from builder import PublicationRecordBuilder
from enrich import NO_ENRICH, EnrichDataEngine
from double import CheckDoubleEngine

import json
import os
import logging
import requests
import enrich

logger = logging.getLogger(__name__)


# ======================================================================================================================
#    IMPORT DATA INTO REPOSITORY
# ======================================================================================================================
class DataImporter:

    def __init__(self, schemas_directory=None, enrich_data=NO_ENRICH):
        if schemas_directory is None:
            schemas_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'schemas')
        self.schema_store = {}
        for fname in [fname for fname in os.listdir(schemas_directory) if fname.endswith('.json')]:
            with open(os.path.join(schemas_directory, fname), 'r') as fh:
                schema = json.load(fh)
                if '$id' in schema:
                    Draft4Validator.check_schema(schema)
                    self.schema_store[schema['$id']] = schema
        self.resolver = RefResolver('', '', self.schema_store)

        # load configurations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf', 'services.json')) as sh:
            self.services = json.load(sh)

        # create Fedora connection ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        credentials = {
            'username': self.services['fedora']['username'],
            'password': self.services['fedora']['password'],
        }
        api_a = API_A_LITE(self.services['fedora']['url'], **credentials)
        api_a.describeRepository()  # this operation generate an error if connection failed.
        del api_a
        self.repository = Repository(self.services['fedora']['url'], **credentials)

        # create actions engines ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.enrich_engine = EnrichDataEngine(favorite_data=enrich_data, services=self.services)
        self.double_engine = CheckDoubleEngine(services=self.services)

    def _found_specific_schema(self, document_type):
        return [v for k, v in self.schema_store.items() if self._schema_get_document_type(v) == document_type]

    def _schema_get_document_type(self, schema):
        if "properties" in schema:
            if "type" in schema['properties']\
               and "properties" in schema['properties']['type']\
               and "document_type" in schema['properties']['type']['properties']:
                doc_type = schema['properties']['type']['properties']['document_type']
                if 'enum' in doc_type:
                    return next(iter(doc_type['enum']), None)
        elif "allOf" in schema:
            for sub_schema in schema['allOf']:
                doc_type = self._schema_get_document_type(sub_schema)
                if doc_type is not None:
                    return doc_type

    def validate_data(self, json_data):
        """
           This method will validate the json data according the the document type.

           This method need to use a different jsonschema according of the main document type into the json_data.
           As each dial document jsonschema inherit from 'basics-publications' schema, we can first validate the
           json_data according to this schema. If validation of this schema is successfully, we know that the key
           `json_data['type']['document_type']` exists (it's a required property). So we can use this value to determine
           the right jsonschema according to the found main document type.

           :param json_data: Data to validate. Should represent a dial publication according to jsonschemas
           :type json_data: dict

           :raise `jsonschema.exception.ValidationError: if some error occured during the data validation.
        """
        try:
            basic_schema = self.schema_store.get("http://dial.uclouvain.be/schemas/basics-publications.json")
            Draft4Validator(basic_schema, resolver=self.resolver).validate(json_data)
            matching_schemas = self._found_specific_schema(json_data['type']['document-type'])
            for schema in matching_schemas:
                Draft4Validator(schema, resolver=self.resolver).validate(json_data)
        except ValidationError as ve:
            # TODO : do something better when ValidationError is catched
            raise ve

    def _create_handle(self, data):
        """ This function will create the handle about a publication. Provided data must specify a pid.
            :param data : the publication data.
            :return the created handle as '2018(.[1-4])/xxxxxx'
            :rtype string
            :raise HTTPError if handle creation failed
            :raise AssertionError if missing configuration component
        """
        assert 'pid' in data, "The publication hasn't pid. To create the handle, PID is required"
        assert 'handle' in self.services, "Handle isn't set into services configuration"
        assert 'api' in self.services['handle'], "Handle API isn't set into services configuration"
        config = self.services['handle']

        # perform institutions define into data entities and keep only partners institutions.
        # Partners institutions are defined into the service config file.
        publication_institutions = set([entity['institution'] for entity in data['entities']])
        partners_institutions = list()
        for inst in config['partner_institutions']:
            partners_institutions.extend([i.upper for i in inst['name']])
        publication_institutions = filter(lambda i: i.upper() in partners_institutions, publication_institutions)

        # Check to find the best naming authority
        #   * If only one value remain, use the corresponding authority define into the service config file
        #   * otherwise (2 or more, or O!), use the default naming authority
        naming_authority = None
        if len(publication_institutions) == 1:
            institution = publication_institutions[0]
            for inst in config['partner_institutions']:
                if institution in [i.upper() for i in inst['name']]:
                    naming_authority = inst['authority']
                    break
        else:
            naming_authority = config['default_authority']
        logger.debug("   * Using naming authority [{0}]".format(naming_authority))

        # Now, create tha handle for this publication using the Handle API and return the created value
        params = {
            'naming_authority': naming_authority,
            'pid': data['pid'].replace("boreal:", '')
        }
        resp = requests.get(config['api'], params=params, timeout=10)
        resp.raise_for_status()
        return resp.text

    def import_data(self, data, create_handle=True):
        """ This function allow to ingest some JSON data into DIAL. To be ingested into DIAL:
               1. the data must be validate against a JSON schema
               2. Enrich data
               3. Check if double exists into DIAL based on data (data will be enriched by step 2)
               4. create the MARCXML record from data suing pymarc.builder.builder interface
               5. Create handle for this record
               6. ingest into DIAL (and return OK status from DIAL)
        """
        try:
            logger.info("DATA IMPORTER ====================================================")
            logger.info("  STEP 1 :: validate json data ........................")
            self.validate_data(data)
            logger.info("    --> Data validation success")

            logger.info("  STEP 2 :: enrich json data ..........................")
            logger.info("     enrich mode = [{0}]".format(enrich.get_level_name(self.enrich_engine.favorite_data)))
            data = self.enrich_engine.call(data)
            logger.info("    --> Enrich data done")

            logger.info("  STEP 3 :: check double ...............................")
            self.double_engine.proceed(data)
            logger.info("    --> No double candidate found")

            logger.info("  STEP 4 :: init fedora object .........................")
            fc_obj = self.repository.get_object(create=True, type=DialObject.get_type(data))
            fc_obj.state = 'A'  # object need to be active
            fc_obj.save()
            logger.info("    * object created into fedora repository :: {pid}".format(pid=fc_obj.pid))
            data['pid'] = fc_obj.pid
            builder = PublicationRecordBuilder.get_builder(data)
            record = builder.json2xml(data)
            logger.debug("   * MARC record created")

            logger.info("  STEP 5 :: Create handle ..............................")
            logger.info("    * handle creation :: {0}".format(str(create_handle)))
            if create_handle:
                try:
                    handle_value = self._create_handle(data)
                    if handle_value is not None:
                        handle_url = self.services['handle']['handle_base_url']+"/"+handle_value
                        record = PublicationRecordBuilder.add_handle(record, handle_url)
                except requests.exceptions.RequestException as re:
                    logger.warn("    !! Error occured during handle creation. Se detail below")
                    logger.warn(str(re))

            logger.info("  STEP 6 :: Ingest MARCXML .............................")
            fc_obj.marcxml.content = builder.record2xml(record)
            fc_obj.save()
            return fc_obj.pid
        except ImportPublicationError as ipe:
            logger.error("  !!! Validation error")
            logger.error(str(ipe))
            raise ipe


