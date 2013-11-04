#!/usr/bin/env python
import memcache
import time
import socket

# Settings
MEMCACHE_SERVER = '127.0.0.1'
MEMCACHE_PORT = '11211'
CARBON_PORT = '2003'
CARBON_SERVER = '127.0.0.1'
CARBON_PREFIX = 'stats.memcache.%s' % unicode(MEMCACHE_SERVER)

def main():
    try:
        mc = memcache.Client(MEMCACHE_SERVER:MEMCACHE_PORT], debug=0)
        all_stats = mc.get_stats()
    except Exception, ex:
        print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()), 'Memcache connect error: '
        print str(ex)
        sys.exit(1)

    for node_stats in all_stats:
        server, stats = node_stats
        host = server.split(':')[0]
        for stat in stats:
             message = '%s.%s %s %d\n' % \
                  (unicode(CARBON_PREFIX), unicode(stat),  unicode(stats[stat]), int(time.time()))

             try:
                  sock = socket.socket()
                  sock.connect((CARBON_SERVER, CARBON_PORT))
                  sock.sendall(message)
                  sock.close()
             except Exception, ex:
                  print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()), 'Carbon connect error: '
                  print str(ex)
                  sys.exit(1)

if __name__ == '__main__':
    main()
