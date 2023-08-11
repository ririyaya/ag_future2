
select
    o,
    c,
    h,
    l,
    ts ts,
    t,
    ma20 ma20,
    zf zf,
    zf_1 zf_1,
    series series,
    sum(round((- ma20)/ma20*100,2)) over (partition by series order by ts ) area, sum(zf) over (partition by series order by ts) sum_zf
from
    (
    select
        o,
        c,
        h,
        l,
        ts,
        t,
        ma20 ,
        zf zf,
        zf_1,
        sum(if((zf_1 = if(((- ma20) > 0), 1, if((= ma20), 0,-(1)))), 0, 1)) over (order by ts ) series
    from
        (
        select
            o,
            c,
            h,
            l,
            ts,
            t,
            ma20,
			if(((- ma20) > 0),1,if((= ma20),0,-(1))) zf,
            lag(if(((- ma20) > 0), 1, if((= ma20), 0,-(1))), 1) over ( order by ts ) zf_1
        from
            (
            select
                round(last_c, 3) o,
                round( 3) c,
                round( 3) h,
                round( 3) l,
                ts,
                t,
                round(avg( over (order by ts rows between 19 preceding and current row) , 3) ma20
            from
                (
                select
                    o,
                    c,
                    h,
                    l,
                    ts,
                    t,
                    round(lag( 1) over (order by ts ) , 3) last_c
                from
                    (
                    select
                        distinct  o,
                         c,
                         h,
                         l,
						 ts,
                         t
                    from
                        )   t) t
    where
        (ts > 1535025600000)) t
