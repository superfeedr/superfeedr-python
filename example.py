from superfeedrpy import Superfeedr
import time

def sf_message(event):
	print "received event without entries"

def sf_entry(event):
	print "received entry with events", event

sf = Superfeedr('demo@superfeedr.com', 'demo')
sf.on_notification(sf_message)
sf.on_entry(sf_entry)
while True:
	time.sleep(1)
