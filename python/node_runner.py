#! /usr/bin/env python3
"""
## Node Runner
## Authors: Alex Deckmyn & Idir Dehmous
## TODO:
## ... a lot :-)
"""
from ecflow import * 
import os
import sys
import importlib
import configparser
from nr_modules.suite_config import nr_suite_config

# get init file from command line
# > python node_runner.py oper.ini
nargv = len(sys.argv)
if nargv > 1 :
  ini_file = sys.argv[1]
  if not os.path.exists(ini_file) :
    print("File " + ini_file + " not found.")
    exit(1)
else :
  print("You need to provide a <suite>.ini file!\n")
  print("Usage:")
  print("> python node_runner.py <suite>.ini\n")
  exit(1)


# NOTE: suite_name MUST be equal to the path
#       so you can take "pwd" as suite_path
#       THIS ONLY WORKS IF YOU RUN NODERUNNER FROM THE BASE DIRECTORY!
#suite_path = os.getcwd() # BUG: on ATOS this now returns the "real" path to /home -> error for ecflow server
suite_path = os.getenv("PWD")

###############

# ATTENTION: "configparser" reads unicode by default
#   so this can be problematic with python2 (a lot of str() needed!)
#   but using python2 ConfigParser is less flexible
#   we prefer to use the back-ported configparser from py3
#   When using ConfigParser (py2): no indentation allowed

config=configparser.ConfigParser()
# keep key names in upper case
config.optionxform = str
config.read(ini_file)

if os.path.exists("local.ini") :
  print("Additional settings found in local.ini")
  config.read("local.ini")

####################
# read config file #
####################

suite_config = nr_suite_config(suite_path, config)
def_file = '{0}.def'.format(suite_config.suite_name)
print(( "\n" +
        "NodeRunner               : creating suite {1}\n" +
        "ini file used            : {0}\n" +
        "definition file location : {2}"
        ).format(ini_file, suite_config.suite_name, def_file))

##############################
# start the suite definition #
##############################

defs = Defs()
suite = defs.add_suite(suite_config.suite_name) # we just call the variable "suite"...

#######################
### Suite variables ###
#######################

# main
variables = { 
  "ECF_MICRO":"@",
  "MODE":suite_config.mode,
  "CYCLE_INC":str(suite_config.cycle_inc),

  }
suite.add(Edit(variables))

# JOB SUBMISSION etc. #
suite.add(Edit(suite_config.platform))

### variables for PBS/user/ecFlow/hpc...
directories = {
  "ECF_INCLUDE":suite_config.suite_path + "/include",
  "ECF_FILES":suite_config.suite_path + "/scr",
  "ECF_HOME":suite_config.local_temp,
  "SUITE_DATA":suite_config.suite_path + "/data"     # this is used for sync'ing them to HPC
  }
suite.add(Edit(directories))

# the default "USER"@"SCHOST" is the HPC account
suite.add_variable(suite_config.jobs["hpcjob"])
default_job = {
  "NODE_SELECT":"@SELECT_SERIAL@",
  "WALLTIME":"0:05:00"
  }

suite.add_variable(default_job)

# .ini sections that are directly converted to ecflow variables:
section_list = ["settings", "local", "tasks"]
if suite_config.suite_type in [ "forecast_cycle", "Bmatrix" , "case_runner"] :
  section_list += ["model", "coupling"]

for section in section_list :
  # TODO: check all entries? default values?
  if section in config.sections() :
    x = config.items(section)
    xd = { str(y[0]):str(y[1]) for y in x }
    suite.add_variable(xd)
# FIXME: such limits should be defined somewhere else (platform?)
if suite_config.has_forecast :
  suite.add_limit("max_postproc", suite_config.max_postproc)

# never allow two main "init sync" tasks at the same time!
suite.add_limit("max_init", 1)
# never allow two main "sync scratch" tasks at the same time!
suite.add_limit("max_sync", 1)

# assimilation settings:
suite.add(Edit(suite_config.assim_var))

# The SCHOST label is useful
suite.add_label("SCHOST", suite_config.hpc_host)

# ECMWF Time Critical suites:
if config.has_option("settings", "STHOST") :
  suite.add_label("STHOST", str(config.get("settings", "STHOST")))

########################
# BUILD THE FULL SUITE #
########################

suite_def = importlib.import_module("nr_modules.suite.nr_suite_" + suite_config.suite_type)
suite_def.build_suite(suite, suite_config, config)

######################################
# operational use: external triggers #
######################################
# "True" means: remove existing extern definitions first, then scan the suite
defs.auto_add_externs(True)

#######################
### write .def file ###
#######################
defs.save_as_defs(def_file)

