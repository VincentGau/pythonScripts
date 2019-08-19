-- 删除冗余数据
delete from authors where authorid in (select authorid from authors group by authorid having count(1) >  1) and workscicount = 0 and worksshicount = 0 and worksqucount = 0 and workswencount = 0 and worksfucount = 0;

-- 继续删除冗余数据
select * from authors where authorid in (select authorid from authors group by authorid having count(1) >  1);
delete from authors where objectid in('598ecef91b69e60058cd83f8', '5a404ccb44d9040037a56c4c');