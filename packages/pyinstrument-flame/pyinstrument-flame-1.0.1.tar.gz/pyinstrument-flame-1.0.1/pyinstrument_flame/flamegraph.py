import pyinstrument
import os
import subprocess


flamegraphpl = os.path.join(os.path.dirname(__file__), "vendor", "flamegraph.pl")

def flamegraph(session, params):
    p = subprocess.Popen(['/usr/bin/perl', flamegraphpl, *params], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    for stack, t in session.frame_records:
        line = "{} {}\n".format(";".join(frame.replace("\x00", ":") for frame in stack), t * 1000000).encode('utf-8')
        p.stdin.write(line)

    stdout, _ = p.communicate()

    return stdout.decode('utf-8')



