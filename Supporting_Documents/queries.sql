
/* Get the number of visits from each unit within facility 44 */ 
select rooms.uid,uname,  count(*) 
from visits, rooms, units 
where visits.rid = rooms.rid and rooms.fid = 44 and rooms.uid = units.uid  
group by rooms.uid;

/* Get the number of visits in each facility */
select fid, count(*)
from visits v, rooms r
where v.rid = r.rid 
group by r.fid;

/* Get the number of visits in each facility  with unit information */
select rooms.uid, rooms.fid,  uname,count(*)
from visits, rooms, units 
where visits.rid = rooms.rid and rooms.uid = units.uid and units.uname like "%ICU%"
group by rooms.uid;


/*  Rooms to compare 
| uid | fid | uname                     | count(*) |
| 128 |  19 | ICU                       |   492976 | 
| 181 |  21 | ICU                       |   146757 |
| 195 |  15 | ICU                       |   425059 | No information about the facility type 
*/ 


/*Didn't work*/
select distinct datepart(dy,v.itime) 
from visits v;

/*Date part function doesn't work on the server*/
select distinct datepart(dy,visits.itime), rooms.rid
from visits, rooms, units
where visits.rid = rooms.rid and rooms.uid = units.uid and (units.uid = 128 or units.uid = 181) ;

/* Finds min and max date for specified units */
select date(min(itime)), date(max(itime)), rooms.uid
from visits, rooms, units
where visits.rid = rooms.rid and rooms.uid = units.uid and (units.uid = 128 or units.uid = 181) 
group by rooms.uid;

SELECT v.rid,v.hid,v.duration,v.itime,v.otime,v.idisp,v.odisp,jt.jtid,jt.jtname 
FROM visits v, hcws h, rooms r, units u, jobs j, jtypes jt
WHERE v.hid=h.hid AND v.shift='day' AND h.fid=19 AND v.rid=r.rid AND r.uid=u.uid AND u.uid=128 AND j.jid=h.jid AND jt.jtid=j.jtid AND
      itime>"2019-03-12" AND otime<"2019-03-13" ORDER BY otime,itime;


/* Error in the sql syntax*/
select v.hid, v.rid, j.jtid, v.itime, v.otime
from visits v, hcws h, rooms r, units u, jobs j, 
where v.hid=h.hid and v.shift='day' and u.uid = 128  and v.rid = r.rid and r.uid = u.uid and
     itime>"2019-03-12" and otime<"2019-03-13";
     