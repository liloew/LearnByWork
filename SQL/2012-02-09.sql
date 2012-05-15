SELECT ID,Name,CountryCode from city;
select ID,District from city where ID <= 100 and ID >= 14;
select ID,District from city where ID between 10 and 34;

select ID,District from city
where
{
	select * from city
	where ID between 15 and 40;
}