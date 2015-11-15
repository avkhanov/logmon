from logmon.textlog import TextLog
from logmon.event import Event
from logmon.listener import Listener
import time

event = Event("^ERROR\s+-\s+.*$")
event.filename = "file:\s+(.*?);"
event.line = "line:\s+(.*?);"
event.message = "message:\s+(.*?);"


def print_event(e):
    print("============= EVENT ==============")
    print("File: %s" % e.filename)
    print("Line: %s" % e.line)
    print("Message: %s" % e.message)
    print("==================================")

log = TextLog("test.txt")
listener = Listener(log)

listener.attach(event, print_event)
listener.start()
time.sleep(60)
listener.stop()
