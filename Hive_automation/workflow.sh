#!/bin/bash
echo "start"
source /home/hduser/.bashrc
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export HIVE_HOME=/usr/local/apache-hive-2.1.1-bin
cd /usr/local/apache-hive-2.1.1-bin/bin/
./hive -e "use clevertap;LOAD DATA LOCAL INPATH '/home/hduser/hr_employees.csv' OVERWRITE INTO TABLE employee PARTITION (department='HR');select * from clevertap.employee;"
echo "end"
