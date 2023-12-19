NODE-RUNNER
===========

Node Runner is a project for creation of ecFlow suites for ACCORD forecast cycle (arome or alaro, with or without assimilation). It can also create special suites for e.g. B-matrix creation, case re-runs etc.

Developers: Alex Deckmyn, Idir Dehmous
Contributors: Michiel Vanginderachter, Daan Degrauwe, Lesley de Cruz a.m.o.

main documentation is in doc/node\_runner.md

UPDATING A SUITE
================

If there is a change in executables, clim files or other STATIC data, the data directories $TCWORK/STATIC should be updated, not the suites themselves.

1. > cd /home/<user>/ECF/SUITE
2. > git pull

If the changes are only in the include files (\*.h), scripts (\*.ecf)  or namelists, nothing else needs to be done. The new version will be used in the next cycle.

However, if  are changes in the suite structure or in the .ini file, more steps are needed.

3. > ./compile\_suite.sh  
This is in essence just a wrapper for  
*python3 python/node_runner.py SUITE.ini*

At this point, the file SUITE.def is replaced, but the new version is not yet implemented in the suite itself. That can be done in a few ways. For convenience, there is a shell script **update\_suite.sh** which attempts to updated the whole suite and keep track of which parts were already completed.
4. > ./update\_suite.sh

You can also do it manually with ecflow\_client:  
- *ecflow_client --replace /<SUITE> <SUITE>.def*  
This will replace the whole suite. In some cases it may be safer to replace only a part, e.g.  
- *ecflow_client --replace /SUITE/lagged/00 SUITE.def*  
will only replace the 00 family of the lagged family tasks.

**WARNING:** When replacing (part of) a suite in this way, all nodes go back to the default state, which is normally "queued". So if e.g. the 00 cycle had already finished before the change, it should be set complete manually, e.g.  
> ecflow\_client --force=complete recursive /SUITES/cycle/00


**WARNING:** If some variables (macro's) and labels in the suite were manually adapted, they will be reset to the value in the definition file! This may be a desired effect or not. For TC suites, two variables that must be set correctly are **STHOST** and **SCHOST**. Normally, **update\_suite.sh** should correctly preserve the last value.


Some helpful commands
=====================

- manually changing SCHOST or STHOST:
ecflow\_client --alter=change variable STHOST ws1 /<SUITE>
ecflow\_client --alter=change label STHOST ws1 /<SUITE>

- manually changing trigger time of a cycle:
ecflow\_client --alter=delete time /arome/cycle/21
ecflow\_client --alter=add time 03:30 /arome/cycle/21


