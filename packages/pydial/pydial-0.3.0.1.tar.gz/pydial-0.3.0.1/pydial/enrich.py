import os
import json
import logging
import pycountry
import requests

from collections import defaultdict
from habanero import Crossref

logger = logging.getLogger(__name__)

USER_DATA = 0
EXTERNAL_DATA = 1
NO_ENRICH = 2

_enrich_mode = {
    USER_DATA: 'USER_DATA',
    EXTERNAL_DATA: 'EXTERNAL_DATA',
    NO_ENRICH: 'NO_ENRICH',
    'USER_DATA': USER_DATA,
    'EXTERNAL_DATA': EXTERNAL_DATA,
    'NO_ENRICH': NO_ENRICH
}


# ======================================================================================================================
#    ENRICH DATA USING EXTERNAL API
# ======================================================================================================================
def get_level_name(level):
    """ Return the textual representation of enrich level 'level'.
        If the level is one of the predefined levels (USER_DATA, EXTERNAL_DATA, NO_ENRICH) then you get the
        corresponding string. If level doesn't exists return 'UNDEFINED'
    """
    return _enrich_mode.get(level, "UNDEFINED")


class EnrichDataEngine(object):
    """ This class provide method to enrich data provided by user using some external source.
        Data provided by user are possibly not full ; or worst not correct ! If we can have better data ... it's better.

        To work, each API must inherit from this class and implement the static method `enrich_data`.

        User can determine which data must be preserved if a data are found in external source. Either the user data are
        preserved (with possible mistakes), either the external sources data replacing the user data (with overwrite
        problems). If multiple API are call, and both return different data for the same key, then the last called API
        data will be used.

        attributes :
          * favorite_data : which data should be preserve the data will be merged (NONE, EXTERNAL, USER)
          * servies : the configuration dictionary containing all necessary informations about external services

    """

    ENABLED = True
    DISABLED = False

    def __init__(self, favorite_data=USER_DATA, services=None):
        self.favorite_data = favorite_data
        self._handlers = [cls() for cls in EnrichDataHandler.__subclasses__()]
        if services is None:
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf', 'services.json')) as sh:
                services = json.load(sh)
        self.services = services

    def __str__(self):
        return "<{class_name} :: {count} handler{plural}>".format(
            class_name=self.__class__.__name__,
            count=len(self._handlers),
            plural='s' if len(self._handlers) > 1 else ''
        )

    def __repr__(self):
        output = "<{class_name}>".format(class_name=self.__class__.__name__)
        for hdl in self._handlers:
            output += "\n\t* ({status}) {handler} :: {description}".format(
                status='ENABLED' if hdl.status == self.ENABLED else 'DISABLED',
                handler=hdl.__class__.__name__,
                description=hdl.description
            )
        return output

    def add_handler(self, handler):
        self._handlers.append(handler)

    def call(self, data):
        for hdl in [hdl for hdl in self._handlers if hdl.status == self.ENABLED]:
            data = hdl.enrich_data(data, self.favorite_data, services=self.services)
        return data

    @staticmethod
    def merge_data(data1, data2):
        data_merged = data1.copy()  # start with x's keys and values
        for key, data in data2.items():
            if key not in data_merged:
                data_merged[key] = data
            else:
                if type(data_merged[key]) and type(data):
                    if isinstance(data, dict):
                        data_merged[key] = EnrichDataEngine.merge_data(data_merged[key], data)
                    else:
                        # key already present in origin datastream, we keep the original value
                        pass
        return data_merged


class EnrichDataHandler(object):
    description = "Abstract EnrichData handler"
    status = EnrichDataEngine.DISABLED


