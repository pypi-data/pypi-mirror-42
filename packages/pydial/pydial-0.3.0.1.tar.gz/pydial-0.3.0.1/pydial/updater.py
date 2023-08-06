# coding: utf-8
import lxml.etree as ET
import logging

log = logging.getLogger(__name__)


class RulesEngine(object):

    rules = []
    _namespaces = {
        'rdf': u'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs': u'http://www.w3.org/2000/01/rdf-schema#',
        'owl': u'http://www.w3.org/2002/07/owl#',
        'xsd': u'http://www.w3.org/2001/XMLSchema#',
        'fedora': u"info:fedora/fedora-system:def/relations-external#",
        'fedora_model': u"info:fedora/fedora-system:def/model#",
        'dc': u"http://purl.org/dc/elements/1.1/",
        'oai_dc': u"http://www.openarchives.org/OAI/2.0/oai_dc/",
        'dcterms': u'http://purl.org/dc/terms/',
        'mods': u'http://www.loc.gov/mods/v3',
        'marc': u'http://www.loc.gov/MARC21/slim'
    }

    def __init__(self, rules=[]):
        self.rules = rules

    def __repr__(self):
        return "<{0} :: {1} rules>\n".format(self.__class__.__name__, len(self.rules))

    def add_namespaces(self, prefix, uri):
        if prefix in self._namespaces:
            raise KeyError("The prefix '{0}' is already used for <{1}> URI".format(prefix, self._namespaces[prefix]))
        self._namespaces[prefix] = uri

    def run(self, fc_obj):
        # [1] load in a dict all datastream used by this engine. -----------------------------
        #    Check all defined rules and try to load the corresponding datastream content. To be a "valid" datastream
        #    the datastream must exists into the object and the mimeType of this datastream must be 'text/xml'.
        #    If all is good, parse the datastream content to be a valid XML node object.
        datastreams = {}
        for idx, rule in enumerate(self.rules):
            if rule.datastream not in fc_obj.ds_list.keys():
                log.warn("Cannot applied rule {0} for [{1}] :: datastream doesn't exists".format(rule, fc_obj.pid))
                del(self.rules[idx])
                continue
            ds = fc_obj.getDatastreamObject(rule.datastream)
            if not fc_obj.ds_list[rule.datastream].mimeType == 'text/xml':
                log.warn("Cannot applied rule {0} for[{1}] :: {2} isn't 'text/xml'".format(rule, fc_obj.pid, ds.id))
                del(self.rules[idx])
                continue
            datastreams[ds.id] = ds

        # [2] execute each rule on corresponding datastream ---------------------------------
        #   Apply each rules and keep the changed XML to be used by other rules.
        for rule in self.rules:
            log.info("\tprocessing {0} ...".format(rule))
            node = datastreams[rule.datastream].content.node
            updated_node, counter = rule.apply(node, namespaces=self._namespaces)
            datastreams[rule.datastream].content.node = updated_node
            datastreams[rule.datastream].info_modified = True
            rule.updated_tags = counter

        # [3]Save datastream content into the Fedora object ---------------------------------
        fc_obj.save()
        return self.rules


class Rule(object):
    """ Define a basic rule to modify an Fedora XML element. This class must be abstract !!!! """

    __namespaces__ = {}
    __required_fields__ = ['datastream', 'xpath']

    def __init__(self, **kwargs):
        for f in [f for f in self.__required_fields__ if f not in kwargs]:
            raise KeyError("'{0}' parameter is required in this rule".format(f))
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __repr__(self):
        return "<{name} xpath='{xpath}'>".format(name=self.__class__.__name__, xpath=self.xpath)

    @staticmethod
    def get(**kwargs):
        class_mapper = {
            'replace': ModifyRule,
            'add': AddRule,
            'delete': DeleteRule
        }
        if 'method' not in kwargs:
            raise KeyError("'method' parameter is required")
        if kwargs['method'] not in class_mapper.keys():
            raise KeyError("'{0}' method isn't allowed ; 'add', 'replace' or 'delete.".format(kwargs['method']))
        return class_mapper[kwargs['method']](**kwargs)

    def apply(self, xml, namespaces=None):
        raise NotImplementedError("This method is an abstract method ; use subclass to apply")


class ModifyRule(Rule):
    """ Define a modify rule. This rule will be check if xpath exists, and replace all tags found by the new value.
        Attributes for this class are :
          * xml : the xml element to modify
          * xpath : the xpath to use to find tags to modify
          * value : the new value replacing the XPath tags found
    """

    __required_fields__ = ['datastream', 'xpath', 'value']

    def __init__(self, **kwargs):
        super(ModifyRule, self).__init__(**kwargs)

    def apply(self, xml, namespaces={}):
        tags = xml.xpath(self.xpath, namespaces=namespaces)
        for tag in tags:
            tag.text = self.value
        return xml, len(tags)


class AddRule(Rule):
    """ Define a add rule. This rule will try to add a tag to include into the tag define in the xpath.
        Attributes for this class are :
          * xml : the xml element to modify
          * xpath : the element where the value will be added into
          * value : the xml element to be added as a string
    """

    __required_fields__ = ['datastream', 'xpath', 'value']

    def __init__(self, **kwargs):
        super(AddRule, self).__init__(**kwargs)

    def apply(self, xml, namespaces={}):
        new_tag = ET.fromstring(self.value)
        tags = xml.xpath(self.xpath, namespaces=namespaces)
        for rootTag in tags:
            rootTag.append(new_tag)
        return xml, len(tags)


class DeleteRule(Rule):
    """ Define a delete rule. This rule will be delete all tags representing by the xpath.
        Attributes for this class are :
          * xml : the xml element to modify
          * xpath : the xpath representing all tags to delete
    """

    def __init__(self, **kwargs):
        super(DeleteRule, self).__init__(**kwargs)

    def apply(self, xml, namespaces={}):
        tags = xml.xpath(self.xpath, namespaces=namespaces)
        for tag in tags:
            tag.getparent().remove(tag)
        return xml, len(tags)
