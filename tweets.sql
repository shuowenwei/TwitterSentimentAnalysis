select creationDay, count(*) from tweets group by creationDay

select * from tweets

select min(creationTime) from tweets where creationDay = 'Fri'

select min(creationTime) from tweets where creationDay = 'Sun'


SET SQL_SAFE_UPDATES=0;
delete * from tweets where creationDay = 'Tue'


-- how to delete things 