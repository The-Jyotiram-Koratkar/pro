use msql;

CREATE TABLE auto_ins
(
MySQL_Function VARCHAR(30),
DateTime DATETIME,
Date DATE,
Time TIME,
Year YEAR,
TimeStamp TIMESTAMP
);

INSERT INTO auto_ins
(MySQL_Function, DateTime, Date, Time, Year, TimeStamp)
VALUES
("s1", NOW(), NOW(), NOW(), NOW(), NOW());


########################Calculate script execution time#############

#for diff. in Hrs.
#CREATE TABLE t (script VARCHAR(30),start datetime, end datetime, elapsed decimal(5, 2) AS (ROUND(TIMESTAMPDIFF(MINUTE, start, end)/60, 2))); 

#for diff. in Min.

#At the begining of the script

CREATE TABLE t (script VARCHAR(30),start datetime, end datetime, elapsed decimal(5, 2) AS (ROUND(TIMESTAMPDIFF(MINUTE, start, end), 2)));
INSERT INTO t(script,start) values("s1",NOW());
select * from t;
#+--------+---------------------+------+---------+
#| script | start               | end  | elapsed |
#+--------+---------------------+------+---------+
#| s1     | 2018-06-30 15:30:16 | NULL |    NULL |
#+--------+---------------------+------+---------+

#At the end of the script

UPDATE t SET end=NOW() where script='s1';
select * from t;
#+--------+---------------------+---------------------+---------+
#| script | start               | end                 | elapsed |
#+--------+---------------------+---------------------+---------+
#| s1     | 2018-06-30 15:30:16 | 2018-06-30 15:38:35 |    8.00 |
#+--------+---------------------+---------------------+---------+

#############################END###################################


#=-=-=-=-=-=-=-= Method 2 =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
CREATE TABLE `script_tracker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Script_Name` varchar(150) NOT NULL,
  `Start_Time` datetime NOT NULL,
  `End_Time` datetime NOT NULL,
  `Total_Time` time NOT NULL,
  `Created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


#At start of the script

SET @Start_time=now();


#At the end of the script
SET @End_Time=now();
insert into script_tracker (Script_Name,Start_Time,End_Time,Total_Time) values ('FileName',@Start_time,@End_Time,TIMEDIFF(@End_Time,@Start_time)); 


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
