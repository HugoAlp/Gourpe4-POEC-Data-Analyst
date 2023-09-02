# $SRC_PATH="exec.sh"
# $DEST_PATH="/root/exec.sh"


#download docker image  from dockerhub
docker pull liliasfaxi/spark-hadoop:hv-2.7.2
#create connection  to link the 3 containers
docker network create --driver=bridge hadoop

#run
docker run -itd --net=hadoop -p 9070:50070 -p 8088:8088 -p 7077:7077 -p 16010:16010 -p 9090:9090 --name hadoop-master --hostname hadoop-master liliasfaxi/spark-hadoop:hv-2.7.2
docker run -itd -p 8040:8042 --net=hadoop --name hadoop-slave1 --hostname hadoop-slave1 liliasfaxi/spark-hadoop:hv-2.7.2
docker run -itd -p 8041:8042 --net=hadoop --name hadoop-slave2 --hostname hadoop-slave2 liliasfaxi/spark-hadoop:hv-2.7.2

# Initial merge of files
python init_merge.py

# Convert 
Get-content ./send_namenode/exec.sh -raw | % {$_ -replace "`r", ""} | Set-Content -NoNewline ./send_namenode/exec_unix.sh

# Copy files
docker cp send_namenode/. hadoop-master:/root

# Launch script
docker exec hadoop-master /bin/bash -c 'chmod ug+x *.sh'
docker exec hadoop-master /bin/bash -c './exec_unix.sh'
