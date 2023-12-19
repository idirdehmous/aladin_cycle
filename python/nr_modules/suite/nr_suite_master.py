from ecflow import *
from nr_modules.nr_classes import *
from nr_modules.assimilation import *

def build_suite(suite, suite_config, config) :
  
  suite.add_label("SUITE_LIST", str(config.get("settings", "SUITE_LIST")))

  #####################
  # maintenance tasks #
  #####################

  tasklist = { x[0]:str(x[1]) for x in config.items("maintenance") }

  master = suite.add_family("maintenance").add(Edit(ECF_FILES=suite_config.suite_path + "/scr/master"))
  for tt in tasklist.keys() :
    mtask = master.add_task(tt).add(Defstatus("complete"))
    if len(tasklist[tt]) > 0 :
      for task_opt in [ p for p in tasklist[tt].replace("\n",",").split(",") if p.strip() ] :
        zz = list(map(str.strip, task_opt.split("=")))
        if zz[0] == "local" and zz[1] == "yes" :
          mtask.add_variable(suite_config.jobs["localjob"])
        else :
          mtask.add_variable(zz[0], zz[1])

  #################
  # regular tasks #
  #################

  tasklist = { x[0]:str(x[1]) for x in config.items("crontasks") }
  cycleTasks = suite.add_family("cycle").add(
          Edit(ECF_FILES=suite_config.suite_path + "/scr/master"),
          RepeatDate("YMD", int(suite_config.begindate), int(suite_config.enddate)))

  for i in range(suite_config.ncycle) :
    RR = i * suite_config.cycle_inc
    mhour = cycleTasks.add_family(suite_config.this_run(i))
    mhour.add(Time(suite_config.cycle_times[i]))

    for tt in tasklist.keys() :
      mtask = mhour.add_task(tt)
      if len(tasklist[tt]) > 0 :
        for task_opt in [ p for p in tasklist[tt].replace("\n",",").split(",") if p.strip() ] :
          zz = list(map(str.strip, task_opt.split("=")))
          if zz[0] == "local" and zz[1] == "yes" :
            mtask.add_variable(suite_config.jobs["localjob"])
          if zz[0] == "InLimit" :
            mtask.add(InLimit(zz[1]))
#            elif zz[0] == "script" :
#              script_name = zz[1]
          elif zz[0] == "trigger" :
              trigger_list = map(str.strip, zz[1].split())
              trigger = " and ".join(["./" + x + " == complete " for x in trigger_list])
              mtask.add_trigger(trigger)
          else :
              mtask.add_variable(zz[0], zz[1])


