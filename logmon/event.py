from logmon.exceptions import InvalidEventFieldName, EventFieldDoesNotExist
import re


class Event(object):
    def __init__(self, regex_filter):
        object.__setattr__(self, '_dict', {})
        object.__setattr__(self, '_regex_filter', regex_filter)

    def __setattr__(self, key, value):
        if key[0] == "_":
            raise InvalidEventFieldName(key)

        self._dict[key] = value

    def __getattr__(self, item):
        try:
            ret = self._dict[item]
        except KeyError:
            raise EventFieldDoesNotExist(item)

        return ret

    def _match(self, string):
        if re.match(self._regex_filter, string) is None:
            return False
        else:
            return True

    def _gen_event_object(self, string):
        ret = Event(self._regex_filter)

        for i in self._dict:
            m = re.search(self._dict[i], string)

            if m is None:
                value = None
            else:
                groups = m.groups()

                if len(groups) == 1:
                    value = groups[0]
                else:
                    value = groups

            setattr(ret, i, value)

        return ret

if __name__ == "__main__":
    string = "ERROR - file: test_file.py; line: 278; message: Something just happened;"
    e = Event("^ERROR\s+-\s+.*$")
    e.filename = "file:\s+(.*?);"
    e.line = "line:\s+(.*?);"
    e.message = "message:\s+(.*?);"

    r = e._gen_event_object(string)

    print("File: %s\nLine: %s\nMessage: %s" % (r.filename, r.line, r.message))
