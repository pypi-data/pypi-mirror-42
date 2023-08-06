from exceptions import DoubleFoundException
import requests
import logging


logger = logging.getLogger(__name__)


class CheckDoubleEngine(object):
    """ Using this engine, you can check if some publications are already present into DIAL corresponding to
        publication data. Some basics handlers are already present (DOI checker, ISBN checker). You can add some
        `:class:pydial.double.CheckDoubleHandler` subclass. Only 'enable' handler will be used
    """

    def __init__(self, services=None):
        self.services = services
        self._handlers = [cls(self) for cls in CheckDoubleHandler.__subclasses__()]

    def add_handler(self, handler):
        self._handlers.append(handler(self))

    def proceed(self, data):
        for hdl in [hdl for hdl in self._handlers if hdl.enable]:
            pids = hdl.call(data)
            if pids is not None:
                raise DoubleFoundException("Double publication found", handler_class=hdl.__class__, pids=pids)

    def call_solr(self, **kwargs):
        """ This method call solr to search document and return pids of found document.
            :param kwargs: arguments used to filter the solr response.
            :return: A list of found pids, None if no result was found
        """
        params = [
            ('wt', 'python'),
            ('fl', 'ss_pid'),
            ('q', 'ss_state:A')
        ]
        for k, v in kwargs.items():
            params.append(('fq', '{key}:"{data}"'.format(key=k, data=v.replace('"', '\\"'))))
        resp = requests.get(self.services['solr']['base_url'], params=params)
        resp.raise_for_status()
        response = eval(resp.text)
        if response['response']['numFound'] > 0:
            return [doc['ss_pid'] for doc in response['response']['docs']]
        return None


class CheckDoubleHandler(object):

    name = "Abstract check double checker"
    enable = False

    def __init__(self, engine):
        self.engine = engine

    def call(self, data):
        raise NotImplementedError("Abstract method, check children class")


class DOICheckDoubleHandler(CheckDoubleHandler):

    name = "DOI double checker"
    enable = True

    def call(self, data):
        if 'doi' in data:
            logger.debug("* Checking existing DOI [{doi}]...".format(doi=data['doi']))
            return self.engine.call_solr(sm_doi=data['doi'])


class ISBNCheckDoubleHandler(CheckDoubleHandler):

    name = "ISBN double checker"
    enable = True

    def call(self, data):
        if 'isbn' in data:
            logger.debug("* Checking existing ISBN [{isbn}]...".format(isbn=data['isbn']))
            return self.engine.call_solr(sm_isbn=data['isbn'])

