import os, sys
import qb

hosts = qb.hostorder()
for host in hosts:
    name = host['name']
    address = host['address']
    status = host['state']
    string = '%s | %s | Status: %s' % (name, address, status)
    print string
    print host['resources']
    print "---"