class CrossrefEnrichData(EnrichDataHandler):
    """ This class implement the EnrichData behavior for the Crossref API.
        If the publication has a doi (and this DOI is correct and registered into Crossref), we can found a lot of
        good information about the publication using the crossref API
    """

    description = "Use CrossRef API to complete data using DOI as key if exists"
    status = EnrichDataEngine.ENABLED

    @staticmethod
    def enrich_data(data, favorite_data=USER_DATA, **kwargs):
        logger.debug("ENRICH DATA USING CROSSREF API -----------------------")
        if 'doi' not in data:
            # If no doi are provided, we can't call Crossref to get publication informations.
            # So return data without any change
            logger.debug("  * No DOI specified for this publication :: skip it")
            return data
        logger.debug("  * Using DOI [{doi}]".format(doi=data['doi']))

        # Create the Crossref API endpoint. Search into kwargs if an Crossref api_key are provided, if yes, then use it
        # to create the Crossref endpoint
        api_key = None
        if 'services' in kwargs and 'crossref' in kwargs['services'] and 'api_key' in kwargs['services']['crossref']:
            api_key = kwargs['services']['crossref']['api_key']
        api = Crossref(api_key=api_key) if api_key is not None else Crossref()

        # Try to use the API to get informations about the publication. If no informations can be found, then
        # nothing can be enrich, so return original data without modification
        # If publication type isn't into the manageable publication types, skip it
        try:
            work = api.works(ids=[data['doi']])
            if work['status'] != 'ok':
                raise IOError("DOI doesn't found using the Crossref API")
            work = work['message']
            work = work[0] if isinstance(work, list) else work
        except Exception as e:
            logger.debug("  * Error search into Crossref :: {msg}".format(msg=e.message))
            return data
        if 'type' not in work:
            logger.debug("  * publication type doesn't exists:: skip it")
            return data
        if work['type'] not in ['journal-article', 'book-chapter', 'book', 'proceedings-article', 'monograph']:
            logger.debug("  * publication type isn't supported :: {type} :: skip it".format(type=work['type']))
            return data

        # perform the Crossref answer to get available informations ====================================================
        doi_data = defaultdict(lambda: defaultdict())
        # basic metadata -----------------------------------------------------------------------------------------------
        #   * title & subtitle
        #   * publisher
        #   * date
        #   * language
        #   * keywords
        #   * publication status = 'published' (if a DOI exists, the paper will be published if it's not yet)
        if 'title' in work and work['title']:
            infos = work['title'] if isinstance(work['title'], list) else [work['title']]
            doi_data['title-info']['title'] = ' '.join(infos)
        if 'abstract' in work and work['abstract']:
            doi_data['abstracts'] = [work['abstract']]
        if 'subtitle' in work and work['subtitle']:
            infos = work['subtitle'] if isinstance(work['subtitle'], list) else [work['subtitle']]
            infos = filter(None, infos)
            if infos:
                doi_data['title-info']['subtitle'] = ' '.join(infos)
        if 'publisher' in work or 'publisher_location':
            pub_data = dict()
            if 'publisher' in work:
                pub_data['name'] = work['publisher']
            if 'publisher-location' in work:
                pub_data['place'] = work['publisher-location']
            doi_data['publishers'] = [pub_data]
        date_infos = None
        if 'published-online' in work and 'date-parts' in work['published-online']:
            date_infos = work['published-online']['date-parts'][0]
        elif 'published-print' in work and 'date-parts' in work['published-print']:
            date_infos = work['published-print']['date-parts'][0]
        elif 'issued' in work and 'date-parts' in work['issued']:
            date_infos = work['issued']['date-parts'][0]
        if date_infos is not None and date_infos[0] is not None:
            doi_data['year'] = date_infos[0]
        if 'subject' in work:
            infos = work['subject'] if isinstance(work['subject'], list) else [work['subject']]
            doi_data['keywords'] = infos
        if 'language' in work:
            iso_2_code = work['language']
            lang = pycountry.languages.get(alpha_2=iso_2_code)
            doi_data['language'] = lang.alpha_3
        doi_data['publication-status'] = u'published'

        # specific metadata about book-chapter -------------------------------------------------------------------------
        #   * host document title
        #   * host document year
        #   * host document isbn
        #   * host document pagination
        if work['type'] in ['book-chapter', 'proceedings-article']:
            if 'container-title' in work:
                infos = ' : '.join(work['container-title'])
                doi_data['host-document']['title'] = infos
            if 'published-print' in work and 'date-parts' in work['published-print']:
                date = work['published-print']['date-parts'][0]
                doi_data['host-document']['year'] = date[0]
            if 'ISBN' in work:
                doi_data['host-document']['isbn'] = work['ISBN'][0]
            if 'page' in work:
                doi_data['host-document']['page'] = work['page']

        # --> specific metadata about journal-article ------------------------------------------------------------------
        #   * journal title
        #   * journal volume
        #   * journal issue
        #   * journal pagination
        #   * journal year
        if work['type'] in ['journal-article', 'proceedings-article']:
            if 'volume' in work:
                doi_data['journal-issue']['volume'] = work['volume']
            if 'issue' in work:
                doi_data['journal-issue']['issue'] = work['issue']
            if 'page' in work:
                doi_data['journal-issue']['page'] = work['page']
            if 'container-title' in work:
                doi_data['journal-issue']['title'] = ' : '.join(work['container-title'])
            if 'issued' in work and 'date-parts' in work['issued']:
                doi_data['journal-issue']['year'] = work['issued']['date-parts'][0][0]
            if 'issn-type' in work:
                if 'issn_type' not in doi_data['journal-issue']:
                    doi_data['journal-issue']['issn-type'] = list()
                for issn in work['issn-type']:
                    issn['type'] = 'eissn' if issn['type'] == 'electronic' else 'issn'
                    doi_data['journal-issue']['issn-type'].append(issn)

        # --> specific metadata about book -----------------------------------------------------------------------------
        #   * isbn
        #   * collection name
        #   * collection number and collection ISSN (not available in Crossref API)
        if work['type'] in ['book', 'monograph']:
            if 'ISBN' in work:
                doi_data['isbn'] = work['ISBN']
            if 'container-title' in work:
                doi_data['series'] = [{'name': ' '.join(work['container-title'])}]

        # --> specific metadata about speech ---------------------------------------------------------------------------
        #   * event name
        #   * event location
        #   * event start/end date
        if work['type'] == 'proceedings-article':
            if 'event' in work:
                if 'name' in work['event']:
                    doi_data['event']['name'] = work['event']['name']
                if 'location' in work['event']:
                    doi_data['event']['place'] = work['event']['location']
                if 'start' in work['event'] and 'date-parts' in work['event']['start']:
                    date_infos = work['event']['start']['date-parts'][0]
                    doi_data['event']['start'] = '/'.join(reversed(['{:02d}'.format(x) for x in date_infos]))
                if 'end' in work['event'] and 'date-parts' in work['event']['end']:
                    date_infos = work['event']['end']['date-parts'][0]
                    doi_data['event']['end'] = '/'.join(reversed(['{:02d}'.format(x) for x in date_infos]))
            if 'ISBN' in work:
                del (doi_data['journal-issue'])
            if 'ISSN' in work:
                del (doi_data['host-document'])
        logger.debug("  * found data :: "+str(doi_data))

        # At the end, always return merge_data.
        # To merge dict and default_dict, I used the method to transform DATA --> JSON --> DATA
        if favorite_data == USER_DATA:
            merged_data = EnrichDataEngine.merge_data(data, dict(doi_data))
        else:
            merged_data = EnrichDataEngine.merge_data(dict(doi_data), data)
        merged_data = json.dumps(merged_data)

        return json.loads(merged_data)


