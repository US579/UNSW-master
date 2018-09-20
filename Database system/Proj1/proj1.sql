-- COMP9311 18s1 Project 1
--
-- MyMyUNSW Solution Template


-- Q1: 
create or replace view Q1_3(unswid,name)
as
select  unswid, name
from people
where id in (select student
	from course_enrolments
	where mark >= 85
	group by student
	having count(*)>20);

	    
create or replace view Q1_2(id,name)
as	   
select id,name
from people
where id in (select id 
	         from students
			 where stype = 'intl');

create or replace view Q1(unswid,name)
as
select  unswid, name
from Q1_3 
where name in (select name 
	           from Q1_2);
--... SQL statements, possibly using other views/functions defined by you ...
;



-- Q2: 
create or replace view Q2_1(unswid,rtype,capacity)
as
select unswid,rtype,capacity
from rooms
where building in(SELECT id
                  FROM Buildings
                  WHERE name = 'Computer Science Building');
				  
create or replace view Q2_2(unswid,rtype,capacity)
as				  
select 	unswid,rtype,capacity	
from Q2_1
where rtype in (select id
                from room_types
                where description = 'Meeting Room');

create or replace view Q2(unswid,name)
as
select unswid,longname as name
from rooms
where unswid in (select unswid 
	             from Q2_2 
				 where capacity >= 20); 
--... SQL statements, possibly using other views/functions defined by you ...
;



-- Q3: 
create or replace view q3_1(staff,course)
as				 
select staff,course
from course_staff
where course in (select course 
                from course_enrolments
                 where student in(select id 
                                  from people
                                  where name = 'Stefan Bilek'));


create or replace view Q3(unswid, name)
as
select unswid ,name
from people
where id in(select staff
                from q3_1);
--... SQL statements, possibly using other views/functions defined by you ...
;



-- Q4:
create or replace view Q4_1(student)
as
select student 
from course_enrolments
where course in (select id
	             from courses 
				 where subject in (select id 
					               from subjects
								   where code ='COMP3331'));
								   
create or replace view Q4_2(student)
as
select student 
from course_enrolments
where course in (select id
	             from courses 
				 where subject in (select id 
					               from subjects
								   where code ='COMP3231'));
create or replace view Q4_3(student)
as
select student    
from Q4_1 
intersect  
select student   
from Q4_2;


create or replace view Q4(unswid, name)
as
select unswid, name
from people
where id in (select student 
	         from Q4_1 
		     where student not in 
		      (select student 
			   from Q4_3));
--... SQL statements, possibly using other views/functions defined by you ...
;



-- Q5: 
create or replace view Q5a(num)
as
SELECT COUNT(distinct Program_enrolments.id)
FROM Students,Semesters,Streams,Program_enrolments,Stream_enrolments
WHERE Students.stype='local' AND Semesters.name='Sem1 2011' AND Streams.name='Chemistry' 
AND Program_enrolments.student=Students.id AND Program_enrolments.semester=Semesters.id 
AND Stream_enrolments.stream=Streams.id AND Program_enrolments.id=Stream_enrolments.partof
;
--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q5: 
create or replace view Q5b(num)
as
SELECT COUNT(distinct Program_enrolments.id)
FROM Students,Semesters,Program_enrolments,OrgUnit_types,OrgUnits,Programs
WHERE Students.stype='intl' AND Semesters.name='Sem1 2011'  
AND Program_enrolments.student=Students.id AND Program_enrolments.semester=Semesters.id 
AND OrgUnits.utype=OrgUnit_types.id AND OrgUnit_types.name='School'
AND OrgUnits.longname='School of Computer Science and Engineering' AND Programs.offeredby=OrgUnits.id
AND Program_enrolments.semester=Semesters.id AND Program_enrolments.program=Programs.id ;

--... SQL statements, possibly using other views/functions defined by you ...
;

-- Q6:
create or replace function
	Q6(text) returns text
as
$$select concat(code,' ',name,' ',UOC) as text from Subjects
where code = $1
$$ language sql;


-- Q7: 
create or replace view Q7_1(Pid,id)
as
SELECT Programs.id,Students.id 
FROM  Students,Program_enrolments,Programs
WHERE   Program_enrolments.student=Students.id 
AND Program_enrolments.program=Programs.id;


create or replace view Q7_2(pid,id)
as
SELECT Programs.id,Students.id 
FROM  Students,Program_enrolments,Programs
WHERE   Program_enrolments.student=Students.id 
AND Program_enrolments.program=Programs.id AND
Students.stype='intl';

create or replace view Q7_3(pid,num1)
as
select pid,
count(*) as num1
from Q7_1
group by pid;

create or replace view Q7_4(pid,num2)
as
select pid ,
count(*) as num2
from Q7_2
group by pid;

create or replace view Q7_5(pid,rate)
as
select b.pid,
CAST(1.0*a.num2/b.num1 as decimal(18,5)) as rate
from Q7_3 b,Q7_4 a
where a.pid = b.pid;

create or replace view Q7(code,name)
as
select  distinct code, name
from Programs
where id in (select pid from Q7_5
               where rate > 0.50000);

			   
			   
--... SQL statements, possibly using other views/functions defined by you ...
;



-- Q8:

create or replace view Q8_2(course,num)
as
select course, count(course) as num  from course_enrolments where mark is not null group by course;

create or replace view Q8_1(course,mark)
as
select Q8_2.course,course_enrolments.mark
from Q8_2, course_enrolments
where Q8_2.course = course_enrolments.course and
Q8_2.num >= 15;

create or replace view Q8_3(course,course_num ,tmark)
as
select course,count(course) as course, sum(mark) as mark  from Q8_1 group by course;

