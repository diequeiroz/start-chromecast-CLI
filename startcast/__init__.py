def main():
    import socket, ssl, select, time, re
    from thread import start_new_thread
    from struct import pack
    import pychromecast
    import sys
    
    if sys.argv[1] == "--help":
        print "Usage: startcast CHROMECAST_FRIENDLY_NAME APP_ID"
        exit(0)
        
    try:
        CHROMECAST_FRIENDLY_NAME = sys.argv[1]
        APP_ID = sys.argv[2]
    except Exception as e:
        print "Define the 'chromecast friendly name' and 'app id' like this: startcast CHROMECAST_FRIENDLY_NAME APP_ID"
        exit(1)
        
    
    TYPE_ENUM = 0
    TYPE_STRING = 2
    TYPE_BYTES = TYPE_STRING

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

    cast = pychromecast.get_chromecast(friendly_name=CHROMECAST_FRIENDLY_NAME)
    
    if cast:
        cast.quit_app()
        socket = socket.socket()
        socket = ssl.wrap_socket(socket)
        socket.connect((cast.host,8009))

        data = '{"type":"CONNECT","origin":{}}'
        namespace = "urn:x-cast:com.google.cast.tp.connection"
        write_to_socket(socket, namespace, data)

        data = '{"type":"LAUNCH","requestId":46479001,"appId":"%s"}' % APP_ID
        namespace = "urn:x-cast:com.google.cast.receiver"
        write_to_socket(socket, namespace, data)
        
        print "Starting application %s on %s" % (APP_ID, CHROMECAST_FRIENDLY_NAME)
        exit(0)
    
    else:
        
        print "No chromecast found with friendly name %s" % (CHROMECAST_FRIENDLY_NAME)
        exit(1)
    
