/*
Приложению поступают данные в виде POST запросов (в несколько потоков) с информацией о населении, где каждая запись содержит информацию об одном человеке: пол, дата рождения, регион РФ (числовой код), доход (рублей в месяц). Необходимо реализовать структуру и приложение для хранения и обработки данных из входящих сообщений с разделением (разные таблицы) по полу с сохранением сквозного ИД входящего сообщения (уникального числового, присваиваемого приложением в момент получения информации), а также агрегированной информации о всём населении в разбивке по регионам РФ и суммарно для всей территории РФ (обновление статистики при поступлении каждого сообщения):

количество трудоспособного (только по возрасту) населения (чел. и % от населения региона)
средний уровень дохода трудоспособного населения (рублей в месяц)
максимальный уровень дохода (рублей в месяц)
количество безработных (чел. и % от трудоспособного населения региона), если считать, что безработным является человек в трудоспособном возрасте без указания дохода.
Границы трудоспособного населения (условно) - женщины в возрасте от 18 до 55 лет, мужчины – от 18 до 60 лет.
*/

-- select * from pb_info_people order by id_info desc
create table if not exists pb_info_people (
	id_info bigint generated always as identity,
	gender	char(3)	not null check (gender in ('Man','Fem')),
	dt_born	date		not null,
	region	numeric(10) not null,
	profit	numeric(25,2) default 0
)
	partition by list (gender);

create table if not exists pb_info_people_m partition of pb_info_people
	for values in ('Man');
create table if not exists pb_info_people_f partition of pb_info_people
	for values in ('Fem');

--select * from pb_info_people_aggr order by region
create table if not exists pb_info_people_aggr (
	region					numeric(10) 	not null default 0,
	workers_cnt 		numeric(15)		not null default 0,
	workers_prc 		numeric(5,2)	not null default 0,
	avg_income			numeric(25,2)	not null default 0,
	max_income			numeric(25,2)	not null default 0,
	unemployed_cnt 	numeric(15)		not null default 0,
	unemployed_prc 	numeric(5,2)	not null default 0
)

create unique index if not exists idx_unique_region on pb_info_people_aggr (region);

------------------------------------------------------------------------------------------------------

select fnc_pb_setinfo('Man', '23-01-1990',	'23',	'20100.50');
select fnc_pb_setinfo('Fem', '01-03-2003',	'50',	'63000.00');
select fnc_pb_setinfo('Man', '12-08-1994',	'50',	'45000.00');
select fnc_pb_setinfo('Fem', '24-01-1990',	'50',	'54000.00');
select fnc_pb_setinfo('Man', '23-01-1955',	'50',	'77000.00');
select fnc_pb_setinfo('Fem', '23-01-1967',	'50',	'35000.50');
select fnc_pb_setinfo('Man', '05-01-1996',	'50',	'63000.00');
select fnc_pb_setinfo('Man', '01-02-1991',	'44',	'0.00');
select fnc_pb_setinfo('Fem', '02-03-1992',	'44',	'17000.00');
select fnc_pb_setinfo('Man', '03-04-2001',	'44',	'19000.00');
select fnc_pb_setinfo('Fem', '04-05-2004',	'23',	'25000.00');
select fnc_pb_setinfo('Man', '05-06-1993',	'77',	'0.0');
select fnc_pb_setinfo('Fem', '06-07-1989',	'77',	'34000.00');
select fnc_pb_setinfo('Man', '07-08-1977',	'77',	'56000.00');
select fnc_pb_setinfo('Fem', '08-09-1978',	'77',	'44000.00');

select fnc_pb_setinfo('Fem', '10-07-1978',	'1',	'0.00');
select fnc_pb_setinfo('Fem', '10-07-1978',	'1',	'16000.00');
select fnc_pb_setinfo('Man', '10-07-1988',	'1',	'25000.00');
select fnc_pb_setinfo('Man', '17-10-1997',	'1',	'0.00');
select fnc_pb_setinfo('Fem', '17-10-1923',	'1',	'0.00');

select fnc_pb_setinfo('Fem', '09-11-2000',	'77',	'0.00');
select fnc_pb_setinfo('Man', '11-12-1999',	'23',	'0.00');

--drop function fnc_pb_setinfo
create or replace function aggr.fnc_pb_setinfo(in p_gnd	varchar, in p_dt	varchar,	p_rgn	varchar,	p_prf	varchar)  returns varchar  -- p_gnd - пол ('Man' или 'Fem'), p_dt - дата рождения в формате dd-mm-yyyy, p_rgn - регион России (в числовом формате), p_prf - доход за месяц (в формате 99999999999999999999999.99)
as $$
declare
    sql_str text;
    v_dt date;
		v_rgn numeric(10);
		v_prf numeric(25,2);
    v_id bigint;
