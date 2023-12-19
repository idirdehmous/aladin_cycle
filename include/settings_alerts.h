
#module load  ecflow/5.8.1
# TASKS ERROR CODES 
#case @TASK@  in  
#    "check_first_guess")   ERR_CODE="A-101" ;; 
#    "get_obs"          )   ERR_CODE="A-102" ;;
#    "bator"            )   ERR_CODE="A-103" ;;
#    "odb_merge"        )   ERR_CODE="A-104" ;;
#    "addfields"        )   ERR_CODE="A-105" ;;
#    "screening"        )   ERR_CODE="A-106" ;;
#    "minimisation"     )   ERR_CODE="A-107" ;;
#    "retrieve_lbc"     )   ERR_CODE="L-201" ;;
#    "prep_sfx"         )   ERR_CODE="L-202" ;;
#    "integration"      )   ERR_CODE="F-301" ;; 
#    "be87_l"           )   ERR_CODE="P-401" ;; 
#esac  


declare  -A  issue
# ASSIMILATION 
issue["A-101"]="MISSING FIRST GUESS"
issue["A-102"]="BUFR FILE NOT FOUND"
issue["A-103"]="NO ODB PRODUCED"
issue["A-104"]="NO DATA IN ODB, CAN'T RUN MINIMISATION"
issue["A-105"]="MISSING FIRST LBC"
issue["A-106"]="MISSING FIRST GUESS"
issue["A-107"]="ECMA ODB MISSING FOR CANARI"
issue["A-108"]="UNKNOWN OBSERVATION SOURCE. POSSIBLE VALUES: gts OR mars"
issue["A-109"]="SURFEX-ENABLED, BUT SURFEX FIRST GUESS NOT FOUND"
issue["A-110"]="MISSING BUFR FILE FROM ECMWF"
issue["A-111"]="LBC MISSING FOR SST UPDATE"
issue["A-112"]="PREVIOUS CANARI ANALYSIS NOT AVAILABLE:  Coldstart"
issue["A-113"]="1st CLIM FILE NOT AVAILABLE FOR CANARI"
issue["A-114"]="2nd CLIM FILE NOT AVAILABLE FOR CANARI"
issue["A-115"]="MASTERODB:: CANARI ANALYSIS NOT PRODUCED"
issue["A-116"]="MASTERODB:: OI-Main ANALYSIS(.sfx) FAILED"
issue["A-117"]="MISSING UPPER-AIR BUFR FILE FROM ECMWF"
issue["A-118"]="LBC MISSING TO ADD ISBA"
issue["A-119"]="MASTERODB:: PROBLEM IN ADDING ISBA FIELDS"
issue["A-120"]="MISSING FIRST GUESS FOR SCREENING"
issue["A-121"]="MASTERODB:: PROBLEM IN RUNNING SCREENING"
issue["A-122"]="MASTERODB:: PROBLEM IN RUNNING MINIMISATION"
issue["A-123"]="CCMA ODB MISSING FOR SCREENING"
issue["A-124"]="CCMA ODB MISSING FOR MINIMISATION"
issue["A-125"]="BLENDSUR:: FAILED TO RUN SST UPDATE"

# LBC 
issue["L-201"]="INPUT LBC NOT FOUND"
issue["L-202"]="FIRST LBC NOT FOUND"
issue["L-203"]="LBC FILE NOT FOUND IN ACQUISITION DIRECTORY"
issue["L-204"]="LBC FILE NOT FOUND IN ARCHIVE"
issue["L-205"]="FIRST LBC FOR SFX NOT FOUND"
issue["L-206"]="FAILED TO PRODUCE THE SURFEX LBC"
issue["L-207"]="FAILED TO PRODUCE THE LBC FROM ARPEGE"
issue["L-208"]="LBC NOT YET AVAILABLE"

# FORECAST 
issue["F-301"]="LBC NOT FOUND"
issue["F-302"]="MISSING UPPER-AIR ANALYSIS"
issue["F-303"]="WARNING  !: SKIPPING_CANARI, FORECAST RUNNING WITH FIRST GUESS AS INIT FILE"
issue["F-304"]="ANALYSIS NOT FOUND IN ARCHIVE"
issue["F-305"]="MASTERODB:: PROBLEM IN RUNNING FORECAST"


# POST 
issue["P-401"]="OUTPUT FILE NOT PRODUCED"


# FUNCTIONS 
function ClearAlert () {
# NOTE: add " || ." so it doesn't fail if there are no labels
  ecflow_client --alter=delete label ERROR_CODE  @ECF_NAME@ || :
  ecflow_client --alter=delete label ERROR_INFO  @ECF_NAME@ || :
}


function SuiteAlert ()  {
  NodePath=$1
  ErrCode=$2

# DATE TIME 
  dd=$(date -u  +%Y-%m-%d )
  hh=$(date -u  +%H:%M:%S )
  DateTime=$dd" "$hh
  ecflow_client --alter=add  label ERROR_CODE ${ErrCode}  ${NodePath}
  ecflow_client --alter=add  label ERROR_INFO "${issue[${ErrCode}]}"  ${NodePath}
}


function InfoAlert ()  {
  ERR_CODE=$1
  if [ @SUITE_ALERTS:yes@ == "yes" ] ; then 
     SuiteAbort  @ECF_NAME@  ${ERR_CODE} 
  fi
}

function InfoAbort ()  {
  ERR_CODE=$1
  if [ @SUITE_ALERTS:yes@ == "yes" ] ; then 
     SuiteAlert  @ECF_NAME@  ${ERR_CODE} 
  fi  
  exit 123
}

#function TaskAbort() {
#NodePath=$1
#ErrCode=$2
#ecflow_client   --alter add  label ERROR_CODE ${ErrCode}               ${NodePath} 
#ecflow_client   --alter add  label INFO       ${issues[${ErrCode}]}    ${NodePath}

#}

# clear labels at start of script
ClearAlert
sleep 5

