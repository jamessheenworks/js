
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('arg',nargs='+')
args = parser.parse_args()
arg = args.arg

for i in arg:
  pass

