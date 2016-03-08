from optparse import OptionParser

import pychromecast

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
                cast.start_app(options.get("APP_ID"))
                print "Starting application %s on %s" % (options.get("APP_ID"), options.get("CHROMECAST_FRIENDLY_NAME"))
                exit(0)
            
            else:
                print "Chromecast %s is busy!" % options.get("CHROMECAST_FRIENDLY_NAME")
                
        else:
            print "No chromecast found with friendly name %s" % options.get("CHROMECAST_FRIENDLY_NAME")
            exit(1)
    
if __name__ == "__main__":
    main()