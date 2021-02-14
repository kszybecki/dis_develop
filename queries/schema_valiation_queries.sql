-- relational schema validation 

select count(distinct Value)  as 'Relation table Counts'
from validation.RelRelation
union all
SELECT count(*) FROM enron_relational.sqlite_master
WHERE type='table'
 and name like '%Relation';

select count(distinct Value) as 'Location Counts' 
from validation.RelLocation
union all
select count(distinct Value) 
from enron_relational.Location;

select count(distinct Value) as 'Organization  Counts' 
from validation.RelOrganization
union all
select count(distinct Value) 
from enron_relational.Organization;

select count(distinct Value) as 'Person Counts' 
from validation.RelPerson
union all
select count(distinct Value) 
from enron_relational.Person;


-- data warehouse schema validation 

select count(distinct Value) as 'Location Counts' 
from validation.DwLocation
union all
select count(distinct Value) 
from enron_data_warehouse.DimLocation;

select count(distinct Value) as 'Organization  Counts' 
from validation.DwOrganization
union all
select count(distinct Value) 
from enron_data_warehouse.DimOrganization;

select count(distinct Value) as 'Person Counts' 
from validation.DwPerson
union all
select count(distinct Value) 
from enron_data_warehouse.DimPerson;




