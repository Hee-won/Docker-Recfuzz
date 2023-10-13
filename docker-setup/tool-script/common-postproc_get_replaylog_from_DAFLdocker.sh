#!/bin/bash

# Replay newly found crash inputs
#rm output/crashes/README.txt
CRASH_LIST=$(ls output/crashes)

START_TIMESTAMP="2023-10-02 17:34:35"
START_TIME=$(date -d "$START_TIMESTAMP" "+%s")

# During the replay, set the following ASAN_OPTIONS again.
export ASAN_OPTIONS=allocator_may_return_null=1,detect_leaks=0

#cp -f /benchmark/bin/ASAN/$1 ./$1
echo "Crash Replay log for swftophp-4.8-2018-11095" > output/replay_log.txt

for crash in $CRASH_LIST; do

    IFS='_' read -ra parts <<< "$(basename "$crash")"
    time_part="${parts[0]}"
    formatted_time=$(echo "$time_part"  | sed 's/\(.*-.*\)-/\1 /')


    timestamp=$(date -d "$formatted_time" "+%s")
    DIFF_TIME=$((timestamp - START_TIME))



    #DIFF_TIME=$(echo `stat -c%Y output/crashes/${crash}` - $START_TIME | bc)
    readarray -d , -t CRASH_ID <<<$crash

    echo -e "\nReplaying crash - ${CRASH_ID[0]} (found at ${DIFF_TIME} sec.):" >> output/replay_log.txt
    echo -e "\nReplaying crash - ${CRASH_IP[0]} (found at ${DIFF_TIME} sec.):" 

    cp -f output/crashes/$crash ./@@
    timeout -k 30 15 ./swftophp-4.8-2018-11095 @@ 2>> output/replay_log.txt
    echo "Exit value is $(echo $?)" >> output/replay_log.txt
done

# To save storage space.
#rm -rf output/queue/

# Copy the output directory to the path visible by the host.
cp -r output /output

# Notify that the whole fuzzing campaign has successfully finished.
echo "FINISHED" > /STATUS