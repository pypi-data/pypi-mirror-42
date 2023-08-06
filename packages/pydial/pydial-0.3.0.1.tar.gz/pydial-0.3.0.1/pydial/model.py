# coding: utf-8

from eulfedora.models import DigitalObject, XmlDatastream
from eulfedora.util import parse_rdf, RequestFailed
from rdflib import URIRef, Literal
from rdflib.namespace import XSD
from marc import Marcxml
from six.moves import zip_longest
from datetime import datetime

import re
import os
import pymarc
import requests
import urllib2
import logging


log = logging.getLogger(__name__)


class DialObject(DigitalObject):

    _additional_relations = {
        URIRef("http://dial.academielouvain.be/ontologies/policies#accessType"): 'access_type',
        URIRef("http://dial.academielouvain.be/ontologies/policies#embargoDate"): 'embargo_enddate',
        URIRef("http://dial.academielouvain.be/ontologies/policies#restrictionIP"): 'ip_restrictions',
        URIRef("http://www.w3.org/2000/01/rdf-schema#comment"): 'comment',
    }

    _institutions_ip_ranges = {
        'ucl': ['130.104.*.*', '193.190.244.*', '193.190.89.*'],  # UCL, FUCaM, MGD
        'unamur': ['138.48.*.*'],
        'uslb': ['193.190.250.*', '193.190.251.*']
    }
    _institutions_ip_ranges['fundp'] = _institutions_ip_ranges['unamur']
    _institutions_ip_ranges['fusl'] = _institutions_ip_ranges['uslb']

    @staticmethod
    def get_type(data):
        """ This static method return the best DialObject depending of provided data. Into data, we need to provide
            information about the publication document type. Depending of value found, the function will create the
            best model object and return ths object.
            Document type must be specified into ['type']['document-type'] data key. If not, then a exception will be
            raised.

            :param data: the publication data conform to Dial JSON schemas
            :return a new fedora object (with pid, ...)
            :raise KeyError if document type cannot be found into data parameter
        """
        if 'type' not in data:
            raise KeyError("'type' key are required into data")
        if 'document-type' not in data['type']:
            raise KeyError("'document-type' kay are required into data['type']")
        mapping = {
            'article': DialArticleObject,
            'speech': DialSpeechObject,
            'book': DialBookObject,
            'book-chapter': DialBookChapterObject,
            'working-paper': DialWorkingPaperObject,
            'report': DialReportObject,
            'patent': DialPatentObject
        }
        return mapping[data['type']['document-type']] if data['type']['document-type'] in mapping else DialObject

    def call_method(self, method_name, params=None):
        """ This method allow to call a dissemination of this object without know the service object providing it.
            If this method is provided by multiple service objects, then the method return the first method that
            return a valid response (HTTP_STATUS == 200)

            By exemple in DIAL : the method 'getCitation' is present for multiple content model. For 'boreal:12555' this
            method is provided by 'ThesisCM' and for 'boreal:145664' this method is provided by 'ArticleCM'.

            :param method_name: the dissemination method name to call
            :param params: the list of params requested by this dissemination. Key=arg name, value=arg value
            :type method_name: str
            :type params: dict, None
            :return: the response of the dissemination call (to get response content => response.text|raw_content)
            :rtype: <request.model.Response>
        """
        for service_pid, list_methods in self.methods.iteritems():
            if method_name in list_methods:
                try:
                    req = self.getDissemination(service_pid, method_name, params)
                    if req.status_code == 200:
                        req.encoding = 'utf-8'  # force 'utf-8' encoding
                        return u'{0}'.format(req.text)
                except IOError:
                    # just catch the error but do nothing, try to use the next matching dissemination
                    pass
        return None

    @property
    def attached_files(self):
        """ This method allow to retrieve datastream representing attached file about this publication.
            To retrieve these datastreams, the method will skip all technical datastream (XML, JSON) ; for datastreams
            remaining, some technical informations (access_type, embargo and IP restrictions).

            :return: a list of :class:`eulfedora.model.Datastream` enrich with special attributes :
                * uriref          : the URI representing the datastream
                * access_type     : the access type for this datastream (OpenAccess, ucl:restricted, ucl:protected, ...)
                * embargo_enddate : the date at which the embargo will be end using the TZ date format
                * ip_restrictions : a list of ip ranges to limit the access for this datastream
        """

        # remove technical datastream
        #    FedoraCommons objects has a set of datastream : some technical datastreams, and some attached datastreams.
        #    We need to only keep the attached datastream. To filter this set, we will remove all datastreams with
        #    some specific mimeType
        technical_mimetypes = ['text/xml', 'application/rdf+xml', 'application/json']
        ds_ids = {ds_id: self.getDatastreamProfile(ds_id) for ds_id, d in self.ds_list.items()
                  if d.mimeType not in technical_mimetypes}

        # add some technical information for attached datastreams (see `self._additional_relations`).
        #   - access_type     : the access restriction for this datastream (OA, Restricted, Protected, Embargo)
        #   - embargo_enddate : if access_type of the datastream is 'embargo', then add the embargo end date
        #   - ip_restrictions : a list of additional allowed IP ranges
        for ds_id, datastream in ds_ids.items():
            datastream.id = ds_id
            datastream.access_type = "OpenAccess"  # default access type
            datastream.uriref = URIRef("info:fedora/{pid}/{ds_id}".format(pid=self.pid, ds_id=ds_id))
            response = self.api.getRelationships(self.pid, subject=datastream.uriref)
            if response.status_code == 200:
                for s, p, o in parse_rdf(response.text, str(datastream.uriref)):
                    key = self._additional_relations[p]
                    data = str(o)
                    if key == 'embargo_enddate':
                        data = datetime.strptime(data[:10], "%Y-%m-%d")
                    if key == 'ip_restrictions':
                        if hasattr(datastream, key):
                            getattr(datastream, key).append(data)
                            data = getattr(datastream, key)
                        else:
                            data = [data]
                    setattr(datastream, key, data)

        # remove embargo access type if embargo enddate is over. In normal process, when an embargo reach the limit,
        # a script must remove the embargo access type to OpenAccess type. But sometimes, the embargo access type is
        # not removed.... So check the embargo enddate with today, if embago is over, change datastream access type to
        # OpenAccess
        # In the same time, create IP restrictions base on datastream access_type
        for ds_id, datastream in ds_ids.items():
            if 'embargo' in datastream.access_type and hasattr(datastream, 'embargo_enddate'):
                if datastream.embargo_enddate < datetime.today():
                    datastream.access_type = "OpenAccess"
                    delattr(datastream, 'embargo_enddate')
            if datastream.access_type == 'OpenAccess':
                if hasattr(datastream, 'ip_restrictions'):
                    delattr(datastream, 'ip_restrictions')  # OpenAccess cannot play with IP restrictions
            else:
                m = re.search(r'(?P<institution>\w+):(?P<type>\w+)', datastream.access_type)
                if m.groups():
                    datastream.access_type = m.group('type').lower()
                    institution = m.group('institution').lower()
                    if institution in self._institutions_ip_ranges:
                        if hasattr(datastream, 'ip_restrictions'):
                            getattr(datastream, 'ip_restrictions').extend(self._institutions_ip_ranges[institution])
                        else:
                            setattr(datastream, 'ip_restrictions', self._institutions_ip_ranges[institution])
        return ds_ids

    def set_relationship(self, s, p, o):
        """ This method add a relation about this object or one of his datastream ; replacing previous relations if
            it exists.

        :param s: the relation subject. Must be a valid fedora URI (info:fedora/pid[/ds_id]) as :class:`rdflib.URIRef`
        :param p: the relation unifying the subject and the object. As :class:`rdflib.URIRef`
        :param o: the relation object. If 'None', no relation will be created but old relations will be removed.
        :type o: :class:`rdflib.Literal` or :class:`rdflib.URIRef`
        :return: :class:`request.Response`
        """
        # remove previous relations if exists
        response = self.api.getRelationships(self.pid, subject=s, predicate=p)
        if response.status_code == 200:
            for s1, p1, o1 in parse_rdf(response.text, s):
                literal = isinstance(o1, Literal)
                datatype = o1.datatype if literal else None
                # special process for XSD.datetime. Fedora need 'yyyy-MM-ddTHH:mm:ss.SSSZ' but rdflib use isoformat.
                if datatype and str(datatype) == 'http://www.w3.org/2001/XMLSchema#dateTime':
                    o1 = o1.value.strftime('%Y-%m-%dT%H:%I:%S.000Z')
                self.api.purgeRelationship(self.pid, s1, p1, o1, isLiteral=literal, datatype=datatype)
        # add new relations if needed
        if o is not None:
            o_list = o if isinstance(o, list) else [o]
            for o in o_list:
                literal = isinstance(o, Literal)
                datatype = o.datatype if literal else None
                # special process for XSD.datetime. Fedora need 'yyyy-MM-ddTHH:mm:ss.SSSZ' but rdflib use isoformat.
                if datatype and str(datatype) == 'http://www.w3.org/2001/XMLSchema#dateTime':
                    o = o.value.strftime('%Y-%m-%dT%H:%I:%S.000Z')
                response = self.api.addRelationship(self.pid, s, p, o, isLiteral=literal, datatype=datatype)
        return response

    def _compute_datastream_id(self, file_uri):
        """ Allow to compute the next datastream ID that could be used for this object based on a filename.
            Base on a file URI (especially this extension), the function will return a free datastream ID that
            can be use for adding a new datastream in this object

        :param file_uri: the file uri name
        :return a free datastream ID for this object
        """
        filename, file_extension = os.path.splitext(file_uri)
        file_extension = file_extension.replace('.', '').upper() if len(file_extension) else 'UND'
        ds_ids = [int(ds_id.split('_')[-1]) for ds_id in self.ds_list.keys() if ds_id.startswith(file_extension+"_")]
        max_id = max(ds_ids) if ds_ids else 0
        return "{ext}_{count:02d}".format(ext=file_extension, count=max_id+1)

    def _update_rels_int_relationship(self, ds_id, **kwargs):
        """ this private function manage all relations linked to a datastram. Used by :meth:`update_file` and
            :meth:`add_file`.

        :param ds_id: the datastream ID
        :param kwargs: relation to link to this datastream. Allowed arguments values are :
            * access_type     : the access type about this datastream. Allowed values are 'restrited', 'protected',
                                'embargo'. If you need to set OpenAccess for this datastream, use an empty string as
                                param value.
            * embargo_enddate : the date where the embargo will be over as a :class:`datetime.datetime`
            * ip_restrictions : a list of ip range where the datastream will be allowed to download
            * version         : a comment/note about this datastream (preprint, postprint, ...)
        """
        ds_uri = URIRef("info:fedora/{pid}/{ds_id}".format(pid=self.pid, ds_id=ds_id))
        reversed_relations = {v: k for k, v in self._additional_relations.items()}
        if 'access_type' in kwargs:
            # we can use an empty string as 'access_type' value to tell than the access type is now OpenAccess.
            # In this case, no relation should be stored into triplestore but we need to remove previous access_type
            # relation if exists ; so we can use 'None' as access_type value in this case (cfr :meth:`set_relationship`
            access_type = Literal(u'ucl:{0}'.format(kwargs['access_type'])) if len(kwargs['access_type']) > 0 else None
            self.set_relationship(ds_uri, reversed_relations['access_type'], access_type)
            if access_type and 'embargo' in access_type and 'embargo_enddate' in kwargs and kwargs['embargo_enddate']:
                embargo_enddate = Literal(kwargs['embargo_enddate'], datatype=XSD.dateTime)
                self.set_relationship(ds_uri, reversed_relations['embargo_enddate'], embargo_enddate)
            else:  # remove embargo enddate if access type isn't 'embargo'
                self.set_relationship(ds_uri, reversed_relations['embargo_enddate'], None)
        if 'ip_restrictions' in kwargs:
            if len(kwargs['ip_restrictions']):
                ranges = [Literal(ip) for ip in kwargs['ip_restrictions']]
                self.set_relationship(ds_uri, reversed_relations['ip_restrictions'], ranges)
            else:
                self.set_relationship(ds_uri, reversed_relations['ip_restrictions'], None)
        if 'version' in kwargs:
            version = Literal(kwargs['version']) if kwargs['version'] is not None else None
            self.set_relationship(ds_uri, reversed_relations['comment'], version)

    def update_file(self, ds_id, label=None, mime_type=None, alt_ids=[], versionable=True, state=None, location=None,
                    access_type=u'', embargo_enddate=None, ip_restrictions=None, version=None):
        """ Modify an existing datastream, similar to :method:`add_file`

        :param ds_id: the datastream ID to update
        :param label: the datastream label (filename with extension). If not specified, the `location` basename will be
                      used if present (not always human readable and with correct extension)
        :param mime_type: the mime type for this datastream
        :param alt_ids: a list of alternated ID's for this file (will be join using ' ' (space) as separator
        :param versionable: if this datastream is versionable. Default is True
        :param state:  A(Active), I(Inactive), D(Deleted) (default is A)
        :param location: URI where find the file to add
        :param access_type: Access type in (restricted, protected, embargo). Not required for OpenAccess
        :param embargo_enddate: The date when the embargo on this file will be over (only applicable if access type is
                                'embargo'. Must be type of :class:`datetime.datetime`
        :param ip_restrictions: a list of ip ranges where the file will be available (except UCL ip ranges)
        :param version: a version label about this file (preprint, postprint, first version, ...)
        :return: return a tuple (HTTP response code, message)
                 If successful, the HTTP code is 200 (OK) and message is datastream ID
                 If failed, the HTTP code depends of the errors occurred and the message is the fedora returned message
        """
        # create arguments for Fedora API call ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        http_args = {}
        if label:
            http_args['dsLabel'] = label
        if mime_type:
            http_args['mimeType'] = mime_type
        if location:
            http_args['dsLocation'] = location
        if alt_ids:
            http_args['altIDs'] = ','.join(alt_ids)
        if versionable is not None:
            http_args['versionable'] = versionable
        if state:
            http_args['dsState'] = state

        # call the Fedora API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        response = self.api.modifyDatastream(self.pid, ds_id, **http_args)
        if response.status_code != requests.codes.ok:
            return response.status_code, response.content

        # update relation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        params = {
            'access_type': access_type,
            'embargo_enddate': embargo_enddate,
            'ip_restrictions': ip_restrictions,
            'version': version
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}
        self._update_rels_int_relationship(ds_id, **filtered_params)
        return response.status_code, ds_id

    def add_file(self, location, mime_type=None, ds_id=None, label=None, alt_ids=[], versionable=True, state='A',
                 access_type=u'', embargo_enddate=None, ip_restrictions=[], version=None):
        """ This method allow to add any file into this object. If no 'ds_id' parameter are specified into additional
            parameter, than it will be automatically created depending of the filename (extracted from the 'location'
            URI).
            Depending of the mime type the FedoraCommons datastream :attr:`controlGroup` will be known ; By
            default, this attribute will be 'M' (Managed) except if mime type of the file seems to be an XML datastream
            then it will be 'X'. !!! This attribute cannot be change later.

        :param location: URI where find the file to add
        :param mime_type: the mime type of the file
        :param ds_id: the desired datastream ID. It is recommended don't specify this argument. The datastream ID
                      should be automatically compute using the dsLabel
        :param label: the datastream label (filename with extension). If not specified, the location basename will
                      be used (not always human readable and with correct extension)
        :param alt_ids: a list of alternated ID's for this file (will be join using ' ' (space) as separator
        :param versionable : If datastream must be versionable. Default is True
        :param state: A(Active), I(Inactive), D(Deleted) (default is A)
        :param access_type: Access type in (restricted, protected, embargo). Not required for OpenAccess
        :param embargo_enddate: The date when the embargo on this file will be over (only applicable if access type
                                is 'embargo'. Must be type of :class:`datetime.datetime`
        :param ip_restrictions: a list of ip ranges where the file will be available (except UCL ip ranges)
        :param version: a version label about this file (preprint, postprint, first version, ...)

        :return: return a tuple (HTTP response code, message)
                 If successful, the HTTP code is 200 (OK) and message is datastream ID
                 If failed, the HTTP code depends of the errors occurred and the message is the fedora returned message
        """
        # Check arguments values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if access_type:
            assert access_type in ['restricted', 'protected', 'embargo'], \
                "'access_type' are incorrect values. Allowed values are ('restricted', 'protected', 'embargo')"
            if access_type == 'embargo':
                assert embargo_enddate is not None, "You need to specify an embargo enddate"
                assert isinstance(embargo_enddate, datetime), \
                    "'embargo_enddate' param must be :class:`datetime.datetime`"

        # create arguments for Fedora API call ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        http_args = {}
        if label:
            http_args['dsLabel'] = label
        if mime_type:
            http_args['mimeType'] = mime_type
        else:
            request = urllib2.Request(location)
            request.get_method = lambda: 'HEAD'
            try:
                response = urllib2.urlopen(request)
                http_args['mimeType'] = response.info().getheader('Content-Type')
                if http_args['mimeType'] is None:
                    raise IOError("Unable to get the mime-type of response")
            except IOError as ie:
                log.warning("Unable to get file mimetype :: "+str(ie))
                http_args['mimeType'] = 'application/octet-stream'
        http_args['dsLocation'] = location
        if alt_ids:
            http_args['altIDs'] = ' '.join(alt_ids)
        if versionable is not None:
            http_args['versionable'] = versionable
        if state:
            http_args['dsState'] = state
        http_args['controlGroup'] = 'X' if 'xml' in http_args['mimeType'] else 'M'
        if ds_id:
            http_args['dsID'] = ds_id
        else:
            filename = label if label else location
            http_args['dsID'] = self._compute_datastream_id(filename)

        # call the Fedora API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    remove 'dsID' attribute from kwargs (it should be used as positional param instead of named param) and
        #    call Fedora API.
        ds_id = http_args['dsID']
        del http_args['dsID']
        response = self.api.addDatastream(self.pid, ds_id, **http_args)
        if response.status_code != requests.codes.created:
            return response.status_code, response.content

        # update relation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        params = {
            'access_type': access_type,
            'embargo_enddate': embargo_enddate,
            'ip_restrictions': ip_restrictions,
            'version': version
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}
        self._update_rels_int_relationship(ds_id, **filtered_params)
        return response.status_code, ds_id

    def delete_datastream(self, ds_id, purge=False):
        """ This method allow to delete a datastream of this object. By default, the datastream is set as 'D'elete state
            but if the `purge` parameter is set to True, then the datastream will be purged from object with no return.
            In this case, all relations linked to the datastram will be removed.

        :param ds_id: the datastream ID
        :param purge: True if you would purge the datastream from Fedora object and relations linked to this datastream
        :return: return a tuple where first argument will be the delete state (True or False) and the second a message
                 if needed (a message should always be set if False is returned)
        """
        # simple case, put the datastream if state 'D'eleted
        if not purge:
            datastream = self.getDatastreamProfile(ds_id)
            if datastream.state == 'D':
                return True, "Datastream state are now 'D'"
            try:
                success = self.api.setDatastreamState(self.pid, ds_id, dsState='D')
                if not success:
                    raise RequestFailed("Error updating datastream state")
                return True, "Datastream state are now 'D'"
            except RequestFailed as rf:
                return False, rf.message
        # complex case, we need to purge the datastream and all relations linked to it
        else:
            self._update_rels_int_relationship(ds_id, access_type='', ip_restrictions=[], version=None)
            response = self.api.purgeDatastream(self.pid, ds_id)
            return response.status_code == requests.codes.ok, response.content


