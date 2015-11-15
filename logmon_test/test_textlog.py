import unittest
import threading
import time
import tempfile
import os
from logmon.textlog import TextLog

file_created = threading.Lock()
log_attached = threading.Lock()


class TestTextLog(unittest.TestCase):
    @classmethod
    def write_to_log(cls, filename, num_repeats=10):
        with open(filename, "w") as f:
            file_created.release()
            repeat = 0
            log_attached.acquire()

            while repeat < num_repeats:
                f.write("Repeat %s" % (repeat + 1))
                f.flush()
                time.sleep(1.5)
                repeat += 1

            log_attached.release()

    @classmethod
    def read_from_log(cls, log_obj, num_repeats=20):
        repeat = 0
        ret = ""
        while repeat < num_repeats:
            ret += log_obj.read()
            time.sleep(1)
            repeat += 1

        return ret

    def setUp(self):
        self.tmp_filename = tempfile.mktemp()
        self.object = TextLog(self.tmp_filename)

    def test_attach(self):
        pass

    def test_read(self):
        log_attached.acquire()
        file_created.acquire()

        thread = threading.Thread(target=TestTextLog.write_to_log, args=[self.tmp_filename])
        thread.start()

        file_created.acquire()
        self.object.attach()
        log_attached.release()

        read_log = TestTextLog.read_from_log(self.object)

        thread.join()

        with open(self.tmp_filename, 'r') as f:
            self.assertEqual(f.read().strip(), read_log.strip())

    # def tearDown(self):
    #     os.remove(self.tmp_filename)

