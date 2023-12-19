# main settings
# make all output etc. readable to others
umask 0022 

DELAY=$(boolean @DELAY:no@) # set to yes if running in delayed mode
REALTIME=$(boolean @REALTIME:no@)

RUNDATE=@RUNDATE:""@
DOMAIN=@DOMAIN@
CNMEXP=@CNMEXP@
HOURRANGE=@FCLEN:0@
NLEVELS=@NLEVELS@
TIMESTEP=@TIMESTEP@

# basic model switches
MODEL=@MODEL@  # arome | alaro
SURFACE=@SURFACE@ # isba | surfex
HYDROSTATIC=$(boolean @HYDROSTATIC@)
DFI=$(boolean @DFI:yes@)
ASSIMILATION=$(boolean @ASSIMILATION:yes@)
if [[ $ASSIMILATION == yes ]] ; then
  ASSIM_UPPER=@ASSIM_UPPER:none@
  ASSIM_SURFACE=@ASSIM_SURFACE:none@
  COLDSTART=@COLDSTART:yyyymmddhh@
  OBSTYPES="@OBSTYPES: @"
  ASSIM_LABEL=@ASSIM_LABEL:""@ # are we in surface or upper?
else
  ASSIM_UPPER=none
  ASSIM_SURFACE=none
fi
OBS_NPOOL=@OBS_NPOOL:4@

# IO server (forecast only)
NPROC_IO=@NPROC_IO:0@
if [[ $NPROC_IO -gt 0 && @TASK@ == "integration" ]] ; then
  IO_SERVER=yes
else
  IO_SERVER=no
fi

# Climate files
PGD_FILE=@PGD_FILE:${DOMAIN}_PGD_2L.fa@

# boundary conditions:
COUPLING=@COUPLING:none@ # meaning may depend on type of suite
LBC_INC=@LBC_INC@
COUPLING_DOMAIN=@COUPLING_DOMAIN@
DFI_CPL=@DFI_CPL:${LBC_INC}@

@include <settings_namelists.h>

set -x

