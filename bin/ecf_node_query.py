#! /usr/bin/env python3
#import sys
#import os
import ecflow
import argparse

parser = argparse.ArgumentParser(prog="ecf_query")
parser.add_argument("path", metavar="/path/to/node" )

action = parser.add_mutually_exclusive_group()
action.add_argument('-v', metavar='variable') 
action.add_argument('-l', metavar='label') 
action.add_argument('-e', metavar='event') 
action.add_argument('-r', help='current repeat value', const=True, default=False, action="store_const") 
action.add_argument('-nl', help='list of sub-nodes', const=True, default=False, action="store_const") 
action.add_argument('-ns', help='state of sub-nodes', const=True, default=False, action="store_const") 
action.add_argument('-m', help='meter') 
action.add_argument('-s', help='node state', const=True, default=False, action="store_const") 

args = parser.parse_args()

# we take the ECF_HOST and ECF_PORT from environment
ci = ecflow.Client()
ci.sync_local()
defs = ci.get_defs()
try :
  node = defs.find_abs_node(args.path)
except :
  print("Node not found")


# TODO: if result is empty, this could mean "not defined" or "empty"
if node is None :
  # the node does not exist
  result = None
elif not args.v is None :
  result = node.find_variable(args.v).value()
elif not args.e is None :
  result = node.find_event(args.e).value()
elif not args.l is None :
  result = node.find_label(args.l).value()
elif not args.m is None :
  result = node.find_meter(args.m).value()
elif args.nl :
  result = " ".join([ p.name() for p in node.nodes ])
elif args.ns :
    result = " ".join([ p.name()+":"+p.get_state().name for p in node.nodes ])
elif args.r :
  result = node.get_repeat().value()
else :
  result = node.get_state().name

print(result)

