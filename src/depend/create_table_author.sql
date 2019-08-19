-- postgresql
create table Authors(
	ObjectId text primary key, 
	AuthorId int, 
	BirthYear text, 
	DeathYear text, 
	AuthorDesc text, 
	AuthorDescTr text, 
	Dynasty text, 
	DynastyTr text, 
	AuthorName text, 
	AuthorNameTr text, 
	WorksCiCount integer, 
	WorksShiCount integer, 
	WorksQuCount integer, 
	WorksWenCount integer, 
	WorksFuCount integer, 
	WorksCount integer
)