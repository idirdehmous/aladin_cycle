from ecflow import *
from nr_modules.nr_classes import *
from nr_modules.assimilation import *

def build_suite(suite, suite_config, config) :
  if suite_config.cycle_inc == 24 :
    # FIXME !!!
    print("For a cycle with 1 run per day: set suite_type = forecast_cycle_loop ")
  # What if RR != 00 ??? USE RUNCYCLE
  # single run cycle with a repeat cc=1:ncases
  #  add.(RepeatDate("YMD", case_list))

  if suite_config.forecast_length < suite_config.cycle_inc :
    print("ERROR: forecast_length can not be shorter than cycle_inc.")

# variables are easy to pass to jobs
# but they can not be used in triggers unless they are numeric (no string comparisons!)
<<<<<<< HEAD
=======
# so we define an event to indicate whether we are in real time or delayed mode.
# (exp mode for experiments is, by definition, not real-time)
>>>>>>> 7b69f59... update ATOS ini files
# ATTENTION: you can not initialise an event to "set" with add_event
#            maybe it can be done another way???
#            maybe using events in this way is not ideal
#            but what else can you use inside a trigger expression?
#suite.add_label("LAST_FINISHED", " ")

  if suite_config.realtime :
    suite.add_variable("REALTIME", "yes")
<<<<<<< HEAD
  else:
    suite.add_variable("REALTIME", "no")
=======
    if suite_config.delay_mode :
      suite.add_variable("DELAY", "no")
      suite.add_event("DELAY") #.force_event("set")
  else:
    suite.add_variable("REALTIME", "no")
#    suite.add_variable("DELAY", "no") # a bit strange...
>>>>>>> 7b69f59... update ATOS ini files

# From experience, we know that HPC can get into problems with i/o
# So we must limit the number of post-processing jobs
#   (this is mainly for low resolution models which run very fast,
#    so the post processing lags behind)
# TODO: make this an option in the .ini file [settings]?

###########################################################

## Initialise the suite ###
#  suite += nr_init_suite(suite_config)

# some simple tasks for changing the suite mode etc.
  suite += nr_maintenance(suite_config)


########################
# standard main cycle
########################

  suite.add_label("LAST_RUNNING", "")
<<<<<<< HEAD
=======
  suite.add_label("LAST_QUEUED", "")
  suite.add_variable("LAST_QUEUED", "")
>>>>>>> 7b69f59... update ATOS ini files
  if not suite_config.has_loop :
    suite.add_label("LAST_QUEUED", "")
    suite.add_variable("LAST_QUEUED", "")
# TODO: - for a "single run" suite (e.g. only 00h): no triggering of next cycle possible
#           in that case: use a "repeat". Presumably not with assimilation.
#       - "CaseRunner": repeat over a given set of dates
#           (maybe including assimilation if you have archived FG's)
  cycleMain = suite.add_family("cycle")
  if suite_config.has_loop :
    cycleMain.add(RepeatDate("YMD", int(suite_config.begindate), int(suite_config.enddate)))

  for i in range(suite_config.ncycle) :
    RR = i * suite_config.cycle_inc
    ## add a family for this cycle (e.g. "morning" or "00")
    mhour = cycleMain.add_family(suite_config.this_run(i))
    mhour += Edit(RR="%02d" % RR,
                  RUNDATE="@YMD@@RR@",
                  FINISHED_YMD="0",
                  FCLEN=str(suite_config.fclen(i)),
                  THIS_RUN=suite_config.this_run(i),
                  PREV_RUN=suite_config.prev_run(i),
                  NEXT_RUN=suite_config.next_run(i)
                  )
<<<<<<< HEAD
    if not suite_config.has_loop :
=======
    if not suite_config.has_loop : 
>>>>>>> 7b69f59... update ATOS ini files
      mhour += Edit(YMD="")


    mhour += Label("RUNDATE", "")
    # NOTE: Defstatus("complete") is handy to stop the cycle from starting immediately
    if (not suite_config.has_loop) or (suite_config.begindate=="") : 
      mhour += Defstatus("complete")

    if suite_config.has_wait(i) :
      mhour += nr_wait(suite_config, i)
    elif suite_config.realtime :
<<<<<<< HEAD
      # mhour.add(Time(suite_config.cycle_times[i]))
      # NOTE: if e.g. a 21h cycle should be triggered after 00h, we must increase the date!
      #        otherwise the cycle could be triggered much too soon
      # NOTE: if a cycle is delayed to the next date, don't insist on :TIME as well!
      triggertime = int(suite_config.cycle_times[i].replace(":",""))
      if triggertime < 2400:
        ymd = ":YMD"
      else:
        ymd = f"(:YMD + {triggertime // 2400})"
        triggertime = triggertime % 2400
        
      cycle_trigger = f"(:TIME ge {triggertime} AND :ECF_DATE ge {ymd}) OR (:ECF_DATE gt {ymd})"

      mhour.add(Trigger(cycle_trigger))