begin
		if not lower(p_gnd) in ('man', 'fem') then
			return 'Неверный параметр p_gnd - '||coalesce(p_gnd,'null')||' ! Должен быть "Man" или "Fem"'::varchar;
		end if;
	
		v_dt 	:= to_date(p_dt,'dd-mm-yyyy');
		v_rgn := to_number(p_rgn, '9999999999');
		v_prf := to_number(p_prf, '99999999999999999999999.99');
		
		insert into aggr.pb_info_people (gender,	dt_born,	region,	profit)
				values (p_gnd,	v_dt,	v_rgn,	v_prf) returning id_info into v_id;

    create temporary table if not exists tbl_agg(
			region			numeric(10) 	not null default 0,
			act_people 	numeric(15)		not null default 0,
			prc_act 		numeric(5,2)	not null default 0,
			avg_pf			numeric(25,2)	not null default 0,
			max_pf			numeric(25,2)	not null default 0,
			cnt_unemp 	numeric(15)		not null default 0,
			prc_unemp 	numeric(5,2)	not null default 0
    ) on commit preserve rows;
		
		insert into	tbl_agg	(region,	act_people,	prc_act,	avg_pf,	max_pf,	cnt_unemp,	prc_unemp)
		select	distinct 
				a.region,
				a.act_people,
				((a.act_people::numeric(15,2)/a.people::numeric(15,2))*100)::numeric(15,2) prc_act,
				(a.sum_pf::numeric(25,2)/a.act_people::numeric(25,2))::numeric(25,2) avg_pf,
				a.max_pf::numeric(15,2),
				a.cnt_unemp,
				((a.cnt_unemp::numeric(15,2)/a.act_people::numeric(15,2))*100)::numeric(15,2) prc_unemp
		from (
			select
				region,
				sum(case	when lower(gender) = 'man' and (current_date - dt_born)/365.0 between 18 and 60 then  1
									when lower(gender) = 'fem' and (current_date - dt_born)/365.0 between 18 and 55 then  1
									else 0 
						end) over (partition by region) act_people,
				count(*) over (partition by region) people,
				sum(profit) over (partition by region) sum_pf,
				max(profit) over (partition by region) max_pf,
				sum(case	when lower(gender) = 'man' and (current_date - dt_born)/365.0 between 18 and 60 and profit=0 then  1
									when lower(gender) = 'fem' and (current_date - dt_born)/365.0 between 18 and 55 and profit=0 then  1
									else 0 
						end) over (partition by region) cnt_unemp
			from aggr.pb_info_people
			union all
			select
				99999 region,  ---- По всей России
				sum(case	when lower(gender) = 'man' and (current_date - dt_born)/365.0 between 18 and 60 then  1
									when lower(gender) = 'fem' and (current_date - dt_born)/365.0 between 18 and 55 then  1
									else 0 
						end) over () act_people_all,
				count(*) over () people_all,
				sum(profit) over () sum_pf_all,
				max(profit) over () max_pf_all,
				sum(case	when lower(gender) = 'man' and (current_date - dt_born)/365.0 between 18 and 60 and profit=0 then  1
									when lower(gender) = 'fem' and (current_date - dt_born)/365.0 between 18 and 55 and profit=0 then  1
									else 0 
						end) over () cnt_unemp_all
			from aggr.pb_info_people
			) a;

		insert into aggr.pb_info_people_aggr	 (region,	workers_cnt,	workers_prc,	avg_income,	max_income,	unemployed_cnt,	unemployed_prc)
		select	region,	act_people,	prc_act,	avg_pf,	max_pf,	cnt_unemp,	prc_unemp
			from	tbl_agg 
			on conflict do nothing;

		with tbl as (
			select	region,	act_people,	prc_act,	avg_pf,	max_pf,	cnt_unemp,	prc_unemp
				from	tbl_agg 
		)
		update aggr.pb_info_people_aggr	m set	workers_cnt = tbl.act_people,
																			workers_prc 		= tbl.prc_act,
																			avg_income			=	tbl.avg_pf,
																			max_income			=	tbl.max_pf,
																			unemployed_cnt 	=	tbl.cnt_unemp,
																			unemployed_prc	=	tbl.prc_unemp
			from tbl
		where m.region=tbl.region;

		drop table if exists tbl_agg;
		
		return 'Inserting id_info = '||v_id||' and upsert	pb_info_people_aggr!'::varchar;

exception when others
    then
	 return '!!! Ошибка '||sqlerrm||' !!!'::varchar;
end;
$$ language plpgsql;
