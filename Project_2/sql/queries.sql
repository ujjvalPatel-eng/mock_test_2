
select ti.department,avg(ti.resolution_hours) as avg_hours
from tickets ti join teams te on 
ti.team_id =te.team_id 
group by ti.department 
order by avg_hours;

select * from tickets;
select ti.team_id,ti.department,avg(ti.resolution_hours) as avg_hours
from tickets ti join teams te on 
ti.team_id =te.team_id 
group by ti.team_id,ti.department
order by avg_hours;

select
    channel,
    COUNT(*) AS breach_count
from tickets
where resolution_hours > 24
group by channel
order by breach_count desc, channel asc
limit 2;

SELECT
    COUNT(*) AS unmatched_team_keys
FROM tickets t
LEFT JOIN teams te
    ON t.team_id = te.team_id
WHERE te.team_id IS NULL;
