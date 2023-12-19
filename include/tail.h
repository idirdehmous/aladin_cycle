# better put sync commands (only) where they are really needed?
# echo "sync ... `date`"
# sync -d .                 # flush all file I/O before signalling completion!
echo "wait ... `date`"
wait                      # wait for any background processes to stop
set +x
TASK_FINISH_TIME=`date -u +"%Y-%m-%d %H:%M:%S"`
echo "===== TASK STARTED:  ${TASK_START_TIME:-unknown} ====="
echo "===== TASK FINISHED: ${TASK_FINISH_TIME:-unknown} ====="
set -x

ecflow_client --complete  # Notify ecFlow of a normal end
trap 0                    # Remove all traps
exit 0                    # End the shell

