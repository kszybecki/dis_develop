
select count(distinct Value) as 'Location Counts' from RelLocation
union all
select count(distinct Value) from enron_relational.Location;

select count(distinct Value) as 'Organization  Counts' from RelOrganization
union all
select count(distinct Value) from enron_relational.Organization;

select count(distinct Value) as 'Person Counts' from RelPerson
union all
select count(distinct Value) from enron_relational.Person;

select count(distinct Value) from RelRelation as 'Relation table Counts'
union all
SELECT count(*) FROM enron_relational.sqlite_master
WHERE type='table'
 and name like '%Relation';

