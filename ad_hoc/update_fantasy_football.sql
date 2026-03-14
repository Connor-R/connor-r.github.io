SET SESSION group_concat_max_len = 100000;


update fantasy_sports_DEADLYACCURATE d
join(
    select d.year, d.sport, d.league_name, d.owner
    , ( if(d.Above_Replacement is not null, d.Above_Replacement, d.Projected_Points) -a.proj_avg)/(a.proj_std) as draft_z
    , ( d.Above_Expected -a.AE_avg)/(a.AE_std) as AE_z
    , ( d.Hitter_Dollars -a.Hitter_avg)/(a.Hitter_std) as Hitter_z
    , ( d.Pitcher_Dollars -a.Pitcher_std)/(a.Pitcher_std) as Pitcher_z
    from fantasy_sports_DEADLYACCURATE d
    join(
        select year
        , sport
        , league_name
        , avg(if(d.Above_Replacement is not null, d.Above_Replacement, d.Projected_Points)) as proj_avg
        , std(if(d.Above_Replacement is not null, d.Above_Replacement, d.Projected_Points)) as proj_std
        , avg(d.Above_Expected) as AE_avg
        , std(d.Above_Expected) as AE_std
        , avg(d.Hitter_Dollars) as Hitter_avg
        , std(d.Hitter_Dollars) as Hitter_std
        , avg(d.Pitcher_Dollars) as Pitcher_avg
        , std(d.Pitcher_Dollars) as Pitcher_std
        from fantasy_sports_DEADLYACCURATE d
        group by year, sport, league_name
    ) a on (d.year = a.year and d.sport = a.sport and d.league_name = a.league_name)
) u using (year, sport, league_name, owner)
set d.draft_z = u.draft_z
, d.AE_z = u.AE_z
, d.Hitter_z = u.Hitter_z
, d.Pitcher_z = u.Pitcher_z
;


update fantasy_sports_ballnightlong_helper d
join(
    select d.year, d.team_name
    , (100*Approx_NORMSDIST( (d.R - a.avg_R)/(a.std_R) )
        + 100*Approx_NORMSDIST( (d.HR - a.avg_HR)/(a.std_HR) )
        + 100*Approx_NORMSDIST( (d.RBI - a.avg_RBI)/(a.std_RBI) )
        + 100*Approx_NORMSDIST( (d.SB - a.avg_SB)/(a.std_SB) )
        + 100*Approx_NORMSDIST( (d.OPS - a.avg_OPS)/(a.std_OPS) )
        + 100*Approx_NORMSDIST( (d.K - a.avg_K)/(a.std_K) )
        + 100*Approx_NORMSDIST( (d.QS - a.avg_QS)/(a.std_QS) )
        + 100*Approx_NORMSDIST( -1*(d.ERA - a.avg_ERA)/(a.std_ERA) )
        + 100*Approx_NORMSDIST( -1*(d.WHIP - a.avg_WHIP)/(a.std_WHIP) )
        + 100*Approx_NORMSDIST( (d.SVHD - a.avg_SVHD)/(a.std_SVHD) )
    ) as est_PF
    , (d.R - a.avg_R)/(a.std_R) as z_R
    , (d.HR - a.avg_HR)/(a.std_HR) as z_HR
    , (d.RBI - a.avg_RBI)/(a.std_RBI) as z_RBI
    , (d.SB - a.avg_SB)/(a.std_SB) as z_SB
    , (d.OPS - a.avg_OPS)/(a.std_OPS) as z_OPS
    , (d.K - a.avg_K)/(a.std_K) as z_K
    , (d.QS - a.avg_QS)/(a.std_QS) as z_QS
    , -1*(d.ERA - a.avg_ERA)/(a.std_ERA) as z_ERA
    , -1*(d.WHIP - a.avg_WHIP)/(a.std_WHIP) as z_WHIP
    , (d.SVHD - a.avg_SVHD)/(a.std_SVHD) as z_SVHD
    from fantasy_sports_ballnightlong_helper d
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
        , avg(ops) as avg_ops
        , std(ops) as std_ops
        , avg(k) as avg_k
        , std(k) as std_k
        , avg(qs) as avg_qs
        , std(qs) as std_qs
        , avg(era) as avg_era
        , std(era) as std_era
        , avg(whip) as avg_whip
        , std(whip) as std_whip
        , avg(svhd) as avg_svhd
        , std(svhd) as std_svhd
        from fantasy_sports_ballnightlong_helper h
        group by year
    ) a using (year)
) u using (year, team_name)
set d.est_PF = u.est_PF
, d.z_R = u.z_R
, d.z_HR = u.z_HR
, d.z_RBI = u.z_RBI
, d.z_SB = u.z_SB
, d.z_OPS = u.z_OPS
, d.z_K = u.z_K
, d.z_QS = u.z_QS
, d.z_ERA = u.z_ERA
, d.z_WHIP = u.z_WHIP
, d.z_SVHD = u.z_SVHD
;


