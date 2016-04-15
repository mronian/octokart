from transactions.models import Connection
import urllib2
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlencode
from logger.models import Operation
from logger.models import writetransactionlog, writecommitlog, writelocklog, writeloginlog

def flood(mip, mport, suburl, params, msg, logmsg, reply):
    conn=Connection.objects.all()
    
    for c in conn:
        if (c.ip, c.port) != (mip, mport):
            print "SENDING "+logmsg+" TO "+c.ip+":"+c.port
            url="http://"+c.ip+":"+c.port+suburl
            result=""
            try :
                if logmsg == "TRYLOCK":
                    writelocklog(transaction_id = msg.mid, site_id = c.ip+":"+c.port, 
                        operation = Operation.lockrequest, mode = False)
                response = urlopen( url , params)
            except HTTPError, e:
                reply[(c.ip,c.port)]="Abort"
                result = 'The server couldn\'t fulfill the request. Reason:'+str(e.code)
                print result
            except URLError, e:
                reply[(c.ip,c.port)]="Abort"
                result =  'We failed to reach a server. Reason:'+str(e.reason)
                print result
            else :
                html = response.read()
                reply[(c.ip,c.port)]=html
            
    return reply
            