class DialMarcXMLObject(DialObject):
    """
        This class represent a FedoraCommons object for which metadata comes from MARCXML datastream. This object
        reflects the UCLouvain DIAL object model ; the location of some metadata are specific for the DIAL project
    """

    AUTHOR_SUBFIELD_MAP = {
        'a': 'name',
        'g': 'email',
        '5': 'institution',
        'o': 'oricd-id',
        'i': 'institution_id',
        'e': 'role'
    }

    marcxml = XmlDatastream("MARCXML", "descriptive metadata", Marcxml, defaults={
        'versionable': True,
        'control_group': 'X',
    })

    @property
    def title(self):
        fields = self.marcxml.content.marc_data.get_fields('245')
        if fields:
            return ' : '.join(fields.pop(0).get_subfields('a', 'b'))
        return None

    @property
    def urls(self):
        """ This method allows to retrieve all urls stored into the MARCXML. Each urls are a dict containing two keys :
              * 'type' : the URL type (Handle, Pubmed, DOI, ...) This key could be None
              * 'url' : the URL value
            Note : The DOI url are completed with the doi resolution prefix to get a full valid doi URL. By example :
            '10.12345/test_publication' --> 'https://dx.doi.org/10.12345/test_publication'

            :return a dict of all URL's stored into the object
        """
        fields = self.marcxml.content.marc_data.get_fields('856')
        if fields:
            urls = [{'type': f['z'], 'url': f['u']} for f in fields]
            for url in urls:
                if url['type'] is not None and url['type'].upper() == 'DOI' and not url['url'].startswith('http'):
                    url['url'] = 'https://dx.doi.org/'+url['url']
            return urls
        return []

    @property
    def handle(self):
        handles = [url['url'] for url in self.urls if url['type'] is not None and url['type'].lower() == 'handle']
        return next(iter(handles), None)  # return the first handle found or None if no handle url exists.

    @property
    def flags(self):
        """ This method allows to retrieve all flags stored into the MARCXML. Each flag are a dict containing the
            following keys :
              * 'type' : the flag type as a string
              * 'timestamp' : the date where tha flag were created as datetime class
              * 'user' : the user which create the tag as a string

            :return the list of all flags. Each flag is a dict
        """
        fields = self.marcxml.content.marc_data.get_fields('909')
        if fields:
            flags = []
            for f in fields:
                flags.append({
                    'type': f['a'],
                    'user': f['c'],
                    'timestamp': datetime.strptime(f['d'].replace('Z', '000Z'), '%Y-%m-%dT%H:%M:%S.%fZ')
                })
            return flags
        return None

    @property
    def authors(self):
        """ This method allows to retrieve all authors for the publication. For each found author, MARC subfields are
            mapped to a human readable style (see AUTHOR_SUBFIELD_MAP for subfields mapping)

            :return a list of authors. Each author is a dict.
        """
        authors = []
        marc_authors = self.marcxml.content.marc_data.get_fields('100', '700')
        for author in marc_authors:
            data = {self.AUTHOR_SUBFIELD_MAP[tag]: value for tag, value in zip_longest(*[iter(author.subfields)] * 2)\
                    if tag in self.AUTHOR_SUBFIELD_MAP}
            authors.append(data)
        return authors

    def get_fields(self, *args):
        """ wrapper function to pymarc.record.get_fields() function """
        return self.marcxml.content.marc_data.get_fields(*args)

    def get_metadata(self, tag, code):
        """ This method search into the MARCXML a tag/subfield. If multiple field are found, return the first found

            :param tag: the datafield tag code
            :param code: the subfield code
            :return: the corresponding tag/subfield found ; None if not found
            :rtype str
        """
        field = self.marcxml.content.marc_data[tag]
        if field is not None:
            return u'{0}'.format(field[code])
        return None

    def add_flag(self, text, user):
        """ This method allow to add a flag for this publication. This flag will be stored into the MARCXML as a
            909 datafield.

            :param text: the type of flag to add. By exemple : 'validated', 'approuved', 'custom text ...', ...
            :param user: the user name who create the flag
            :type text: basestring
            :type user: basestring
        """
        subfields = ['a', text, 'd', datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%I:%S.000Z'), 'c', user]
        field = pymarc.Field(tag=909, indicators=['', ''], subfields=subfields)
        self.marcxml.content.marc_data.add_ordered_field(field)


class DialResearchPublicationObject(DialMarcXMLObject):

    default_pidspace = "boreal"
    CONTENT_MODELS = ['info:fedora/boreal-system:ResearchPublicationCM']


class DialArticleObject(DialResearchPublicationObject):

    CONTENT_MODELS = [
        'info:fedora/boreal-system:ResearchPublicationCM',
        'info:fedora/boreal-system:ArticleCM'
    ]


class DialSpeechObject(DialResearchPublicationObject):
    """
        Special class to manage a conference speech from Dial repository.
    """

    CONTENT_MODELS = [
        'info:fedora/boreal-system:ResearchPublicationCM',
        'info:fedora/boreal-system:SpeechCM'
    ]


class DialBookObject(DialResearchPublicationObject):
    """
        Special class to manage a book from Dial repository.
    """

    CONTENT_MODELS = [
        'info:fedora/boreal-system:ResearchPublicationCM',
        'info:fedora/boreal-system:BookCM'
    ]


class DialBookChapterObject(DialResearchPublicationObject):
    """
        Special class to manage a book chapter from Dial repository.
    """

    CONTENT_MODELS = [
        'info:fedora/boreal-system:ResearchPublicationCM',
        'info:fedora/boreal-system:BookChapterCM'
    ]


class DialWorkingPaperObject(DialResearchPublicationObject):
    """
        Special class to manage a working-paper from Dial repository.
    """

    CONTENT_MODELS = [
        'info:fedora/boreal-system:ResearchPublicationCM',
        'info:fedora/boreal-system:WorkingPaperCM'
    ]


class DialReportObject(DialResearchPublicationObject):
    """
        Special class to manage a report from Dial repository.
    """

    CONTENT_MODELS = [
        'info:fedora/boreal-system:ResearchPublicationCM',
        'info:fedora/boreal-system:ReportCM'
    ]


class DialPatentObject(DialResearchPublicationObject):
    """
        Special class to manage a book from Dial repository.
    """

    CONTENT_MODELS = [
        'info:fedora/boreal-system:ResearchPublicationCM',
        'info:fedora/boreal-system:PatentCM'
    ]


class DialEbookObject(DialMarcXMLObject):

    default_pidspace = 'ebook'
    CONTENT_MODELS = ['info:fedora/boreal-system:ebookCM']