update fantasy_sports_chili_helper d
join(
    select d.year, d.team_name
    , (100*Approx_NORMSDIST( (d.R - a.avg_R)/(a.std_R) )
        + 100*Approx_NORMSDIST( (d.HR - a.avg_HR)/(a.std_HR) )
        + 100*Approx_NORMSDIST( (d.RBI - a.avg_RBI)/(a.std_RBI) )
        + 100*Approx_NORMSDIST( (d.SB - a.avg_SB)/(a.std_SB) )
        + 100*Approx_NORMSDIST( (d.OBP - a.avg_OBP)/(a.std_OBP) )
        + 100*Approx_NORMSDIST( (d.SLG - a.avg_SLG)/(a.std_SLG) )
        + 100*Approx_NORMSDIST( (d.IP - a.avg_IP)/(a.std_IP) )
        + 100*Approx_NORMSDIST( (d.QS - a.avg_QS)/(a.std_QS) )
        + 100*Approx_NORMSDIST( (d.SV - a.avg_SV)/(a.std_SV) )
        + 100*Approx_NORMSDIST( -1*(d.ERA - a.avg_ERA)/(a.std_ERA) )
        + 100*Approx_NORMSDIST( -1*(d.WHIP - a.avg_WHIP)/(a.std_WHIP) )
        + 100*Approx_NORMSDIST( (d.K9 - a.avg_K9)/(a.std_K9) )
    ) as est_PF
    , (d.R - a.avg_R)/(a.std_R) as z_R
    , (d.HR - a.avg_HR)/(a.std_HR) as z_HR
    , (d.RBI - a.avg_RBI)/(a.std_RBI) as z_RBI
    , (d.SB - a.avg_SB)/(a.std_SB) as z_SB
    , (d.OBP - a.avg_OBP)/(a.std_OBP) as z_OBP
    , (d.SLG - a.avg_SLG)/(a.std_SLG) as z_SLG
    , (d.IP - a.avg_IP)/(a.std_IP) as z_IP
    , (d.QS - a.avg_QS)/(a.std_QS) as z_QS
    , (d.SV - a.avg_SV)/(a.std_SV) as z_SV
    , -1*(d.ERA - a.avg_ERA)/(a.std_ERA) as z_ERA
    , -1*(d.WHIP - a.avg_WHIP)/(a.std_WHIP) as z_WHIP
    , (d.K9 - a.avg_K9)/(a.std_K9) as z_K9
    from fantasy_sports_chili_helper d
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
    ) a using (year)
) u using (year, team_name)
set d.est_PF = u.est_PF
, d.z_R = u.z_R
, d.z_HR = u.z_HR
, d.z_RBI = u.z_RBI
, d.z_SB = u.z_SB
, d.z_OBP = u.z_OBP
, d.z_SLG = u.z_SLG
, d.z_IP = u.z_IP
, d.z_QS = u.z_QS
, d.z_SV = u.z_SV
, d.z_ERA = u.z_ERA
, d.z_WHIP = u.z_WHIP
, d.z_K9 = u.z_K9
;






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
        when f.Sport in ('mlb', 'nba', 'nhl')
            then 0.1207*( (f.pf-y.pf_avg)/(y.pf_std) ) + 0.5
    end as xPtsPct # regression based on PF_z vs PtsPct
    , case
        when f.Sport = 'nfl'
            then (0.1337*( (f.pf-y.pf_avg)/(y.pf_std) ) + 0.5) - (2*f.W+1*f.T)/(2*(f.W+f.T+f.L))
        when f.Sport in ('mlb', 'nba', 'nhl')
            then (0.1207*( (f.pf-y.pf_avg)/(y.pf_std) ) + 0.5) - (2*f.W+1*f.T)/(2*(f.W+f.T+f.L))
    end as PtsPct_Diff
    
    , Approx_NORMSDIST( (f.pf-y.pf_avg)/(y.pf_std) ) as zStrength
    , Approx_NORMSDIST( (f.pa - ((y.pft-f.pf)/(y.tms-1))) / (y.xpa_std) ) as PA_zStrength
    
    , case
        when f.Sport = 'nfl'
            then y.tms*(0.5429-((f.pf-y.pf_avg)/(y.pf_std)*0.2070))
        when f.Sport in ('mlb', 'nba', 'nhl')
            then y.tms*(0.5442-((f.pf-y.pf_avg)/(y.pf_std)*0.2289))
    end as xRank # linear regression based on PF_z vs. Rank/TotalTeams
    , case
        when f.Sport = 'nfl'
            then f.rank - ( y.tms*(0.5429-((f.pf-y.pf_avg)/(y.pf_std)*0.2070)) )
        when f.Sport in ('mlb', 'nba', 'nhl')
            then f.rank - ( y.tms*(0.5442-((f.pf-y.pf_avg)/(y.pf_std)*0.2289)) )
    end as Rank_Diff
    
    , case
        when f.Sport = 'nfl' 
            then 1/(1+POW(exp(1), -(-3.1344 + 1.5358 * ( (f.pf-y.pf_avg)/(y.pf_std) ) ) ) ) # logistic regression based on PF_z
        when f.Sport in ('mlb', 'nba', 'nhl')
            then 1/(1+POW(exp(1), -(-3.0178 + 1.5140 * ( (f.pf-y.pf_avg)/(y.pf_std) ) ) ) )
    end as xTitles
    , case
        when f.Sport = 'nfl'
            then 1/(1+POW(exp(1), -(-2.8695 - 1.1754 * ( (f.pf-y.pf_avg)/(y.pf_std) ) ) ) ) # logistic regression based on PF_z
        when f.Sport in ('mlb', 'nba', 'nhl')
            then 1/(1+POW(exp(1), -(-4.7637 - 2.7238 * ( (f.pf-y.pf_avg)/(y.pf_std) ) ) ) )
    end as xSackos
    
    from fantasy_sports f
    join(
        select a.*
        , std(f.PA - (a.pft-f.pf)/(a.tms-1)) as xpa_std
        from fantasy_sports f
        join(
            select f.year
            , f.sport
            , f.league_name
            , sum(pf) pft
            , count(*) as tms
            , avg(pf) as pf_avg
            , std(pf) as pf_std
            from fantasy_sports f
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
join fantasy_sports_ballnightlong_helper h on (f.year = h.year and f.Team_Name = h.Team_Name and f.League_Name = 'BallNightLong')
set f.PF = h.est_PF
;

update fantasy_sports f
join fantasy_sports_chili_helper h on (f.year = h.year and f.Team_Name = h.Team_Name and f.League_Name = 'ChiliStew')
set f.PF = h.est_PF
;

update fantasy_sports f
join fantasy_sports_DEADLYACCURATE d on (f.year = d.year and f.owner = d.owner and f.League_Name = d.League_Name and f.sport = d.sport)
set f.draft_z = d.draft_z
, f.draft_zStrength = Approx_NORMSDIST(d.draft_z)
;




drop table if exists fantasy_sports_summary;
create table fantasy_sports_summary as
select 'Total' AS year
, ff.owner
, concat(ff.league_name,'-',ff.sport) as league_name
, concat(ff.owner , ' - ', ff.league_name, ' (', ff.sport, ')', "\n\n", group_concat(concat('#'
    , if(ff.Rank is not null, if(ff.Rank % 1 = 0, round(ff.rank,0), ff.rank), '??')
    , " (", ff.Year
    , if(ff.PICK is not null, concat(", pick #", ff.PICK), '')
    , if(ff.draft_zStrength is not null, concat(", ", round(100*ff.draft_zStrength,0), ' draft_zStrength'), '')
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
, round(avg(ff.Moves),2) as Moves
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

, round(avg(ff.draft_z),2) as draft_z
, round(avg(100*ff.draft_zStrength),0) as draft_zStrength

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
, f.Moves
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

, round(f.draft_z,2) as draft_z
, round(100*f.draft_zStrength,0) as draft_zStrength

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
;