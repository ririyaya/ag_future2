-- koudai.xag1h_ma1_ratio source

create or replace
algorithm = UNDEFINED view `koudai`.`xag1h_ma1_ratio` as
select
    `t3`.`o` as `o`,
    `t3`.`c` as `c`,
    `t3`.`h` as `h`,
    `t3`.`l` as `l`,
    `t3`.`ts` as `ts`,
    `t3`.`dt` as `dt`,
    `t3`.`min10` as `min10`,
    `t3`.`max10` as `max10`,
    `t3`.`ma10` as `ma10`,
    `t3`.`ratio` as `ratio`,
    `t3`.`up_down` as `up_down`,
    `t3`.`up_down_lag_1` as `up_down_lag_1`,
    `t3`.`series` as `series`,
    sum(`t3`.`ratio`) over (partition by `t3`.`series`
order by
    `t3`.`ts` ) as `series_ratio`,
    count(1) over (partition by `t3`.`series`
order by
    `t3`.`ts` ) as `series_count`,
    row_number() over (
    order by `t3`.`ts` ) as `row_nber`,
    sum(`t3`.`up_down`) over (partition by `t3`.`series`
order by
    `t3`.`ts` ) as `trend`
from
    (
    select
        `t2`.`o` as `o`,
        `t2`.`c` as `c`,
        `t2`.`h` as `h`,
        `t2`.`l` as `l`,
        `t2`.`ts` as `ts`,
        `t2`.`dt` as `dt`,
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
            `t1`.`dt` as `dt`,
            min(`t1`.`c`) over (
            order by `t1`.`ts` rows between 9 preceding and current row) as `min10`,
            max(`t1`.`c`) over (
            order by `t1`.`ts` rows between 9 preceding and current row) as `max10`,
            round(avg(`t1`.`c`) over (order by `t1`.`ts` rows between 9 preceding and current row) , 3) as `ma10`,
            round((((`t1`.`c` - `t1`.`o`) / `t1`.`o`) * 100), 2) as `ratio`,
            if(abs((((`t1`.`c` - `t1`.`o`) / `t1`.`o`) > 0.00001)),
            if((`t1`.`c` > `t1`.`o`),
            1,
            if((`t1`.`c` < `t1`.`o`),
            -(1),
            0)),
            0) as `up_down`,
            lag(if(abs((((`t1`.`c` - `t1`.`o`) / `t1`.`o`) > 0.00001)), if((`t1`.`c` > `t1`.`o`), 1, if((`t1`.`c` < `t1`.`o`),-(1), 0)), 0), 1) over (
            order by `t1`.`ts` ) as `up_down_lag_1`
        from
            (
            select
                distinct round(`koudai`.`xag1h`.`c`, 2) as `c`,
                round(`koudai`.`xag1h`.`h`, 2) as `h`,
                round(`koudai`.`xag1h`.`l`, 2) as `l`,
                lag(round(`koudai`.`xag1h`.`c`, 2), 1) over (
                order by `koudai`.`xag1h`.`ts` ) as `o`,
                `koudai`.`xag1h`.`ts` as `ts`,
                date_format(from_unixtime((`koudai`.`xag1h`.`ts` / 1000)), '%Y-%m-%d %H:%i') as `dt`,
                `koudai`.`xag1h`.`v` as `v`
            from
                `koudai`.`xag1h`
            where
                (((`koudai`.`xag1h`.`ts` between 1545688800000 and 1545768000000) = 0)
                    and ((`koudai`.`xag1h`.`ts` between 1546293600000 and 1546372800000) = 0)
                        and ((`koudai`.`xag1h`.`ts` between 1577833200000 and 1577912400000) = 0)
                            and ((`koudai`.`xag1h`.`ts` between 1577228400000 and 1577307600000) = 0))) `t1`
        where
            (`t1`.`ts` > 0)) `t2`) `t3`;



-- koudai.f_ag_15m_v source

create or replace
algorithm = UNDEFINED view `koudai`.`f_ag_15m_v` as

