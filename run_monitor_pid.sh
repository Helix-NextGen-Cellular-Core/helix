#!/bin/bash
filename="/tmp/corelogs/pid_output.txt"
[ -f $filename ] && rm $filename;
while true; do
  ps -ax --sort comm | grep -E "/(amf|smf)/(amf|smf)" | awk '{print $1, $5}' | while read -r pid process; do
      output=$(bash /tmp/total_cpu_usage.sh "$pid")
      echo "$pid,$process,$output" >> $filename
  done
  timestamp=$(date | awk '{print $5}')
  echo "time: $timestamp"  >> $filename
  sync $filename
  sleep 1
done


