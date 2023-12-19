from ecflow import *
import os
#import pwd
import configparser
import datetime
import importlib

def estimate_walltime(fclen, ncores, factor) :
  # in minutes: fclen (in h) * factor / #ncores
  # this is just a rough estimate based on "perfect scaling"
  # transform to "hh:mm:ss" string
  # add 10' for DFI etc.
  return str(datetime.timedelta(minutes=fclen * factor / ncores + 10))

class nr_suite_config :
  def __init__(self, suite_path, config):
    # if the suite config.ini has a hard-coded path, use that rather than PWD
    self.suite_name = config.get('suite', 'name', fallback=os.path.basename(os.getcwd()))
    if os.getenv('NR_SUITE_PATH') :
        self.suite_path = os.getenv('NR_SUITE_PATH') + "/" + self.suite_name
    else :
        self.suite_path = config.get('suite', 'suite_path', fallback=suite_path)
    self.config = config
    self.local_temp = self.suite_path + "/tmp"
    self.local_bin  = self.suite_path + "/bin"
    self.userid = os.getuid()
    self.username = os.environ["LOGNAME"]
#    self.username = os.getlogin()   # fails on e.g. ecgate
#    self.username = pwd.getpwuid(self.userid)[0]

    # PLATFORM
<<<<<<< HEAD
    # we could simply load "all entries"
    # but doing each seperately allows for default values...
    self.localhost = str(config.get("platform", "localhost", fallback = "localhost"))
    self.platform = {
            "HEAD":str(config.get("platform", "HEAD",
                fallback = "head.h")).strip(),
            "TAIL":str(config.get("platform", "TAIL",
                fallback = "tail.h")).strip(),
            "HPC_HEADER":str(config.get("platform", "HPC_HEADER",
                fallback = "slurm.h")).strip(),
            "ENV_ALADIN":str(config.get("platform", "ENV_ALADIN")).strip(),
=======
    self.localhost = str(config.get("platform", "localhost", fallback = "localhost"))
    self.platform = {
            "PLATFORM":str(config.get("platform", "PLATFORM", fallback = "default")).strip(),
            "HPC_HEADER":str(config.get("platform", "HPC_HEADER",
                fallback = "slurm.h")).strip(),
>>>>>>> 7b69f59... update ATOS ini files
            "ECF_JOB_CMD":str(config.get("platform", "ECF_JOB_CMD",
                fallback = "@ECF_JOB@ 1>@ECF_JOBOUT@ 2>&1")).strip(),
            "ECF_KILL_CMD":str(config.get("platform", "ECF_KILL_CMD",
                fallback = "kill -15 @ECF_RID@")).strip(),
            "ECF_STAT_CMD":str(config.get("platform", "ECF_STAT_CMD",
                fallback = "ps --pid @ECF_RID@ -f > @ECF_JOB@.stat 2>&1")).strip()
            }
    # SUITE
    self.mode = str(config.get("suite", "suite_mode", fallback="exp")).strip()
<<<<<<< HEAD
#    self.delay_mode = config.getboolean("suite", "delay_mode", fallback = False)
=======
    self.delay_mode = config.getboolean("suite", "delay_mode", fallback = False)
>>>>>>> 7b69f59... update ATOS ini files
    self.wait_mode = config.getboolean("suite", "wait_mode", fallback = False)
    self.suite_type = config.get("suite", "suite_type", fallback="forecast_cycle")
    self.realtime = config.getboolean("suite", "realtime", fallback="no")

    self.hpc_host = str(config.get("settings", "SCHOST")).strip()
    self.hpc_user = str(config.get("settings", "HPC_USER", fallback=self.username)).strip()
#    self.scratch = str(config.get("settings", "SCRATCH")).strip()
    self.has_cycle = (("cycle" in config.sections()) and
                     config.getint("cycle", "cycle_inc", fallback=0) > 0)

    if self.realtime :
      bd_default = datetime.date.today().strftime("%Y%m%d")
    else :
      bd_default = "00000000"

    if self.has_cycle :
      self.begindate = str(config.get("suite", "begindate", fallback=bd_default))
      self.enddate = str(config.get("suite", "enddate", fallback="20301231"))
      self.cycle_inc = config.getint("cycle", "cycle_inc")
      self.ncycle = 24 // self.cycle_inc
      # try to make sure that trigger_labels has the correct length (ncyles)
      default_labels = ",".join([ "%02i"%hh for hh in range(0, 24, self.cycle_inc) ])

      self.trigger_labels = list(map(str.strip, str(config.get("cycle", "trigger_labels", fallback=default_labels)).split(",")))
      self.cycle_labels = list(map(str.strip, str(config.get("cycle", "cycle_labels", fallback=default_labels)).split(",")))
      if self.realtime :
          self.cycle_times = list(map(str.strip, str(config.get("cycle", "trigger_time")).split(",")))
          # to allow staging suite with same config but shifted trigger time
          # Yes, this is pretty hacky.
          if "override" in config.sections() and "cycle_time_lag" in config['override'].keys() :
              td = config.get("override", "cycle_time_lag")
              print("Shifting cycle times by " + td )
              add_td = lambda x : datetime.datetime.strftime(
                      datetime.datetime.strptime(x,"%H:%M") + 
                      datetime.timedelta(minutes=int(td)), "%H:%M")
              self.cycle_times = [ add_td(x) for x in self.cycle_times ]
              

    if self.suite_type in [ "forecast_cycle" ] :
      self.has_forecast = True
      self.runlist = list(map(int,map(str.strip, str(config.get("cycle", "runcycles")).split(","))))
      self.has_postproc = ("postproc" in config.sections()) and (len(config.items("postproc")) > 0)
      self.max_postproc = config.getint("settings", "MAX_POSTPROC", fallback=30)
<<<<<<< HEAD
=======
      self.max_lbc = config.getint("settings", "MAX_LBC", fallback=30)
>>>>>>> 7b69f59... update ATOS ini files
      self.has_products = ("products" in config.sections()) and (len(config.items("products")) > 0)
      self.has_lagged = ("lagged" in config.sections()) and (len(config.items("lagged")) > 0)
      self.trigger = str(config.get("suite", "trigger", fallback=""))
      self.has_trigger = self.trigger != ""
      self.has_clock = self.realtime and config.get("cycle", "trigger_time") != ""
      self.has_alert = config.get("settings", "WALLTIME_CYCLE", fallback="") != ""
<<<<<<< HEAD
      self.has_assimilation = config.getboolean("assimilation", "assimilation")
=======
      if "assimilation" not in config.sections() :
        self.has_assimilation = False
      else :
        self.has_assimilation = config.getboolean("assimilation", "ASSIMILATION")
>>>>>>> 7b69f59... update ATOS ini files
      self.has_dfi = config.getboolean("model", "DFI")
      self.forecast_length = config.getint("cycle", "forecast_length")
      if self.forecast_length < self.cycle_inc :
        print("ERROR: forecast length shorter than assimilation cycle!")
      # which cycles are actually doing a forecast (not only DA)
      # organise as daily loop or continuous chain
      self.has_loop = self.realtime or self.cycle_inc == 24
    elif self.suite_type in [ 'bmatrix' ] :
      self.has_forecast = True
      self.realtime = False
      self.has_assimilation = True
    elif self.suite_type in [ "master" ] :
      self.realtime = True
      self.has_forecast = False
      self.has_assimilation = False

    if self.has_forecast :
      # coupling
      self.lbc_inc = config.getint("coupling", "LBC_INC")
<<<<<<< HEAD
=======
      self.lbc_in_loop = config.getboolean("coupling", "LBC_IN_LOOP", fallback = True)
>>>>>>> 7b69f59... update ATOS ini files
      model_domain = config.get("model", "DOMAIN")
      self.coupling_strategy = config.get("coupling", "COUPLING", fallback = "unknown")
      coupling_domain = config.get("coupling", "COUPLING_DOMAIN", fallback = model_domain)
      self.has_e927 = coupling_domain != model_domain
      # model
      self.has_surfex = config.get("model", "SURFACE") == "surfex"
      # namelists may be on ecflow server side or on HPC side
      self.local_namelists = config.get("settings", "DPATH_NAMELISTS", fallback="") == ""

    # these variables need fixing for *all* local (non-hpc) jobs
    # non-hpc tasks may have to know the user account used on HPC (if it is different)
    self.jobs = { "localjob":{ "HOST":self.localhost, "USER":self.username,
                               "HPC_USER":self.hpc_user,
                               "ECF_OUT":self.local_temp, "LOCALJOB":"yes"},
                  "hpcjob":{ "HOST":"@SCHOST@", "USER":self.hpc_user,
                             "ECF_OUT":"@HPC_LOGPATH@", "LOCALJOB":"no"}
                  }

    #########################
    # ASSIMILATION SETTINGS #
    #########################

<<<<<<< HEAD
    if not self.has_assimilation :
      self.assim_var = { "ASSIMILATION":"no" }
    else :
    # TODO: more robustness, fallback values... it's still a bit of a mess
      self.assim_upper = config.get("assimilation", "assim_upper")
      self.assim_surface = config.get("assimilation", "assim_surface")
      self.obs_npool = config.getint("assimilation", "obs_npool")
      self.obstypes_surface = list(map(str.strip, str(config.get("assimilation", "obstypes_surface")).split(",")))
      self.fg_max = config.getint("assimilation", "fg_max", fallback=self.cycle_inc)
      # FIXME: bmatrix suite shouldn't have COLDSTART defined (but no harm...)
      self.coldstart = config.get("assimilation", "coldstart", fallback="1234567890")
      self.assim_var = {
        "ASSIMILATION":"yes",
        "ASSIM_UPPER":str(self.assim_upper),
        "ASSIM_SURFACE":str(self.assim_surface),
        "OBS_NPOOL":str(self.obs_npool),
        "COLDSTART":str(self.coldstart),
        "OBSTYPES_SURFACE":" ".join(self.obstypes_surface),
        "FG_MAX":str(self.fg_max),
        }
      if self.assim_upper == "3dvar" :
        self.obstypes_upper   = list(map(str.strip, str(config.get("assimilation", "obstypes_upper")).split(",")))
        self.assim_var["OBSTYPES_UPPER"] = " ".join(self.obstypes_upper)
      # we may want to add robustness by storing a "pre-first guess" for later cycles
      # FIXME: do canari and screening ALWAYS have to be == npool?
      self.odb_arch = config.getboolean("assimilation", "odb_arch", fallback=False)

=======
    if self.has_assimilation :
    # TODO: more robustness, fallback values... it's still a bit of a mess
      self.assim_upper = config.get("assimilation", "ASSIM_UPPER")
      self.assim_surface = config.get("assimilation", "ASSIM_SURFACE")
      self.fg_max = config.getint("assimilation", "FG_MAX", fallback=self.cycle_inc)

      # we may want to add robustness by storing a "pre-first guess" for later cycles
      # FIXME: do canari and screening ALWAYS have to be == npool?
>>>>>>> 7b69f59... update ATOS ini files

  def has_wait(self, i):
    if self.wait_mode :
      w_time = ( self.realtime and self.cycle_times[i] != "" )
      w_trigger = self.has_trigger and self.trigger_labels[i] != ""
      w_firstguess = self.has_assimilation
      return (w_trigger or w_time or w_firstguess )
    else :
      return (False)

  def cycle_trigger(self, i):
    if self.trigger_labels[i] == "" :
      return ""
    else :
      return self.cycle_trigger.replace("cycle", self.cycle_labels[i])

  def this_run(self, i):
    return self.cycle_labels[ i ]

  def next_run(self, i):
    return self.cycle_labels[ (i + 1) % self.ncycle]

  def prev_run(self, i):
    return self.cycle_labels[ (i - 1) % self.ncycle]

  def is_runcycle(self, i):
    return (i == -1 or i * self.cycle_inc in self.runlist )

  def is_maincycle(self, i):
    return (i * self.cycle_inc in [0,6,12,18] )

  def fclen(self, i):
    if i == -1 or i * self.cycle_inc in self.runlist :
      return self.forecast_length
    else :
      return self.cycle_inc

  def read_section(self, section, err=False):
    if section in self.config.sections() :
      return { str(y[0]):str(y[1]) for y in self.config.items(section) }
    elif err :
      raise Exception("Section " + section + " not found in config file.")
    else :
      return None

