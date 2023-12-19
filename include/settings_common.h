# main settings
# make all output etc. readable to others
umask 0022 

USER=@USER@
SUITE=@SUITE@
SCHOST=@SCHOST@
BASEDIR=@BASEDIR@

#host=`echo ${HOSTNAME,,} | cut -f1 -d'.' ` # requires bash >= 4
host=`echo "$HOSTNAME" | tr '[:upper:]' '[:lower:]' | cut -f1 -d'.' `

@include <settings_functions.h>

CYCLE_INC=@CYCLE_INC@
RUNMODE=@MODE:exp@ # oper | exp | tc
REALTIME=$(boolean @REALTIME:no@)
DELAY=$(boolean @DELAY:no@) # set to yes if running in delayed mode
  # this turns off date-checking and gets LBC's from RECENT archive
  # FIXME: better let $DELAY depend directlty on RUNDATE and real date
  #       the macro should mainly be used in triggers only

RUNDATE=@RUNDATE:""@
MAIL_LIST=@MAIL_LIST:@

set -x

