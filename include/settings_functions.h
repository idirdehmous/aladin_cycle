#####################
# utility functions #
#####################

function show_warning {
  local message=$1
  local wpath=${2:-""}
  if [[ $wpath == "" ]] ; then
    wpath="/@SUITE@ /@SUITE@/cycle/@THIS_RUN@"
  fi
  for wp in $wpath; do
    clear_warning $wp
    ecflow_client --alter=add label WARNING "$message" $wp > /dev/null 2>&1 || :
  done
}

function clear_warning {
  local wpath=${1:-/@SUITE@}
  # make sure the command doesn't fail if there is no current warning
  ecflow_client --alter=delete label WARNING $wpath > /dev/null 2>&1 || :
}


function complete_and_exit {
  # when completing a task early (i.e. without getting to tail.h)
  # in fact you could call this function at the end of 
  # every task in stead of including head.h
  # OR: just replace it by include tail.h ?
  if [[ $1 != "" ]] ; then
    echo "complete_and_exit: $1"
  fi
@include <tail.h>
#  TASK_FINISH_TIME=`date -u +"%Y-%m-%d %H:%M:%S"`
#  echo "===== TASK STARTED:  ${TASK_START_TIME:-unknown} ====="
#  echo "===== TASK FINISHED: ${TASK_FINISH_TIME:-unknown} ====="

#  ecflow_client --complete
#  trap 0
#  exit 0
}

function boolean {
  # returns a standard string value
  # that can be evaluated directly
  case $1 in
    y|yes|Y|YES|true|T|1) echo yes ;;
    n|no|N|NO|false|F|0) echo no ;;
    *) echo "not a boolean" ; exit 1 ;;
  esac
}
# if you return true|false you can do "if $(boolean $x) ; then ..."
# but yes/no may be a bit more common in scripting?

# return workdir for a certain cycle date
# useful to e.g. address the previous cycle's output for nesting
function workdir {
  local fcdate=${1:-$RUNDATE}
  local basedir=${2:-$BASEDIR}

  local fcRR=`echo $fcdate | cut -c 9-10`
  echo $basedir/work/run_$fcRR
}

##############################################
# extract date and lead time from an FA file #
##############################################

# uses the very simple fa_checkdate python script

function fa_rundate {
  local fafile=$1
  echo `fa_checkdate $fafile | cut -d"+" -f1`
}

function fa_leadtime {
  local fafile=$1
  echo `fa_checkdate $fafile | cut -d"+" -f2`
}

function fa_validdate {
  local fafile=$1
  local fadate=`fa_checkdate $fafile`
  local yyyymmdd=`echo $fadate | cut -c 1-8`
  local rr=`echo $fadate | cut -c 9-10`
#  local rundate=`echo $fadate | cut -d+ -f1`
  local ldt=`echo $fadate | cut -d+ -f2`
  echo `date -u -d "$yyyymmdd ${rr} +$ldt hours" +%Y%m%d%H`
}