=======
      # NOTE: a time setting is harder to skip in delay mode...
      mhour.add(Time(suite_config.cycle_times[i])) 
>>>>>>> 7b69f59... update ATOS ini files

    ## Initialisation
    mhour += nr_initialisation(suite_config, i)

    ## LBC's #
    mhour += nr_lbc(suite_config, suite_config.fclen(i)).add(
                    Trigger("./initialisation == complete"),
                    InLimit("max_postproc"))

    ## assimilation family
    if suite_config.has_assimilation :
      mhour += nr_assimilation(suite_config).add(Trigger("./initialisation == complete"))

    ## the forecast itself #
    fctrigger = "(./lbc == complete or ./lbc:LAUNCH_FC == set)"
    if suite_config.has_assimilation :
      fctrigger += " && ./assimilation == complete "
    if suite_config.has_surfex :
      fctrigger += " && ./lbc/prep_sfx == complete "
    mhour += nr_forecast(suite_config, suite_config.fclen(i)).add(
                 Trigger(fctrigger))

    ## cycle tasks (queue next cycle, save first guess)
    # if we are in a non-loop suite, add a task to queue next cycle
    if suite_config.has_assimilation or not suite_config.has_loop :
      mhour += nr_next_cycle(suite_config, suite_config.fclen(i), suite_config.next_run(i))

    ## post-processing family: hourly fullpos tasks
    if suite_config.has_postproc and suite_config.is_runcycle(i) :
      mhour += nr_postproc(suite_config, config)

    ## "post-processing" tasks that are not hourly full-pos, 
    ## but run once after the forecast is finished
    if suite_config.has_products and suite_config.is_runcycle(i) :
      mhour += nr_products(suite_config, config)

    ## A simple "alert" if the (realtime) forecast cycle takes too long
    if suite_config.has_alert :
      mhour += nr_time_alert(suite_config)

    # things that run /after/ the forecast has finished
    mhour += nr_finish(suite_config, suite_config.is_runcycle(i))


########################
# lagged cycle
########################

  if suite_config.has_lagged :
    cycleLag = suite.add_family("lagged")
    cycleLag.add(RepeatDate("YMD", int(suite_config.begindate), int(suite_config.enddate)))

    for i in range(suite_config.ncycle) :
      RR = i * suite_config.cycle_inc

      ## add a family for this cycle (e.g. "morning" or "00")
      mhour = cycleLag.add_family(suite_config.this_run(i))
      main_cycle = "/" + suite_config.suite_name + "/cycle/%02d"%RR
      #main_trigger = "({0}:YMD > :YMD ) OR ({0} == complete AND {0}:YMD == :YMD)".format(main_cycle)
      #  :YMD may trigger too soon, so we use different variable
      #if not suite_config.has_loop :
      main_trigger = " {0}:FINISHED_YMD >= :YMD".format(main_cycle)
      mhour.add_trigger(main_trigger)
      mhour += Edit(RR="%02d" % RR,
                  RUNDATE="@YMD@@RR@",
                  FCLEN=str(suite_config.fclen(i)),
                  THIS_RUN=suite_config.this_run(i),
                  PREV_RUN=suite_config.prev_run(i),
                  NEXT_RUN=suite_config.next_run(i),
                  ECF_FILES=suite_config.suite_path + "/scr/lagged"
                  )

      mhour += Label("RUNDATE", "")
      tasklist = { x[0]:str(x[1]) for x in config.items("lagged") }
      for tt in tasklist.keys() :
        lag_task = mhour.add_task(tt)
        if len(tasklist[tt]) > 0 :
          for opt in [ p for p in tasklist[tt].replace("\n",",").split(",") if p.strip() ] :
            zz = list(map(str.strip, opt.split("=")))
#            print(zz[0] + " : " + zz[1])
            if zz[0] == "local" and zz[1] == "yes" :
              lag_task.add_variable(suite_config.jobs["localjob"])
            if zz[0] == "InLimit" :
              lag_task.add(InLimit(zz[1]))
#            elif zz[0] == "script" :
#              script_name = zz[1]
            elif zz[0] == "trigger" :
              trigger_list = map(str.strip, zz[1].split())
              trigger = " and ".join(["./" + x + " == complete " for x in trigger_list])
              lag_task.add_trigger(trigger)
            else :
              lag_task.add_variable(zz[0], zz[1])


