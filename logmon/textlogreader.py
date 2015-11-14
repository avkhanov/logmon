from logmon.logreader import LogReader


class TextLogReader(LogReader):
    def __init__(self, filename):
        pass

    def attach(self):
        pass

    def detach(self):
        pass

if __name__ == "__main__":
    log = TextLogReader("test.txt")
    print("Hello World")
