select *
  from Person
limit 100;

select *
  from Person
where Value = 'David Oxley';

  
select Sentence.Sentence, SourceEmailFile.FileName
  from Person,
       PersonSentence,
       Sentence, 
       SourceEmailFile 
where Person.PersonId = PersonSentence.PersonId
  and PersonSentence.SentenceId = Sentence.SentenceId
  and Sentence.SourceEmailFileId = SourceEmailFile.SourceEmailFileId
  and Person.Value = 'David Oxley'
  order by SourceEmailFile.FileName;
  
select Person.Value as 'Person', Organization.Value as 'Organization'
  from AppliesToJurisdictionRelation relation, 
       Organization,
       Person
where relation.OrganizationId = Organization.OrganizationId
  and relation.PersonId = Person.PersonId
  and Person.Value = 'Kenneth L';
  

select Person.Value as 'Person', 
       Organization.Value as 'Organization', 
       Sentence.Sentence
  from AppliesToJurisdictionRelation relation, 
       Organization,
       Person,
       PersonSentence,
       Sentence, 
       SourceEmailFile 
where relation.OrganizationId = Organization.OrganizationId
  and relation.PersonId = Person.PersonId
  and Person.Value = 'Kenneth L'
  and Person.PersonId = PersonSentence.PersonId
  and PersonSentence.SentenceId = Sentence.SentenceId
  and Sentence.SourceEmailFileId = SourceEmailFile.SourceEmailFileId
  and Organization.Value = 'United States District Court'
  