select *,
sum(serie_up)over(order by ts)series
,lead(serie_up)over(order by ts)serie_down
,(c-o)/o as raito
from
(
select
    date_format(from_unixtime((((`t`.`ts` / 1000) + 86400) - (3600 * 15))), '%Y-%m-%d') as `d`,
    date_format(from_unixtime((`t`.`ts` / 1000)), '%H') as `hour`,
    date_format(from_unixtime(((`t`.`ts` / 1000) - (3600 * 15))), '%w') as `week`,
    ((((`t`.`ts` / 1000) - 46800) % 86400) / (60 * 15)) as `num_15`,
    row_number() over (partition by date_format(from_unixtime(((`t`.`ts` / 1000) - (3600 * 15))), '%Y-%m-%d')
order by
    `t`.`ts` ) as `rn`,
    `t`.`c` as `c`,
    `t`.`v` as `v`,
    `t`.`h` as `h`,
    `t`.`l` as `l`,
    `t`.`o` as `o`,
    `t`.`ts` as `ts`,
    if(((ts-last_ts)/1000/60/60)<4,0,1)serie_up
from
    (
    select
    c,t,ts,h,l,v
    ,lag(ts)over(order by ts)last_ts
    ,lag(c)over(order by ts)o
    from
    (
    select
        distinct `koudai`.`f_ag_15m`.`c` as `c`,
        `koudai`.`f_ag_15m`.`t` as `t`,
        `koudai`.`f_ag_15m`.`ts` as `ts`,
        `koudai`.`f_ag_15m`.`o` as `o`,
        `koudai`.`f_ag_15m`.`h` as `h`,
        `koudai`.`f_ag_15m`.`l` as `l`,
        `koudai`.`f_ag_15m`.`v` as `v`
    from
        `koudai`.`f_ag_15m`) `t`
)
    t
order by
    `t`.`ts` desc)t ;



-- koudai.xag1h_ma20 source

create or replace
algorithm = UNDEFINED view `koudai`.`xag1h_ma20` as
select
    `t`.`o` as `o`,
    `t`.`c` as `c`,
    `t`.`h` as `h`,
    `t`.`l` as `l`,
    `t`.`ts` as `ts`,
    `t`.`dt` as `dt`,
    date_format(from_unixtime((`t`.`ts` / 1000)), '%H') as `hour`,
    `t`.`ma20` as `ma20`,
    `t`.`up_down` as `up_down`,
    `t`.`up_down_lag1` as `up_down_lag1`,
    `t`.`series` as `series`,
    sum((`t`.`c` - `t`.`ma20`)) over (partition by `t`.`series`
order by
    `t`.`ts` ) as `area`,
    sum(`t`.`up_down`) over (partition by `t`.`series`
order by
    `t`.`ts` ) as `trend`,
    sum(round((((`t`.`c` - `t`.`ma20`) / `t`.`ma20`) * 100), 2)) over (partition by `t`.`series`
order by
    `t`.`ts` ) as `area_ratio`
from
    (
    select
        `t`.`o` as `o`,
        `t`.`c` as `c`,
        `t`.`h` as `h`,
        `t`.`l` as `l`,
        `t`.`ts` as `ts`,
        `t`.`dt` as `dt`,
        `t`.`ma20` as `ma20`,
        `t`.`up_down` as `up_down`,
        `t`.`up_down_lag1` as `up_down_lag1`,
        sum(if((`t`.`up_down_lag1` = `t`.`up_down`), 0, 1)) over (
        order by `t`.`ts` ) as `series`
    from
        (
        select
            `t`.`o` as `o`,
            `t`.`c` as `c`,
            `t`.`h` as `h`,
            `t`.`l` as `l`,
            `t`.`ts` as `ts`,
            `t`.`dt` as `dt`,
            `t`.`ma20` as `ma20`,
            if(((`t`.`c` - `t`.`ma20`) > 0),
            1,
            if((`t`.`c` = `t`.`ma20`),
            0,
            -(1))) as `up_down`,
            lag(if(((`t`.`c` - `t`.`ma20`) > 0), 1, if((`t`.`c` = `t`.`ma20`), 0,-(1))), 1) over (
            order by `t`.`ts` ) as `up_down_lag1`
        from
            (
            select
                round(`t1`.`last_c`, 3) as `o`,
                round(`t1`.`c`, 3) as `c`,
                round(`t1`.`h`, 3) as `h`,
                round(`t1`.`l`, 3) as `l`,
                `t1`.`ts` as `ts`,
                `t1`.`dt` as `dt`,
                round(avg(`t1`.`c`) over (order by `t1`.`ts` rows between 19 preceding and current row) , 3) as `ma20`
            from
                (
                select
                    `t1`.`o` as `o`,
                    `t1`.`c` as `c`,
                    `t1`.`h` as `h`,
                    `t1`.`l` as `l`,
                    `t1`.`ts` as `ts`,
                    `t1`.`dt` as `dt`,
                    round(lag(`t1`.`c`, 1) over (order by `t1`.`ts` ) , 3) as `last_c`
                from
                    (
                    select
                        distinct `koudai`.`xag1h`.`o` as `o`,
                        `koudai`.`xag1h`.`c` as `c`,
                        `koudai`.`xag1h`.`h` as `h`,
                        `koudai`.`xag1h`.`l` as `l`,
                        `koudai`.`xag1h`.`ts` as `ts`,
                        date_format(from_unixtime((`koudai`.`xag1h`.`ts` / 1000)), '%Y-%m-%d %H:%i') as `dt`
                    from
                        `koudai`.`xag1h`
                    where
                        (((`koudai`.`xag1h`.`ts` between 1545688800000 and 1545768000000) = 0)
                            and ((`koudai`.`xag1h`.`ts` between 1546293600000 and 1546372800000) = 0)
                                and ((`koudai`.`xag1h`.`ts` between 1577833200000 and 1577912400000) = 0)
                                    and ((`koudai`.`xag1h`.`ts` between 1577228400000 and 1577307600000) = 0))) `t1`) `t1`) `t`) `t`
    where
        (`t`.`ts` > 1535025600000)) `t`;



