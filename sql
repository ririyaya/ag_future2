-- koudai.xag1h_ma1_ratio source

create or replace
algorithm = UNDEFINED view `koudai`.`xag1h_ma1_ratio` as
select *
,
	sum(ratio)over (partition by series order by ts)series_ratio
	,count(1)over (partition by series order by ts)series_count
from (select
    `t2`.`o` as `o`,
    `t2`.`c` as `c`,
    `t2`.`h` as `h`,
    `t2`.`l` as `l`,
    `t2`.`ts` as `ts`,
    `t2`.`t` as `t`,
    `t2`.`min10` as `min10`,
    `t2`.`max10` as `max10`,
    `t2`.`ma10` as `ma10`,
    `t2`.`ratio` as `ratio`,
    `t2`.`up_down` as `up_down`,
    `t2`.`up_down_lag_1` as `up_down_lag_1`,
    sum(if((`t2`.`up_down` = `t2`.`up_down_lag_1`), 0, 1)) over (
    order by `t2`.`ts` ) as `series`
from
    (
    select
        `t1`.`o` as `o`,
        `t1`.`c` as `c`,
        `t1`.`h` as `h`,
        `t1`.`l` as `l`,
        `t1`.`ts` as `ts`,
        `t1`.`t` as `t`,
        min(`t1`.`c`) over (
        order by `t1`.`ts` rows between 9 preceding and current row) as `min10`,
        max(`t1`.`c`) over (
        order by `t1`.`ts` rows between 9 preceding and current row) as `max10`,
        round(avg(`t1`.`c`) over (order by `t1`.`ts` rows between 9 preceding and current row) , 3) as `ma10`,
        round((((`t1`.`c` - `t1`.`o`) / `t1`.`o`) * 100), 2) as `ratio`,
--         if((`t1`.`c` > `t1`.`o`),
--         1,
--         if((`t1`.`c` < `t1`.`o`),
--         -(1),
--         0)) as `up_down`,
--         lag(if((`t1`.`c` > `t1`.`o`), 1, if((`t1`.`c` < `t1`.`o`),-(1), 0)), 1) over (
--         order by `t1`.`ts` ) as `up_down_lag_1`
        if(abs((c-o)/o>0.001),if(c>o,1,if(c<o,-1,0)),0) as up_down,
	    lag(if(abs((c-o)/o>0.001),if(c>o,1,if(c<o,-1,0)),0),1)over (order by ts)as up_down_lag_1
    from
        (
        select
            distinct round(`koudai`.`xag1h`.`c`, 2) as `c`,
            round(`koudai`.`xag1h`.`h`, 2) as `h`,
            round(`koudai`.`xag1h`.`l`, 2) as `l`,
            lag(round(`koudai`.`xag1h`.`c`, 2), 1) over (
            order by `koudai`.`xag1h`.`ts` ) as `o`,
            `koudai`.`xag1h`.`ts` as `ts`,
            from_unixtime(ts/1000,'%Y-%m-%d %H:%i') as `t`,
            `koudai`.`xag1h`.`v` as `v`
        from
            `koudai`.`xag1h` ) `t1`
            where ts>0) `t2`
      )t3  ;