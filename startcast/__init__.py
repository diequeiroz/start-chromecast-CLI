import socket, ssl, select, time, re
from thread import start_new_thread
from struct import pack
import pychromecast
import sys
from optparse import OptionParser

TYPE_ENUM = 0
TYPE_STRING = 2
TYPE_BYTES = TYPE_STRING

def set_options():
    parser = OptionParser(usage="Usage: startcast [options] [action] \n\n Actions: \n start [CHROMECAST_FRIENDLY_NAME] [APP_ID] - Start application on chromecast \n list - list all chromecasts on network")
    parser.add_option("-f", "--force", action="store_true", dest="force",
        help="Force application to start when chromecast is already running other application")
    return parser
    
def get_options(parser):
    options, args = parser.parse_args()
    if len(args) > 0:
        ret = {"FORCE": options.force, "ACTION": args[0]}
        if ret.get("ACTION") == "start":
            try:
                ret.update({"CHROMECAST_FRIENDLY_NAME": args[1], "APP_ID": args[2]})
            except:
               print "Define CHROMECAST_FRIENDLY_NAME APP_ID!"
               parser.print_help()
               exit(1)
                
        elif ret.get("ACTION") != "list":
            print "Invalid action: %s" % ret.get("ACTION")
            parser.print_help()
            exit(1)
    else:
        print "Define action!"
        parser.print_help()
        exit(1)
    
    return ret
    
    
def clean(s):
    return re.sub(r'[\x00-\x1F\x7F]', '?',s)
def getType(fieldId,t):
    return (fieldId << 3) | t
def getLenOf(s):
    x = ""
    l = len(s)
    while(l > 0x7F):
        x += pack("B",l & 0x7F | 0x80)
        l >>= 7
        x += pack("B",l & 0x7F)
    return x

def write_to_socket(socket, namespace, data):
    lnData = getLenOf(data)
    msg = pack(">BBBB%dsBB%dsBB%dsBBB%ds%ds" % (len("sender-0"),len("receiver-0"),len(namespace),len(lnData),len(data)),getType(1,TYPE_ENUM),0,getType(2,TYPE_STRING),len("sender-0"),"sender-0",getType(3,TYPE_STRING),len("receiver-0"),"receiver-0",getType(4,TYPE_STRING),len(namespace),namespace,getType(5,TYPE_ENUM),0,getType(6,TYPE_BYTES),lnData,data)
    msg = pack(">I%ds" % (len(msg)),len(msg),msg)
    socket.write(msg)

def main():
    parser = set_options()
    options = get_options(parser)
    if options.get("ACTION") == "list":
        for key, value in pychromecast.get_chromecasts_as_dict().items():
            print "%s \t %s" % (key, value.host)
    else:
        cast = pychromecast.get_chromecast(friendly_name=options.get("CHROMECAST_FRIENDLY_NAME"))
        cast.wait()
        if cast and cast.status:
            if cast.status.is_stand_by or options.get("FORCE"): 
                cast.quit_app()
                sckt = socket.socket()
                sckt = ssl.wrap_socket(sckt)
                sckt.connect((cast.host,8009))
        
                data = '{"type":"CONNECT","origin":{}}'
                namespace = "urn:x-cast:com.google.cast.tp.connection"
                write_to_socket(sckt, namespace, data)
        
                data = '{"type":"LAUNCH","requestId":46479001,"appId":"%s"}' % options.get("APP_ID")
                namespace = "urn:x-cast:com.google.cast.receiver"
                write_to_socket(sckt, namespace, data)
            
                print "Starting application %s on %s" % (options.get("APP_ID"), options.get("CHROMECAST_FRIENDLY_NAME"))
                exit(0)
            
            else:
                print "Chromecast %s is busy!" % options.get("CHROMECAST_FRIENDLY_NAME")
                
        else:
            print "No chromecast found with friendly name %s" % options.get("CHROMECAST_FRIENDLY_NAME")
            exit(1)
    
if __name__ == "__main__":
    main()