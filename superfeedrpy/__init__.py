import sleekxmpp
import logging
from optparse import OptionParser
import time
import Queue
from sleekxmpp.xmlstream.handler.callback import Callback
from sleekxmpp.xmlstream.matcher.xpath import MatchXPath

class Superfeedr(sleekxmpp.ClientXMPP):
	
	def __init__(self, jid, password):

		self.success = False
		self.notification_callback = None
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self.registerPlugin('xep_0004')
		self.registerPlugin('xep_0030')
		self.registerPlugin('xep_0060')
		self.registerPlugin('xep_0199')
		self.add_event_handler("session_start", self._start)
		self.registerHandler(Callback('superfeedr', MatchXPath("{jabber:client}message/{http://jabber.org/protocol/pubsub#event}event"), self._superfeedr_msg, thread=False))
		self.success = self.connect(('xmpp.superfeedr.com', 5222))
		if self.success:
			self.waitforstart = Queue.Queue()
			self.process(threaded=True)
			start = self.waitforstart.get(10)
			if start is None:
				self.success = False
	
	def _start(self, event):
		self.getRoster()
		self.sendPresence()
		self.waitforstart.put(True)

	def _superfeedr_msg(self, stanza):
		xml = stanza.xml
		event = {}
		statusx = xml.find('{http://jabber.org/protocol/pubsub#event}event/{http://superfeedr.com/xmpp-pubsub-ext}status')
		httpx = xml.find('{http://jabber.org/protocol/pubsub#event}event/{http://superfeedr.com/xmpp-pubsub-ext}status/{http://jabber.org/protocol/pubsub#event}http')
		next_fetchx = xml.find('{http://jabber.org/protocol/pubsub#event}event/{http://superfeedr.com/xmpp-pubsub-ext}status/{http://jabber.org/protocol/pubsub#event}next_fetch')
		itemsx = xml.find('{http://jabber.org/protocol/pubsub#event}event/{http://jabber.org/protocol/pubsub#event}items')
		entriesx = xml.findall('{http://jabber.org/protocol/pubsub#event}event/{http://jabber.org/protocol/pubsub#event}items/{http://jabber.org/protocol/pubsub#event}item/{http://www.w3.org/2005/Atom}entry')
		if None not in (statusx, httpx, next_fetchx, itemsx, entriesx):
			event['xml'] = xml
			event['feed'] = itemsx.get('node')
			event['http'] = (httpx.get('code'), httpx.text)
			event['next_fetch'] = next_fetchx.text
			event['entries'] = []
			for entryx in entriesx:
				entry = {'title': '', 'summary':'','link':('','',''), 'id':'','published':''}
				titlex = entryx.find('{http://www.w3.org/2005/Atom}title')
				summaryx = entryx.find('{http://www.w3.org/2005/Atom}summary')
				linkx = entryx.find('{http://www.w3.org/2005/Atom}link')
				idx = entryx.find('{http://www.w3.org/2005/Atom}id')
				publishedx = entryx.find('{http://www.w3.org/2005/Atom}published')
				if titlex is not None:
					entry['title'] = titlex.text
				if summaryx is not None:
					entry['summary'] = summaryx.text
				if linkx is not None:
					entry['link'] = (linkx.get('rel'), linkx.get('type'), linkx.get('href'))
				if idx is not None:
					entry['id'] = idx.text
				if publishedx is not None:
					entry['published'] = publishedx.text
				event['entries'].append(entry)
		self.event('superfeedr', event)
		if len(event['entries']) > 0:
			self.event('superfeedr_entry', event)
	
	def subscribe(self, feed):
		return self.plugin['xep_0060'].subscribe('firehoser.superfeedr.com', feed)
	
	def unsubscribe(self, feed):
		return self.plugin['xep_0060'].unsubscribe('firehoser.superfeedr.com', feed)

	def list(self, page=0):
		pubsub = ET.Element('{http://jabber.org/protocol/pubsub}pubsub')
		pubsub.attrib['xmlns:superfeedr'] = 'http://superfeedr.com/xmpp-pubsub-ext'
		subscriptions = ET.Element('subscriptions')
		subscriptions.attrib['jid'] = self.jid
		subscriptions.attrib['superfeedr:page'] = page
		pubsub.append(subscriptions)
		iq = self.xmpp.makeIqSet(pubsub)
		iq.attrib['to'] = jid
		iq.attrib['from'] = self.xmpp.fulljid
		id = iq.get('id')
		result = self.xmpp.send(iq, "<iq id='%s'/>" % id)
		if result is False or result is None or result.get('type') == 'error': return False
		nodes = result.findall('{http://jabber.org/protocol/pubsub}pubsub/{http://jabber.org/protocol/pubsub}subscriptions/{http://jabber.org/protocol/pubsub}subscription')
		if nodes is None: return []
		nodelist = []
		for node in nodes:
			nodelist.append(node.get('node', ''))
		return nodelist

	def on_notification(self, callback):
		self.add_event_handler('superfeedr', callback)
	
	def on_entry(self, callback):
		self.add_event_handler('superfeedr_entry', callback)
		
