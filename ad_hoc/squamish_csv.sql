select @row := @row+1 as `row`
, a.name
, a.instances
, a.version_4
, a.type
, a.location
, a.grade
, a.completed
, a.tried
, a.details
from(
    select s.name
    , count(distinct s.version) as instances
    , sum(if(s.version = 4, 1, 0)) as version_4
    , group_concat(distinct s.type order by s.version asc separator '->') as type
    , group_concat(distinct s.location order by s.version asc separator '->') as location
    , round(avg(s.grade), 1) as grade
    , count(distinct if(b.completed='COMPLETED', b.session_num, null)) as completed
    , count(distinct b.session_num) as tried
    , group_concat(distinct concat('Version ', s.version, ', V', s.grade, ' - ', type) order by s.version separator ' | ') as details
    , @row := 0 as rowinit
    from squamish_top100 s
    left join boulder_problems b on (s.name = b.boulder_name and b.area = 'Squamish')
    group by name
) a
order by completed desc
, tried desc
, if(completed = 1, grade, null) desc
, if(completed = 0, grade, null) asc
, instances desc
, version_4 desc
;