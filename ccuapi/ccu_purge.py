#!/usr/bin/env python

def __main__():
        import ccuapi, optparse, sys, os

        PURGE_TYPES =   ['arl', 'cpcode']

        parser      =   optparse.OptionParser()
        parser.add_option('-d', '--domain', help = "Where to purge from, 'production' or 'staging'")
        parser.add_option('-u', '--urls', help = "Path to a file of URLs or CP Codes to purge, one per line.")
        parser.add_option('-e', '--email', help = "Email addresses (comma-separated) to notify when purge is complete.")
        parser.add_option('-t', '--type', help = "The type of purge to perform. Choose from 'arl' or 'cpcode'")
        parser.add_option('--username', help = "Akamai username to use.")
        parser.add_option('--password', help = "Akamai password to use.")

        opts, args  =   parser.parse_args()
        urls        =   []
        kwargs      =   {}

        if opts.urls:
            urls    =   open(opts.urls).read().strip().split("\n")
            
        if not len(urls) and len(args):
            urls    =   args
            
        if not len(urls):
            print "You must specify at least one URL or CP Code to purge."
            sys.exit(os.EX_NOINPUT)
            
        if opts.email:
            kwargs['email']     =   opts.email
        if opts.username:
            kwargs['username']  =   opts.username
        if opts.password:
            kwargs['password']  =   opts.password
        if opts.type:
            kwargs['kind']      =   opts.type
        if opts.domain:
            kwargs['domain']    =   opts.domain


        purger      =   ccuapi.purge.PurgeRequest(**kwargs)
        purger.add(urls)
        results     =   purger.purge()
        for result in results:
            if result[0].resultMsg == "Success.":
                print '%d URL[s] or CPcode[s] will be purged within %d minutes' % (result[1], result[0].estTime / 60)
            else:
                print 'There was an error making the purge request: %s' % result[0].resultMsg if 'resultMsg' in result[0] else 'unknown error.'
