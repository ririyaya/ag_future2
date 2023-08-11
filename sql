
create or replace
algorithm = UNDEFINED view `koudai`.`xag1h_ma20_ratio` as
select
    `t`.`o` as `o`,
    `t`.`c` as `c`,
    `t`.`h` as `h`,
    `t`.`l` as `l`,
    `t`.`ts` as `ts`,
    `t`.`t` as `t`,
    `t`.`ma20` as `ma20`,
    `t`.`zf` as `zf`,
    `t`.`zf_1` as `zf_1`,
    `t`.`series` as `series`,
    sum((`t`.`c` - `t`.`ma20`)) over (partition by `t`.`series`
order by
    `t`.`ts` ) as `area`,
    sum(`t`.`zf`) over (partition by `t`.`series`
order by
    `t`.`ts` ) as `sum_zf`
from
    (
    select
        `t`.`o` as `o`,
        `t`.`c` as `c`,
        `t`.`h` as `h`,
        `t`.`l` as `l`,
        `t`.`ts` as `ts`,
        `t`.`t` as `t`,
        `t`.`ma20` as `ma20`,
        `t`.`zf` as `zf`,
        `t`.`zf_1` as `zf_1`,
        sum(if((`t`.`zf_1` = if(((`t`.`c` - `t`.`ma20`) > 0), 1, if((`t`.`c` = `t`.`ma20`), 0,-(1)))), 0, 1)) over (
        order by `t`.`ts` ) as `series`
    from
        (
        select
            `t`.`o` as `o`,
            `t`.`c` as `c`,
            `t`.`h` as `h`,
            `t`.`l` as `l`,
            `t`.`ts` as `ts`,
            `t`.`t` as `t`,
            `t`.`ma20` as `ma20`,
            if(((`t`.`c` - `t`.`ma20`) > 0),
            1,
            if((`t`.`c` = `t`.`ma20`),
            0,
            -(1))) as `zf`,
            lag(if(((`t`.`c` - `t`.`ma20`) > 0), 1, if((`t`.`c` = `t`.`ma20`), 0,-(1))), 1) over (
            order by `t`.`ts` ) as `zf_1`
        from
            (
            select
                round(`t1`.`last_c`, 3) as `o`,
                round(`t1`.`c`, 3) as `c`,
                round(`t1`.`h`, 3) as `h`,
                round(`t1`.`l`, 3) as `l`,
                `t1`.`ts` as `ts`,
                `t1`.`t` as `t`,
                round(avg(`t1`.`c`) over (order by `t1`.`ts` rows between 19 preceding and current row) , 3) as `ma20`
            from
                (
                select
                    `t1`.`o` as `o`,
                    `t1`.`c` as `c`,
                    `t1`.`h` as `h`,
                    `t1`.`l` as `l`,
                    `t1`.`ts` as `ts`,
                    `t1`.`t` as `t`,
                    round(lag(`t1`.`c`, 1) over (order by `t1`.`ts` ) , 3) as `last_c`
                from
                    (
                    select
                        distinct `koudai`.`xag1h`.`o` as `o`,
                        `koudai`.`xag1h`.`c` as `c`,
                        `koudai`.`xag1h`.`h` as `h`,
                        `koudai`.`xag1h`.`l` as `l`,
                        `koudai`.`xag1h`.`ts` as `ts`,
                        `koudai`.`xag1h`.`t` as `t`
                    from
                        `koudai`.`xag1h`) `t1`) `t1`) `t`) `t`
    where
        (`t`.`ts` > 1535025600000)) `t`;