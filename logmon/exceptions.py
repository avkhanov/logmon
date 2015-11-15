class InvalidLogReaderException(Exception):
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return "'%s' is not a valid LogReader object" % self.obj


class AlreadyListeningException(Exception):
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return "Listener object '%s' has already started listening" % self.obj


class AlreadyNotListeningException(AlreadyListeningException):
    def __str__(self):
        return "Listener object '%s' is already not listening" % self.obj


class InvalidEventFieldName(Exception):
    def __init__(self, field_name):
        self.field_name = field_name

    def __str__(self):
        return "Invalid name for Event field: '%s'. An Event field cannot start with a '_'" % self.field_name


class EventFieldDoesNotExist(Exception):
    def __init__(self, field_name):
        self.field_name = field_name

    def __str__(self):
        return "The Event field '%s' does not exist" % self.field_name
