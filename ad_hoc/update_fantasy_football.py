import time
from datetime import datetime
import csv
import os
from py_db import db
import argparse
import ast

db = db('personal')

# use the /Users/connorreed/GoogleDrive/Work/Codebase/baseball/ad_hoc/testSQLToHTML.py script to make the tables


base_path = os.getcwd()


def initiate():
    print "\tupdating csvs"
    process_ff()

def process_ff():
    qry = """SET SESSION group_concat_max_len = 100000;

    update fantasy_sports f
    join(
        select f.year
        , f.sport
        , f.league_name
        , f.owner
        , round(100*f.pf/(y.pft/(y.tms)),1) as PF_PLUS
        , if(f.pa is not null, round((y.pft-f.pf)/(y.tms-1),1), null) as xPA
        , f.pa - round((y.pft-f.pf)/(y.tms-1),1) as PA_DIFF
        , round(100*f.pa/((y.pft-f.pf)/(y.tms-1)),1) as PA_PLUS
        
        , (f.pf-y.pf_avg)/(y.pf_std) as PF_z
        , (f.pa - ((y.pft-f.pf)/(y.tms-1))) / (y.xpa_std) as PA_z
        , (2*f.W+1*f.T)/(2*(f.W+f.T+f.L)) as PtsPct
        
        , case
            when f.Sport = 'nfl'
                then 0.1337*( (f.pf-y.pf_avg)/(y.pf_std) ) + 0.5
            when f.Sport = 'mlb'
                then 0.1207*( (f.pf-y.pf_avg)/(y.pf_std) ) + 0.5
        end as xPtsPct # regression based on PF_z vs PtsPct
        , case
            when f.Sport = 'nfl'
                then (0.1337*( (f.pf-y.pf_avg)/(y.pf_std) ) + 0.5) - (2*f.W+1*f.T)/(2*(f.W+f.T+f.L))
            when f.Sport = 'mlb'
                then (0.1207*( (f.pf-y.pf_avg)/(y.pf_std) ) + 0.5) - (2*f.W+1*f.T)/(2*(f.W+f.T+f.L))
        end as PtsPct_Diff
        
        , Approx_NORMSDIST( (f.pf-y.pf_avg)/(y.pf_std) ) as zStrength
        , Approx_NORMSDIST( (f.pa - ((y.pft-f.pf)/(y.tms-1))) / (y.xpa_std) ) as PA_zStrength
        
        , case
            when f.Sport = 'nfl'
                then y.tms*(0.5429-((f.pf-y.pf_avg)/(y.pf_std)*0.2070))
            when f.Sport = 'mlb'
                then y.tms*(0.5442-((f.pf-y.pf_avg)/(y.pf_std)*0.2289))
        end as xRank # linear regression based on PF_z vs. Rank/TotalTeams
        , case
            when f.Sport = 'nfl'
                then f.rank - ( y.tms*(0.5429-((f.pf-y.pf_avg)/(y.pf_std)*0.2070)) )
            when f.Sport = 'mlb'
                then f.rank - ( y.tms*(0.5442-((f.pf-y.pf_avg)/(y.pf_std)*0.2289)) )
        end as Rank_Diff
        
        , case
            when f.Sport = 'nfl' 
                then 1/(1+POW(exp(1), -(-3.1344 + 1.5358 * ( (f.pf-y.pf_avg)/(y.pf_std) ) ) ) ) # logistic regression based on PF_z
            when f.Sport = 'mlb'
                then 1/(1+POW(exp(1), -(-3.0178 + 1.5140 * ( (f.pf-y.pf_avg)/(y.pf_std) ) ) ) )
        end as xTitles
        , case
            when f.Sport = 'nfl'
                then 1/(1+POW(exp(1), -(-2.8695 - 1.1754 * ( (f.pf-y.pf_avg)/(y.pf_std) ) ) ) ) # logistic regression based on PF_z
            when f.Sport = 'mlb'
                then 1/(1+POW(exp(1), -(-4.7637 - 2.7238 * ( (f.pf-y.pf_avg)/(y.pf_std) ) ) ) )
        end as xSackos
        
        from fantasy_sports f
        join(
            select a.*
            , std(f.PA - (a.pft-f.pf)/(a.tms-1)) as xpa_std
            from fantasy_sports f
            join(
                select year
                , sport
                , league_name
                , sum(pf) pft
                , count(*) as tms
                , avg(pf) as pf_avg
                , std(pf) as pf_std
                from fantasy_sports
                group by year, sport, league_name
            ) a using (year, sport, league_name)
            group by year, sport, league_name
        ) y using (year, sport, league_name)
    ) u on (f.year = u.year
        and f.owner = u.owner
        and f.sport = u.sport
        and f.league_name = u.league_name
    )
    set f.PF_PLUS = u.PF_PLUS
    , f.xPA = u.xPA
    , f.PA_DIFF = u.PA_DIFF
    , f.PA_PLUS = u.PA_PLUS
    , f.PF_z = u.PF_z
    , f.PA_z = u.PA_z
    , f.PtsPct = u.PtsPct
    , f.xPtsPct = u.xPtsPct
    , f.zStrength = u.zStrength
    , f.PA_zStrength = u.PA_zStrength
    , f.xRank = u.xRank
    , f.Rank_Diff = u.Rank_Diff
    , f.PtsPct_Diff = u.PtsPct_Diff
    , f.xTitles = u.xTitles
    , f.xSackos = u.xSackos
    ;


    update fantasy_sports f
    join(
        select b.year
        , b.league_name
        , b.sport
        , b.owner
        , b.team_name
        , (100*Approx_NORMSDIST( z_R )
            + 100*Approx_NORMSDIST( z_HR )
            + 100*Approx_NORMSDIST( z_RBI )
            + 100*Approx_NORMSDIST( z_SB )
            + 100*Approx_NORMSDIST( z_OBP )
            + 100*Approx_NORMSDIST( z_SLG )
            + 100*Approx_NORMSDIST( z_IP )
            + 100*Approx_NORMSDIST( z_QS )
            + 100*Approx_NORMSDIST( z_SV )
            + 100*Approx_NORMSDIST( z_ERA )
            + 100*Approx_NORMSDIST( z_WHIP )
            + 100*Approx_NORMSDIST( z_K9 )
        ) as est_PF
        from(
            select f.year
            , f.league_name
            , f.sport
            , f.owner
            , f.team_name
            , (ch.R - a.avg_R)/(a.std_R) as z_R
            , (ch.HR - a.avg_HR)/(a.std_HR) as z_HR
            , (ch.RBI - a.avg_RBI)/(a.std_RBI) as z_RBI
            , (ch.SB - a.avg_SB)/(a.std_SB) as z_SB
            , (ch.OBP - a.avg_OBP)/(a.std_OBP) as z_OBP
            , (ch.SLG - a.avg_SLG)/(a.std_SLG) as z_SLG
            , (ch.IP - a.avg_IP)/(a.std_IP) as z_IP
            , (ch.QS - a.avg_QS)/(a.std_QS) as z_QS
            , (ch.SV - a.avg_SV)/(a.std_SV) as z_SV
            , -1*(ch.ERA - a.avg_ERA)/(a.std_ERA) as z_ERA
            , -1*(ch.WHIP - a.avg_WHIP)/(a.std_WHIP) as z_WHIP
            , (ch.K9 - a.avg_K9)/(a.std_K9) as z_K9
            from fantasy_sports f
            join fantasy_sports_chili_helper ch on (f.year = ch.year and f.team_name = ch.team_name and f.sport = 'mlb' and f.league_name = 'chilistew')
            join(
                select year
                , avg(r) as avg_r
                , std(r) as std_r
                , avg(hr) as avg_hr
                , std(hr) as std_hr
                , avg(rbi) as avg_rbi
                , std(rbi) as std_rbi
                , avg(sb) as avg_sb
                , std(sb) as std_sb
                , avg(obp) as avg_obp
                , std(obp) as std_obp
                , avg(slg) as avg_slg
                , std(slg) as std_slg
                , avg(ip) as avg_ip
                , std(ip) as std_ip
                , avg(qs) as avg_qs
                , std(qs) as std_qs
                , avg(sv) as avg_sv
                , std(sv) as std_sv
                , avg(era) as avg_era
                , std(era) as std_era
                , avg(whip) as avg_whip
                , std(whip) as std_whip
                , avg(k9) as avg_k9
                , std(k9) as std_k9
                from fantasy_sports_chili_helper h
                group by year
            ) a on (f.year = a.year and f.sport = 'mlb' and f.league_name = 'chilistew')
        ) b
    ) c on (f.year = c.year
        and f.league_name = c.league_name
        and f.sport = c.sport
        and f.owner = c.owner
        and f.team_name = c.team_name
    )
    set f.PF = c.est_PF
    ;

    """

    db.query(qry)


    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_fantasy_sports.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["row",
        "year", 
        "finish", 
        "owner", 
        "pick", 
        "W", 
        "L", 
        "W%", 
        "PF", 
        "PA", 
        "PF_PLUS", 
        "PA_PLUS", 
        "avg_PF/G", 
        "xPA", 
        "PA_DIFF", 
        "seasons", 
        "std_finish", 
        "std_PF+", 
        "std_PA+", 
        "total_W", 
        "total_L", 
        "total_PF", 
        "total_PA", 
        "Playoffs", 
        "Podiums", 
        "Titles", 
        "Sackos", 
        "Details"
    ]
    append_csv.writerow(csv_header)
    
    qry = """drop table if exists fantasy_sports_summary;
    create table fantasy_sports_summary as
    select 'Total' AS year
    , ff.owner
    , concat(ff.league_name,'-',ff.sport) as league_name
    , concat(ff.owner , ' - ', ff.league_name, ' (', ff.sport, ')', "\n\n", group_concat(concat('#'
        , if(ff.Rank is not null, if(ff.Rank % 1 = 0, round(ff.rank,0), ff.rank), '??')
        , " (", ff.Year
        , if(ff.PICK is not null, concat(", pick #", ff.PICK), '')
        , if(ff.W is not null, concat(', ', ff.W, "-", ff.L, if(ff.T>0, concat("-", ff.T), "")), '')
        , if(ff.PF is not null, concat(", ", round(ff.PF_z,2), " PF_z"
            , ", ", round(100*ff.zStrength,0), " zStrength"
            , ", ", round(100*ff.PF/lg.lg_PF), " PF+"
            , ", ", round(ff.xRank,1), " xRank"
            , ", ", round(ff.xTitles,2), " xTitles"
            , ", ", round(ff.xSackos,2), " xSackos"
            ), '')
        , ')'
        , if(ff.Team_Name is null, '', concat('\n\t-', ff.Team_Name))
    ) order by ff.Year desc separator " \n\n ")) as Details
    , round(avg(ff.RANK),1) as finish
    , round(avg(ff.PICK),1) as pick
    , round(avg(ff.W),1) as W
    , round(avg(ff.L),1) as L
    , round(avg(ff.T),1) as T
    , round(avg(ff.PF),2) as PF
    , round(avg(ff.PA),2) as PA
    , round(sum(2*ff.W+ff.T)/sum(2*(ff.W+ff.L+ff.T)),3) as "PtsPct"
    
    , round(sum(ff.xTitles),2) as xTitles
    , round(sum(ff.xSackos),2) as xSackos
    
    , round(avg(ff.PF_z),2) as PF_z
    , round(avg(100*ff.zStrength),0) as zStrength
    , round(avg(ff.xRank),1) as xRank
    , round(avg(ff.Rank_Diff),1) as RankDiff

    , round(avg(ff.xPtsPct),3) as xPtsPct
    , round(avg(ff.PtsPct_Diff),3) as PtsPctDiff

    
    , round(avg(ff.PA_z),2) as PA_z
    , round(avg(100*ff.PA_zStrength),0) as PA_zStrength
    , round(avg(ff.xPA),1) as xPA
    , sum(ff.PA_DIFF) as PA_DIFF
    
    , round(avg(ff.PF_PLUS),0) as "PF+"
    , round(avg(ff.PA_PLUS),0) as "PA+"
    , cast( concat(count(distinct ff.year), ' (', min(ff.year), ' - ', max(ff.year), ')') as char)  AS seasons
    , sum( greatest(least(ff.Playoff_Teams - ff.Rank + 1, 1), 0) ) as Playoffs
    , sum( greatest(least(3 - ff.Rank + 1, 1), 0) ) as Podiums
    , sum( greatest(least(1 - ff.Rank + 1, 1), 0) ) as Titles
    , sum( greatest(least(ff.Rank - lg.sacko + 1, 1), 0) ) as Sackos
    , round(std(ff.RANK),1) as std_finish
    , sum(ff.W) as total_W
    , sum(ff.L) as total_L
    , sum(ff.PF) as total_PF
    , sum(ff.PA) as total_PA
    , group_concat(distinct ff.team_name order by ff.year asc separator '\n') as team_name
    from fantasy_sports ff
    join (
        select ff2.Year
        , ff2.sport
        , ff2.league_name
        , avg(ff2.PF) as lg_PF
        , count(distinct ff2.Owner, ff2.Team_Name) as sacko 
        from fantasy_sports ff2
        group by year, sport, league_name
    ) lg using (year, sport, league_name)
    group by owner, sport, league_name
    union all
    select f.year as year
    , f.owner
    , concat(f.league_name,'-',f.sport) as league_name
    , NULL as Details
    , f.rank as finish
    , f.pick
    , f.W
    , f.L
    , f.T
    , f.PF
    , f.PA
    , round((2*f.W+1*f.T)/(2*(f.W+f.T+f.L)),3) as `PtsPct`
    
    , round(f.xTitles,2) as xTitles
    , round(f.xSackos,2) as xSackos
    
    , round(f.PF_z,2) as PF_z
    , round(100*f.zStrength,0) as zStrength
    , round(f.xRank,1) as xRank
    , round(f.Rank_Diff,1) as RankDiff

    , round(f.xPtsPct,3) as xPtsPct
    , round(f.PtsPct_Diff,3) as PtsPctDiff

    
    , round(f.PA_z,2) as PA_z
    , round(100*f.PA_zStrength,0) as PA_zStrength
    , f.xPA
    , f.PA_DIFF

    , round(f.PF_PLUS,0) as `PF+`
    , round(f.PA_PLUS,0) as `PA+`
    , NULL as seasons
    , greatest(least(f.Playoff_Teams - f.Rank + 1, 1), 0) as Playoffs
    , greatest(least(3 - f.Rank + 1, 1), 0) as Podiums
    , greatest(least(1 - f.Rank + 1, 1), 0) as Titles
    , greatest(least(f.Rank - lg.sacko + 1, 1), 0) as Sackos
    , NULL as std_finish
    , NULL as total_W
    , NULL as total_L
    , NULL as total_PF
    , NULL as total_PA
    , f.team_name
    from fantasy_sports f
    join (
        select ff2.Year
        , ff2.sport
        , ff2.league_name
        , avg(ff2.PF) as lg_PF
        , count(distinct ff2.Owner, ff2.Team_Name) as sacko 
        from fantasy_sports ff2
        group by year, sport, league_name
    ) lg using (year, sport, league_name)
    order by year desc, league_name, finish asc
    ;"""

    res = db.query(qry)

    r = 0
    for row in res:
        r += 1
        row = list(row)
        row.insert(0,r)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val]).replace("<o>","").replace("<P>","").replace("\n","  ") + '"'
        append_csv.writerow(row)


if __name__ == "__main__":     
    initiate()
