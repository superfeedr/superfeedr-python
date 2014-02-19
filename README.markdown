# Superfeedr XMPP API Python Wrapper

*Warning* : this wrapper is known for its lack of support by its developer. You may want to give a look at [SFPY](http://github.com/superfeedr/sfpy) as well.

## Requirements:
If you use **Python3k**

* [SleekXMPP](http://code.google.com/p/sleekxmpp/), Download the source code : svn://netflint.net/sleekxmpp/trunk

If you use **Python 2.6** Thanks to [dfdeshom](http://github.com/dfdeshom/)

* [SleekXMPP2.6](http://bitbucket.org/dfdeshom/sleekxmpp2.6/src/) 

## Installation:
    sudo python setup.py install

## Example

    from superfeedrpy import Superfeedr
    import time

    def sf_message(event):
    	print "received event without entries"

    def sf_entry(event):
    	print "received entry with events", event

    sf = Superfeedr('user@superfeedr.com', 'password-here')
    sf.on_notification(sf_message)
    sf.on_entry(sf_entry)
    while True:
    	time.sleep(1)

## Warning

We know our limits and we know *we can’t actively support* wrappers in _every_ languages. Like everybody, we have our favorite languages and platform, and there is little chance that we ever get a deep enough knownledge in all that languages that you guys use to offer great services. So, for us, the *limit of what we can provide and support is [our API (both XMPP and PubSubHubbub)](http://superfeedr.com/documentation).*

However, we’re not blind either and we know how these parsers are important for everybody to get started and integrate Superfeedr into their existing apps, so we take great care of them and try to help people use them or fix problems. 

These libs are not ours, _they wait for your input_, _your documentation_, _your testing_, as well as_ your suggestions for new features_. We will just help gathering them and keeping track by connecting the people who made them with the people who use them.

**Please, fork it and make it better!**