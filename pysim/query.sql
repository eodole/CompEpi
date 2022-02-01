
SELECT v.rid,v.hid,v.duration,v.itime,v.otime,jt.jtid,jt.jtname 
FROM visits v, hcws h, rooms r, units u, jobs j, jtypes jt
WHERE v.hid=h.hid AND v.shift='day' AND h.fid=19 AND v.rid=r.rid AND r.uid=u.uid AND u.uid=128 AND j.jid=h.jid AND jt.jtid=j.jtid AND
      itime>"2019-03-12" AND otime<"2019-03-13" ORDER BY otime,itime;






/*

SELECT v.rid,v.hid,v.duration,v.itime,v.otime,v.idisp,v.odisp,jt.jtid,jt.jtname 
FROM visits v, hcws h, rooms r, units u, jobs j, jtypes jt
WHERE v.hid=h.hid AND v.shift='day' AND h.fid=16 AND v.rid=r.rid AND r.uid=u.uid AND u.uid=171 AND j.jid=h.jid AND jt.jtid=j.jtid AND
      itime>"2018-01-01" AND otime<"2018-01-02" ORDER BY otime,itime;
*/
