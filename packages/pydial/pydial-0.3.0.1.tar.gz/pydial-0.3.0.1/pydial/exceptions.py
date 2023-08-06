class RecordBuilderException(Exception):
    pass


class MappingException(Exception):
    pass


class RuleConfigurationException(Exception):
    pass


class NotApplicableException(Exception):

    def __init__(self, origin, fc_obj, message=None):
        super(NotApplicableException, self).__init__(message)
        self.origin = origin
        self.fc_obj = fc_obj

    def __str__(self):
        output = "{name} isn't applicable to {pid} :: {message}".format(
            name=self.origin,
            pid=self.fc_obj.pid,
            message=self.message
        )
        return output


class ImportPublicationError(Exception):
    pass


class RecordBuilderException(ImportPublicationError):
    pass


class DoubleFoundException(ImportPublicationError):

    def __init__(self, message, handler_class, pids=[]):
        super(DoubleFoundException, self).__init__(message)
        self.handle_class = handler_class
        self.pids = pids

    def __str__(self):
        return "{message} raised from {cls} :: {pids}".format(
            message=self.message,
            cls=self.handle_class.__name__,
            pids=str(self.pids)
        )
