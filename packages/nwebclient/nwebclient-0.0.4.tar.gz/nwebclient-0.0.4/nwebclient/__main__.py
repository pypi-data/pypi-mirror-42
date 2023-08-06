
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", help="increase output verbosity", default=False)
parser.add_argument("-s", type=int, help="display a square of a given number")
parser.add_argument("-param1", help="echo the string you use here", default="")
parser.add_argument("op", help="Operation (setup)")

args = parser.parse_args()

def setup():
  print "Execute Setup"
  import os
  os.system("curl https://bsnx.net/d/nweb-install.sh | /bin/bash")  

if args.v:
    print "verbosity turned on"

print "+----------------------+"
print "| nweb client main     |"
print "+----------------------+"

if args.op == "setup":
  setup()
else:
  print "Unknown Operation"
  print "OP:" + args.op
  print args.param1

