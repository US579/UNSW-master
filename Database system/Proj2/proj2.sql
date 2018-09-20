
--Q1:
---------------------------------------------
create or replace view Q1_1(course,num)
as
select distinct course, count(student) as num from course_enrolments group by course;


create or replace function Q1_11(course_id integer) 
	returns integer
as $$
declare valid_room_number integer;
begin 
select count(rooms.id) into valid_room_number 
from Q1_1,rooms
where Q1_1.course = $1 and rooms.capacity >= Q1_1.num
group by course;
return valid_room_number;
end;
$$ language plpgsql;

drop type if exists RoomRecord cascade;
create type RoomRecord as (valid_room_number integer, bigger_room_number integer);
 
create or replace function Q1(course_id integer)
returns RoomRecord
as $$
declare results RoomRecord;
        student_number integer;
begin
IF $1 not in (select id from courses) then 
raise exception 'INVALID COURSEID';
end if;
select count(distinct sub.student) into student_number
from(
	select  course_enrolments.student as student,course_enrolments.course as course
	from course_enrolments
	union
	select  course_enrolment_waitlist.student as student,course_enrolment_waitlist.course as course
	from course_enrolment_waitlist
    )as sub
	where sub.course = ($1);
select count(*) into results.bigger_room_number from rooms where rooms.capacity >= student_number;
select * into results.valid_room_number from Q1_11($1);
return results;
end;
$$ language plpgsql;
---------------------------------------------------------



--Q2:
---------------------------------------------------------
create or replace view Q2_3(id,mark)
as
select courses.id ,Course_enrolments.mark
from semesters,Course_staff,courses,subjects,Course_enrolments
where semesters.id = courses.semester and courses.subject = subjects.id
and course_staff.course = courses.id and Course_enrolments.course = courses.id
and Course_enrolments.mark is not null
;

create or replace view Q2_2(id,average)
as
select  courses.id,round(1.0*sum(Course_enrolments.mark)/count(courses.id),0)
from semesters,Course_staff,courses,subjects,Course_enrolments
where semesters.id = courses.semester and courses.subject = subjects.id
and course_staff.course = courses.id and Course_enrolments.course = courses.id
and Course_enrolments.mark is not null
group by courses.id;


create or replace view Q2_1(id,highest)
as
select courses.id ,max(Course_enrolments.mark) as highest
from semesters,Course_staff,courses,subjects,Course_enrolments
where semesters.id = courses.semester and courses.subject = subjects.id
and course_staff.course = courses.id and Course_enrolments.course = courses.id
and Course_enrolments.mark is not null
group by courses.id;
	
create or replace function Q1_total(integer)
returns bigint
as $$
select count(*) from course_enrolments
where mark is not null 
and course = $1
$$
language sql;

create or replace function median(anyarray) 
returns double precision as $$
  select ($1[array_upper($1,1)/2+1]::double precision + $1[(array_upper($1,1)+1) / 2]::double precision) / 2; 
$$ language sql immutable strict;

create or replace function Q2_4(integer)
returns double precision
as $$
select median(array(select mark from Q2_3 where id = $1 order by mark)) 
$$
language sql;

drop type if exists TeachingRecord cascade;
create type TeachingRecord as (
	cid integer, 
	term char(4), 
	code char(8), 
	name text, 
	uoc integer, 
    average_mark integer, 
	highest_mark integer,
	median_mark integer, 
	totalEnrols integer);

create or replace function Q2(staff_id integer)
returns setof TeachingRecord
as $$
declare results TeachingRecord;
        course_id  integer;   
begin
IF $1 not in (select id from Staff) then 
raise exception 'INVALID STAFFID';
end if;

for results in 
select courses.id,right(semesters.year||lower(semesters.term),4),
subjects.code ,subjects.name ,subjects.uoc,Q2_2.average,Q2_1.highest,Q2_4(course),Q1_total(course)
from semesters,Course_staff,courses,subjects,Q2_1,Q2_2
where semesters.id = courses.semester and Q2_1.id = courses.id and Q2_2.id = courses.id and courses.subject = subjects.id
and course_staff.course = courses.id and Q1_total(course)> 0 and staff = $1 loop
return next results;
end loop;
return;
end;
$$ language plpgsql;
--... SQL statements, possibly using other views/functions defined by you ...



