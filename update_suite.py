#! /usr/bin/env python3
import sys
import os
import ecflow
import argparse

pwd = os.getenv("PWD")
suite_name = os.path.basename(pwd)
deffile = pwd + "/" + suite_name + ".def"

print("--> replacing: \n      suite {0}\n      {1}\n".format(suite_name, deffile))

ci = ecflow.Client()
ci.sync_local()
defs = ci.get_defs()

#
suite = defs.find_suite(suite_name)
spath = "/" + suite_name

if suite is None :
    print("Suite {0} not loaded yet. Initialising.".format(suite_name))
    ci.load(deffile)
    ci.begin_suite(suite_name)
    sys.exit(1)

# TODO: suspend the suite for the duration of this replacement
#       to make sure it doesn't re-activate too soon

# The actual replacement
# NOTE: this will fail is any task is active
try:
    ci.replace(spath, deffile)
except RuntimeError as e :
    print(str(e))
    sys.exit(1)

# NOTE: we use the fact that "defs" still holds the old situation!
# update the basics
for var in [ "STHOST", "SCHOST" ] :
    varn = suite.find_variable(var)
    if not varn.empty() :
        val = varn.value()
        print("{0} = {1}".format(var, val))
        try:
          ci.alter(spath, "change", "variable", var, val)
        except:
          print(f"WARNING: new suite no longer has variable {var}")

# now set the completed cycles back to "complete"
for fam in ["cycle", "lagged" ] :
    fnode = suite.find_node(fam)
    if not fnode is None :
        rep = fnode.get_repeat()
        if rep.empty() :
            print("%s does not have a repeat. Check RUNDATE."%fam)
            # so probably a "looping" suite

        else :
          rundate = str(rep.value())
          print(fam + " rundate: " + rundate)
          # NOTE: may fail if date is not in range
          try: 
              ci.alter(spath + "/" + fam, "change", "repeat", rundate)
          except RuntimeError as e:
              print(str(e))
              print("WARNING: date was not reset!")
              pass

        cycle_list = { p.name():p.get_state().name for p in fnode.nodes }
        print(fam + " status:")
        print(cycle_list)

        completed = [ rr  for rr,ss in cycle_list.items() if ss == "complete" ]
        for cc in completed :
            cname = "/".join([suite_name, fam, cc])
            ci.force_state_recursive(cname, ecflow.State.complete)

# TODO: suites without cycle rundate are possibly "looping" suites
#       there, you must reset the RUNDATE variable

<<<<<<< HEAD

=======
>>>>>>> db99495... Fix update_suite.py for no-STHOST suites