-- koudai.fag15m_ma1_ratio source

create or replace
algorithm = UNDEFINED view `koudai`.`fag15m_ma1_ratio` as
select
    `t3`.`o` as `o`,
    `t3`.`c` as `c`,
    `t3`.`h` as `h`,
    `t3`.`l` as `l`,
    `t3`.`v` as `v`,
    `t3`.`ts` as `ts`,
    `t3`.`dt` as `dt`,
    `t3`.`min10` as `min10`,
    `t3`.`max10` as `max10`,
    `t3`.`ma10` as `ma10`,
    `t3`.`ratio` as `ratio`,
    `t3`.`up_down` as `up_down`,
    `t3`.`up_down_lag_1` as `up_down_lag_1`,
    `t3`.`series` as `series`,
    sum(`t3`.`ratio`) over (partition by `t3`.`series`
order by
    `t3`.`ts` ) as `series_ratio`,
    count(1) over (partition by `t3`.`series`
order by
    `t3`.`ts` ) as `series_count`,
    row_number() over (
    order by `t3`.`ts` ) as `row_nber`
from
    (
    select
        `t2`.`o` as `o`,
        `t2`.`c` as `c`,
        `t2`.`h` as `h`,
        `t2`.`l` as `l`,
        `t2`.`v` as `v`,
        `t2`.`ts` as `ts`,
        `t2`.`dt` as `dt`,
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
            `t1`.`v` as `v`,
            `t1`.`ts` as `ts`,
            `t1`.`dt` as `dt`,
            min(`t1`.`c`) over (
            order by `t1`.`ts` rows between 9 preceding and current row) as `min10`,
            max(`t1`.`c`) over (
            order by `t1`.`ts` rows between 9 preceding and current row) as `max10`,
            round(avg(`t1`.`c`) over (order by `t1`.`ts` rows between 9 preceding and current row) , 3) as `ma10`,
            round((((`t1`.`c` - `t1`.`o`) / `t1`.`o`) * 100), 2) as `ratio`,
            if(abs((((`t1`.`c` - `t1`.`o`) / `t1`.`o`) > 0.001)),
            if((`t1`.`c` > `t1`.`o`),
            1,
            if((`t1`.`c` < `t1`.`o`),
            -(1),
            0)),
            0) as `up_down`,
            lag(if(abs((((`t1`.`c` - `t1`.`o`) / `t1`.`o`) > 0.001)), if((`t1`.`c` > `t1`.`o`), 1, if((`t1`.`c` < `t1`.`o`),-(1), 0)), 0), 1) over (
            order by `t1`.`ts` ) as `up_down_lag_1`
        from
            (
            select
                distinct round(`fam`.`c`, 2) as `c`,
                round(`fam`.`h`, 2) as `h`,
                round(`fam`.`l`, 2) as `l`,
                lag(round(`fam`.`c`, 2), 1) over (
                order by `fam`.`ts` ) as `o`,
                `fam`.`ts` as `ts`,
                date_format(from_unixtime((`fam`.`ts` / 1000)), '%Y-%m-%d %H:%i') as `dt`,
                `fam`.`v` as `v`
            from
                `koudai`.`f_ag_15m` `fam`) `t1`
        where
            (`t1`.`ts` > 0)) `t2`) `t3`;