--Q3:

create or replace function Q3_org(org_id integer)
returns table(owner integer,member integer)
as $$
with recursive q as (select member,owner from orgunit_groups where member=$1
union all select m.member,m.owner from orgunit_groups m join q on q.member=m.owner)
select owner,member from q;
$$ language sql;

create or replace function Q3_org2(org_id integer)
returns table(owner integer,member integer,name mediumstring)
as $$
select Q3_org.owner,Q3_org.member,orgunits.name
from Q3_org($1),orgunits
where orgunits.id=Q3_org.member
$$ language sql;

create or replace function Q3_1(org_id integer,num_courses integer)
	returns table(unswid integer, student_name text)
as $$
select people.unswid,cast(people.name as text)
from Q3_org2($1),subjects,courses,people,Course_enrolments,Students
where  subjects.offeredby=Q3_org2.member and courses.subject=subjects.id 
and Course_enrolments.course=courses.id and people.id=Students.id 
and Course_enrolments.student = students.id
group by people.unswid,people.name
having count(Course_enrolments.course)>$2;
$$ language sql;


create or replace function Q3_sub(org_id integer)
	returns table(unswid integer, student_name text, subject_name text,subject_code char(8),semesters_name char(9),cours_id integer, name mediumstring, mark integer)
as $$
select people.unswid,cast(people.name as text),subjects.name,subjects.code,semesters.name,courses.id,Q3_org2.name, Course_enrolments.mark
from Q3_org2($1),subjects,courses,people, Course_enrolments,students,semesters
where  subjects.offeredby=Q3_org2.member and courses.subject=subjects.id 
and Course_enrolments.course=courses.id and people.id=Students.id 
and Course_enrolments.student = students.id and semesters.id = Courses.semester
group by people.unswid,people.name,subjects.id,subjects.code,courses.id,semesters.name,Q3_org2.name, Course_enrolments.mark
$$ language sql;

create or replace function Q3_2(org_id integer,num_courses integer,min_score integer)
	returns table(unswid integer, student_name text, subjects char(9), min_score integer)
as $$
select unswid,student_name,subject_code,mark
from Q3_sub($1)
where  unswid in (select unswid from Q3_1($1,$2)) and  mark >= $3
group by unswid,student_name,subject_code,mark;
$$ language sql;


create or replace function Q3_3(org_id integer,num_courses integer,min_score integer)
	returns table(unswid integer, student_name text, course_records text,mark integer)
as $$
select t.a ,t.b, t.c, t.d from (
select Q3_1.unswid as a, Q3_1.student_name as b ,cast(Q3_sub.subject_code || ', ' || Q3_sub.subject_name  || ', ' || Q3_sub.semesters_name
|| ', ' || Q3_sub.name as text) as c, cast(Q3_sub.mark  as integer )as d,row_number() over(partition by Q3_1.unswid) as row
from Q3_1($1,$2),Q3_2($1,$2,$3),Q3_sub($1)
where Q3_1.unswid=Q3_2.unswid and Q3_2.unswid = Q3_sub.unswid
group by Q3_1.unswid,Q3_1.student_name,Q3_sub.subject_code,Q3_sub.subject_name,Q3_sub.semesters_name,Q3_sub.name,Q3_sub.mark
order by Q3_1.unswid,Q3_sub.mark desc nulls last) t
where row <= 5;
$$ language sql;
 
create type CourseRecord as (unswid integer, student_name text, course_records text);
create or replace function Q3(org_id integer,num_courses integer,min_score integer) 
	returns setof CourseRecord
as $$
begin
IF $1 not in (select id from OrgUnits) then 
raise exception 'INVALID ORGID';
end if;	
	return query 
	( 	
		select unswid,student_name,string_agg(course_records||', '||mark|| E'\n','' order by mark desc,course_records desc) 
		from Q3_3($1,$2,$3) 
		group by unswid,student_name order by unswid
		
	);	
end;

$$ language plpgsql;
