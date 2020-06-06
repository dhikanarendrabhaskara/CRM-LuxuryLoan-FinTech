


### PREPROCESSING ###

--  calling crm database -- 
use crm;

--  selecting table1 -- 
select * from callcenterlogs;
create table testcallcenterlogs as
select * from callcenterlogs;

--  modifying table1 datatypes -- 
alter table callcenterlogs
modify Date_received date;
alter table callcenterlogs
modify ser_time time;
alter table callcenterlogs
modify ser_start time;
alter table callcenterlogs
modify ser_exit time;

--  selecting table2 -- 
select * from events;
create table testevents as
select * from events;

--  table2 data cleaning -- 
select * from testevents
where date_received not like "2%" or date_received like "%a%";
select count(*) from testevents
where date_received not like "2%" or date_received like "%a%";
delete from testevents where date_received not like "2%" or date_received like "%a%";

--  modifying table2 datatypes -- 
alter table testevents
modify Date_received date;



### ANALYSIS ###

--  analysis1 on joined tables (Overall Call Minutes) -- 
select count(*) as Calls, 
	SUM(time_to_sec(ser_time))/60 as TotalMinutes,
    AVG(time_to_sec(ser_time))/60 as AverageMinutes from testevents
	join testcallcenterlogs on testevents.Complaint_ID = testcallcenterlogs.ComplaintID
    order by AverageMinutes desc;
    
--  analysis2 on joined tables (Call Minutes by Product) --     
select Product, count(*) as Calls, 
	SUM(time_to_sec(ser_time))/60 as TotalMinutes,
    MIN(time_to_sec(ser_time))/60 as MinMinutes,
    MAX(time_to_sec(ser_time))/60 as MaxMinutes,
    AVG(time_to_sec(ser_time))/60 as AverageMinutes from testevents
	join testcallcenterlogs on testevents.Complaint_ID = testcallcenterlogs.ComplaintID
    group by Product
    order by AverageMinutes desc;

--  analysis3 on joined tables (Call Minutes by Issues - Average order) --  
select Issue, Product, count(*) as Calls, 
	SUM(time_to_sec(ser_time))/60 as TotalMinutes,
    MIN(time_to_sec(ser_time))/60 as MinMinutes,
    MAX(time_to_sec(ser_time))/60 as MaxMinutes,
    AVG(time_to_sec(ser_time))/60 as AverageMinutes from testevents
	join testcallcenterlogs on testevents.Complaint_ID = testcallcenterlogs.ComplaintID
    group by Issue
    order by AverageMinutes desc;
    
--  analysis4 on joined tables (Call Minutes by Issues - Max order) --    
select Issue, Product, count(*) as Calls, 
	SUM(time_to_sec(ser_time))/60 as TotalMinutes,
    AVG(time_to_sec(ser_time))/60 as AverageMinutes,
    MIN(time_to_sec(ser_time))/60 as MinMinutes,
    MAX(time_to_sec(ser_time))/60 as MaxMinutes from testevents
	join testcallcenterlogs on testevents.Complaint_ID = testcallcenterlogs.ComplaintID
    group by Issue
    order by MaxMinutes desc;
    
--  analysis5 on joined tables (Call Minutes by Issues - Total order) --   
select Issue, Product, count(*) as Calls, 
    AVG(time_to_sec(ser_time))/60 as AverageMinutes,
    MIN(time_to_sec(ser_time))/60 as MinMinutes,
    MAX(time_to_sec(ser_time))/60 as MaxMinutes,
    SUM(time_to_sec(ser_time))/60 as TotalMinutes from testevents
	join testcallcenterlogs on testevents.Complaint_ID = testcallcenterlogs.ComplaintID
    group by Issue
    order by TotalMinutes desc;


    



    




