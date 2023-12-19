#! /bin/bash
# ATTENTION: only run this once!
suite=$(basename `pwd`)

[ -e ${suite}.def ] || {
  echo "${suite}.def not found"
  echo "run compile_suite.sh first!"
  exit
}

# check if the suite already exists
ecflow_client --get /$suite > /dev/null 2>&1
if [ $? ] ; then
  echo "Suite does not exist yet. Initialising."
  echo "  Loading ${suite} into ecflow. "
  ecflow_client --load ${suite}.def
  echo "  Beginning ${suite} "
  ecflow_client --begin $suite
else
  echo "Suite already exists. Running update_suite.sh"
  ./update_suite.sh
fi