create or replace view Q8_4(course,average)
as
select course,CAST(Q8_3.tmark/Q8_3.course_num as  numeric(4,2)) as average from Q8_3;


create or replace view Q8_5(course,average)
as
select course,average  from Q8_4 where average in (select max(average) from Q8_4);

create or replace view Q8_6(subject)
as
select subject from courses where id in (select course from Q8_5 );

create or replace view Q8_7(semester)
as
select semester from courses where id in  (select course from Q8_5);

create or replace view Q8(code,name,semester)
as
select distinct subjects.code,subjects.name,semesters.name as semester
from subjects,semesters,Q8_6,Q8_7
where subjects.id = Q8_6.subject and Q8_7.semester = semesters.id;

--... SQL statements, possibly using other views/functions defined by you ...
;



-- Q9:

create or replace view Q9_1(name, school,email,phone, starting)
as
SELECT People.name,OrgUnits.longname,people.email,Staff.phone,Affiliations.starting
FROM People,OrgUnits,Staff,Affiliations,Staff_roles,OrgUnit_types
WHERE Staff_roles.name='Head of School' AND Affiliations.role=Staff_roles.id
AND Affiliations.ending is null AND OrgUnit_types.name='School'
AND OrgUnits.utype=OrgUnit_types.id AND Affiliations.orgunit=OrgUnits.id
AND Staff.id=Affiliations.staff AND People.id=Staff.id AND Affiliations.isprimary ='t'
AND Affiliations.ending is null
;

create or replace view Q9_2(pid)
as
select id from people where email in (select email from Q9_1);


create or replace view Q9_3(course,staff)
as
select course , staff from Course_staff where staff in (select pid from Q9_2);

create or replace view Q9_31(subject,staff)
as
select courses.subject,Q9_3.staff from courses,Q9_3
where courses.id = Q9_3.course;

create or replace view Q9_32(code,staff)
as
select distinct code,staff from subjects,Q9_31
where subjects.id = Q9_31.subject;

create or replace view Q9_33(staff,num)
as
select staff,count(code) as num from Q9_32
group by staff;

create or replace view Q9_5(email,pid,num_subjects)
as
select people.email ,people.id, Q9_33.num
from people ,Q9_33
where people.id = Q9_33.staff AND Q9_33.num >= 1;

create or replace view Q9(name, school,email,starting,num_subjects)
as
select Q9_1.name, Q9_1.school,Q9_1.email,Q9_1.starting,Q9_5.num_subjects
from Q9_1,Q9_5
where Q9_1.email = Q9_5.email;


--... SQL statements, possibly using other views/functions defined by you ...
;


-- Q10:

create or replace view Q10_1(code,id, semester, year, term, name, subject, subject_num)
as
select s.code,c.id, c.semester, sem.year, sem.term, s.name, c.subject, count(subject) over (partition by subject) as subject_num
from courses c join semesters sem on sem.id = c.semester 
join subjects s on s.id = c.subject
where s.code ~ '^COMP93'
and (sem.term = 'S1' or sem.term = 'S2') and sem.year >= 2003 and sem.year <= 2012;
 

create or replace view Q10_2(code,mark, student, name, semester, term, year)
as
select code,mark, student, name, semester, term, year from course_enrolments cou
join Q10_1 Q1 on cou.course = Q1.id
where Q1.subject_num = 20
and mark >= 0
;


create or replace view Q10_3(code,mark, student, name, semester, term, year)
as
select code,mark, student, name, semester, term, year from course_enrolments cou
join Q10_1 Q1 on cou.course = Q1.id
where Q1.subject_num = 20
and mark < 85
;


create or replace view Q10_4(code,name,term,year,num1)
as
select  code,name,term,year,
count(*) as num1
from Q10_2
where term = 'S1' 
group by code,name,term,year;


create or replace view Q10_5(code,name,term,year,num2)
as
select code,name,term,year,
count(*) as num2
from Q10_3
where term = 'S1'
group by code,name,term,year;

create or replace view Q10_41(code,name,term,year,num1)
as
select  code,name,term,year,
count(*) as num1
from Q10_2
where term = 'S2' 
group by code,name,term,year;


create or replace view Q10_51(code,name,term,year,num2)
as
select code,name,term,year,
count(*) as num2
from Q10_3
where term = 'S2'
group by code,name,term,year;


create or replace view Q10_6(code,name,term, year,s1_HD_rate)
as
select a1.code,a1.name, a1.term, a1.year,
CAST((b1.num1-1.0*a1.num2)/b1.num1 as  numeric(4,2)) as s1_HD_rate
from Q10_5 a1,Q10_4 b1
where a1.name = b1.name and a1.year = b1.year;

create or replace view Q10_61(code,name,term, year,s2_HD_rate)
as
select a.code,a.name, a.term, a.year,
CAST((b.num1-1.0*a.num2)/b.num1 as  numeric(4,2)) as s2_HD_rate
from Q10_51 a,Q10_41 b
where a.name = b.name and  a.year = b.year;

create or replace view Q10_62(code,name, year, s1_HD_rate, s2_HD_rate)
as
select Q10_61.code,Q10_61.name,Q10_61.year ,Q10_6.s1_HD_rate,Q10_61.s2_HD_rate
from  Q10_61 left outer join Q10_6
on Q10_61.name = Q10_6.name and Q10_61.year = Q10_6.year;

create or replace view Q10(code,name, year, s1_HD_rate, s2_HD_rate)
as
select code,name, substring(cast(year as varchar(4)),3,4), s1_HD_rate, s2_HD_rate from Q10_62;

--... SQL statements, possibly using other views/functions defined by you ...
;