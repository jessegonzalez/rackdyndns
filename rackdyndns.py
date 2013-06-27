#!/usr/bin/env python

import settings
import sys
import urllib

import pyrax
import pyrax.exceptions as exc


def get_ip():
    ip = None
    response = urllib.urlopen(settings.curlip)

    if response.getcode() != 200:
        print "ERROR: %(code)d response code from %(ipurl)s" % \
            {'code': response.getcode(), 'ipurl': settings.curlip}
        sys.exit(1)
    else:
        ip = response.read().rstrip()
        print "Our current ip address is %s" % ip

    return ip


def update_records(ipaddress='127.0.0.1'):
    pyrax.set_setting("identity_type", "rackspace")
    pyrax.set_credentials(settings.username, settings.apikey)
    dns = pyrax.cloud_dns

    try:
        domain = dns.find(name=settings.domain)
    except exc.NotFound:
        print "ERROR: DNS information not found for %s." % settings.domain
        sys.exit(1)

    for record in settings.records:
        print 'Updating or creating record: %s...' % record,

        try:
            record_response = domain.find_record('A', name=record)
            record_response.update(data=ipaddress)
            print 'updated.'
        except exc.DomainRecordNotFound:
            _record = {"type": "A", "name": record, "data": ipaddress}
            domain.add_record(_record)
            print 'created.'

if __name__ == '__main__':
    ip = get_ip()

    if ip:
        update_records(ipaddress=ip)
