#! /bin/bash
suite=$(basename `pwd`)
inifile=${1:-${suite}.ini}

echo " -> python node_runner.py $inifile"
python3 python/node_runner.py $inifile || {
  echo "Could not run node_runner.py"
  exit 1
}


