
#
# simple test program
#
# $Id$
#

import async
import ex1
import socket
import sys
import posix

def cb(err,res):
    print "err=", err, "& res=", res
    print "Calling exit"
    async.core.exit ()
    print "after exit!!"

def cb2(err, foo):
    if err == 0:
        foo.warn ()
    else:
    	print "error / bad result:", err

#
# make call a function, so that way we can test the refcounting on 
# args to arpc.call calls.  if we called from main, then we would
# never see f being dealloced (since main will always have a reference
# to it)
#
def call(cli):
    f = ex1.foo_t ()
    f.x = 'this is a test string'
    f.xx = 1010
    cli.call (ex1.FOO_FUNC, f, cb)

def call2(cli):
    bar = ex1.bar_t ()
    bar.y = [1,2,3,4,5,'shit']
    cli.call (ex1.FOO_BAR, bar, cb2)

def call3(cli):
    z = ex1.bb_t ()
    z.aa = ex1.A2;
    z.b.foos = [ex1.foo_t () for i in range(0,2) ]
    z.b.foos[0].x = "foos[0] = 4"
    z.b.foos[0].xx = 4
    z.b.foos[1].x = "foos[1] = 5"
    z.b.foos[1].xx = 5
    z.b.bar.y = [ 100, 200, 300, 400 ];
    z.warnx ()
    cli.call (ex1.FOO_BB, z, cb)

def call4(cli):
    z = ex1.fooz_t ()
    z.baz.alloc ()
    z.baz.p = ex1.baz_t ()
    z.baz.p.foos = [ex1.foo_t () for i in range (0,2) ]
    z.baz.p.foos[0].x = "foos[0] = 4"
    z.baz.p.foos[0].xx = 4
    z.baz.p.foos[1].x = "foos[1] = 5"
    z.baz.p.foos[1].xx = 5
    z.baz.p.bar.y = [ 100, 200, 300, 400 ];
    z.warnx ()
    cli.call (ex1.FOO_FOOZ, z, cb)

def call5(cli):
    z = ex1.fooz_t ()
    f = ex1.foo_t ()
    f.x = "this is a test string"
    f.xx = 4080
    z.b = f.xdr2str ()
    z.warnx ()
    cli.call (ex1.FOO_FOOZ, z, cb);

    

port = 3000
if len (sys.argv) > 1:
    port = int (sys.argv[1])


sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.connect (('127.0.0.1', port))
fd = sock.fileno ()

x = async.arpc.axprt_stream (fd, sock)
cli = async.arpc.aclnt (x, ex1.foo_prog_1 ())

call5 (cli);

async.util.fixsignals ()
async.core.amain ()

