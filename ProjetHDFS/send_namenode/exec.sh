#!/bin/bash

apt-get update
apt-get -f install
apt-get upgrade -y
apt-get install python3-pip -y
/usr/bin/python3 -m pip install happybase

./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift

hadoop fs -mkdir -p input

hadoop fs -put data.csv input
hdfs dfs -rmdir output

cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
# hadoop jar hadoop-streaming-2.7.2.jar -file mapper.py -mapper "python3 mapper.py" -file reducer.py -reducer "python3 reducer.py" -input input/* -output output