class KermitEnrichData(EnrichDataHandler):

    description = "Use Kermit API to complete data. Use ISSN (all types) if exists. Title otherwise iif exists"
    status = EnrichDataEngine.ENABLED

    @staticmethod
    def enrich_data(data, favorite_data=USER_DATA, **kwargs):
        logger.debug("ENRICH DATA USING KEREMIT API -----------------------")

        # check if all necessary configuration informations is available
        if 'services' not in kwargs or 'kermit' not in kwargs['services']:
            logger.debug("  * Missing configuration informations. Skip it !")
            return data
        if 'base_url' not in kwargs['services']['kermit']:
            logger.debug("  * Missing 'base_url' configuration key. Skip it !")
            return data
        if 'journal-issue' not in data:
            logger.debug("  * No journal information into original data. Skip it !")
            return data

        config = kwargs['services']['kermit']
        if 'headers' not in config:
            config['headers'] = {}

        # Choose the query key. The best query key are the ISSN's (all types). If no ISSN can be found into the data,
        # we will try to query Kermit database using the journal title if it exists
        if 'issn-type' in data['journal-issue'] and len(data['journal-issue']['issn-type']) > 0:
            issns = [issn['value'] for issn in data['journal-issue']['issn-type'] if 'value' in issn]
            logger.debug("  * Searching into Kermit using ISSN's :: [{0}]".format(', '.join(issns)))
            issns = [u'identifiers.identifier:"{0}"'.format(i) for i in issns]
            query = " OR ".join(issns)
        elif 'title' in data['journal-issue']:
            d = data['journal-issue']['title']
            logger.debug(u"  * Searching into Kermit using journal title :: [{0}]".format(d))
            query = u'titles.title="{0}"'.format(d)
        else:
            logger.debug("  !! No avaialble data to search into Kermit. Skip it")
            return data

        # Request the Kermit API and if some result could be found, merge Kermit data with original data.
        # If Kermit Rest API return otherwise than a '200 OK' response, return the original data
        # If request is success, merge the Kermit data to original data depending of the 'favorite_data' mode
        r = requests.get(config['base_url'], params={'query': query}, headers=config['headers'])
        if r.status_code != requests.codes.ok:
            logger.info("  !! Kermit Rest API failed :: HTTP_CODE [{code}]".format(code=r.status_code))
            return data
        resp = r.json()
        if resp['hits'] == 0:
            logger.debug("  * No data found into Kermit. Skip it")
            return data
        jdata = resp['results'][0]
        # if data found, get data from Rest API result
        kermit_data = {'journal-issue': {'title': jdata['title']}}
        if any(j in jdata.keys() for j in ['issn', 'eissn', 'lissn']):
            kermit_data['journal-issue']['issn-type'] = list()
            for t in [t for t in ['issn', 'eissn', 'lissn'] if t in jdata]:
                kermit_data['journal-issue']['issn-type'].append({'type': t, 'value': jdata[t]})
        if 'peerReviewed' in jdata and jdata['peerReviewed']:
            kermit_data['journal-issue']['peer-reviewed'] = True
        logger.debug("  * found data :: "+str(kermit_data))

        # merge data
        if favorite_data == USER_DATA:
            merged_data = EnrichDataEngine.merge_data(data, dict(kermit_data))
        else:
            merged_data = EnrichDataEngine.merge_data(dict(kermit_data), data)
        merged_data = json.dumps(merged_data)
        return json.loads(merged_data)
