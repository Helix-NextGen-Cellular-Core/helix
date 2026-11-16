[ -f "amf_docker_output.txt" ] && rm "amf_docker_output.txt";
[ -f "smf_docker_output.txt" ] && rm "smf_docker_output.txt";
while true; do
  docker stats --no-stream $(docker ps --no-trunc -aqf "name=^k8s_amf_amf*") >> amf_docker_output.txt;  
  docker stats --no-stream $(docker ps --no-trunc -aqf "name=^k8s_smf_smf*") >> smf_docker_output.txt;  
  current_time=$(date | awk '{print $5}')
  echo "TIME-$current_time" >> amf_docker_output.txt;  
  echo "TIME-$current_time" >> smf_docker_output.txt;  
  # sync amf_pid_output.txt
  # pidstat -u -p $(docker inspect -f "{{ .State.Pid }}" $(docker ps --no-trunc -aqf "name=^k8s_smf_smf*") | tr '\n' ',') >> smf_pid_output.txt;  
  # sync smf_pid_output.txt
  # pidstat -u -p $(sudo ps -ax | grep /free5gc/amf/amf | awk '{print $1}' | head -n -1  | tr '\n' ',') >> pid_output.txt;  
  sleep 1
done