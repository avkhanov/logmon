import os
from logmon.logreader import LogReader


class TextLog(LogReader):
    def __init__(self, filename):
        self._filename = filename
        self._fd = None

    def attach(self):
        # Open the log file and go to its end
        self._fd = open(self._filename, 'r')
        self._fd.seek(0, os.SEEK_END)

    def detach(self):
        self._fd.close()
        self._fd = None

    def read(self):
        # Read binary
        raw_buffer = self._fd.read()
        # utf8_buffer = raw_buffer.decode("utf-8")
        # try:
        #     self._fd.seek(-2, os.SEEK_END)
        # except OSError:
        #     self._fd.seek(0, os.SEEK_END)

        return raw_buffer

if __name__ == "__main__":
    log = TextLog("test.txt")
    print("Hello World")
