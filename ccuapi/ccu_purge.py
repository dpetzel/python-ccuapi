#!/usr/bin/env python
"""
Command line interface to Akamai's CCU API
"""


# pylint: disable=too-many-locals, too-many-branches, too-many-statements
def main():
    """
    Main entry point for CLI interactions
    """
    import optparse  # pylint: disable=deprecated-module
    import sys
    import os
    import logging

    from .purge import PurgeRequest
    from .exceptions import AkamaiAuthorizationException
    from .exceptions import AkamaiCredentialException

    parser = optparse.OptionParser()
    parser.add_option('-d', '--domain',
                      help="Where to purge from, 'production' or 'staging'")
    parser.add_option('-u', '--urls',
                      help="Path to a file of URLs or CP Codes to purge,"
                      " one per line.")
    parser.add_option('-e', '--email',
                      help="Email addresses (comma-separated) to notify when"
                      " purge is complete.")
    parser.add_option('-t', '--type', choices=['arl', 'cpcode'], default='arl',
                      help="The type of purge to perform. Choose from"
                      " 'arl' or 'cpcode'")
    parser.add_option('--username', help="Akamai username to use.")
    parser.add_option('--password', help="Akamai password to use.")
    parser.add_option('--api-host',
                      help='Overrides the host where purge requests are send.')
    parser.add_option("--api-host-certificate",
                      help="Path to CA_BUNDLE file to use for SSL "
                           "certification, when making requests to API host")
    parser.add_option("-v", '--verbose', action="store_true", dest="verbose")

    opts, args = parser.parse_args()

    if opts.verbose is True:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Initialize the logger tailored for console output
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    urls = []
    kwargs = {}

    if opts.urls:
        urls = open(opts.urls).read().strip().split("\n")

    if not len(urls) and len(args):
        urls = args

    if not len(urls):
        logger.error("You must specify at least one URL or CP Code to purge.")
        sys.exit(os.EX_NOINPUT)

    if opts.email:
        kwargs['email'] = opts.email
    if opts.username:
        kwargs['username'] = opts.username
    if opts.password:
        kwargs['password'] = opts.password
    if opts.api_host:
        kwargs['api_host'] = opts.api_host
    if opts.api_host_certificate:
        kwargs['certificate'] = opts.api_host_certificate
    if opts.type:
        kwargs['kind'] = opts.type
    if opts.domain:
        kwargs['domain'] = opts.domain

    try:
        purger = PurgeRequest(**kwargs)  # pylint: disable=bad-option-value
        purger.add(urls)
        purger.purge()
    except AkamaiAuthorizationException:
        logger.error(
            "An authorization error was encountered while attempting to"
            " purge one ore more URLs. It appears your username and password"
            " are correct, however you may not have permissions to purge"
            " one or more URLs/CP Codes.")
        sys.exit(os.EX_NOPERM)
    except AkamaiCredentialException:
        logger.error("You failed to supply a valid user name or password.")
        sys.exit(os.EX_CONFIG)

    if purger.http_status == 201:
        time_until_complete = purger.estimated_seconds / 60
        logger.info(
            "%s URL(s) or CPcode(s) will be purged within %s minutes."
            " If you have any issues refer to Akamai support ID %s",
            len(purger.urls), time_until_complete, purger.support_id)
    else:
        reason = getattr(purger, 'detail', 'unknown')
        logger.error("Purge failed with reason: %s", reason)
        exit(1)

if __name__ == "__main__":
    main()
