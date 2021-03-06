import time
from datetime import datetime
import csv
import os
from py_db import db
import argparse
import ast

db = db('personal')


base_path = os.getcwd()


def initiate():
    print "\n\n\tupdating csvs\n\n"
    process_completed()
    process_tried()
    process_returnInterest()
    process_breakdown()

def process_completed():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_completed.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Days Since"
        , "Date"
        , "Boulder Name"
        , "Area"
        , "Sub Area"
        , "V Grade"
        , "Euro Grade"
        , "Stars"
        , "Soft/Hard"
        , "Flash"
        , "Attempts"
        , "Minutes"
        , "Sessions"
        , "8a.nu Points"
        , "Final Time"
        , "Comment"
        , "FA"
        , "Athletic"
        , "Cruxy"
        , "Slopey"
        , "Crimpy"
        , "Sharp"
        , "Technical"
        , "Power"
        , "Endurance"
        , "Overhang"
        , "Vertical"
        , "Slab"
        , "Roof"
        , "Scary"
    ]
    append_csv.writerow(csv_header)

    qry = """SELECT DATEDIFF(NOW(), bp.session_date) AS days_since
    , bp.session_date
    , bp.boulder_name
    , bp.area
    , bp.sub_area
    , bp.v_grade
    , bg.font
    , bp.stars
    , bp.soft_hard
    , bp.flash
    , bp.total_attempts
    , bp.total_minutes
    , bp.total_sessions
    , bg.8a_points
        + IF(bp.flash = 'FLASH', 50, 0)
        + IF(bp.total_attempts = 2, 2, 0)
        + IF(bp.fa = 'FA', 20, 0)
    AS 8a_points
    , bp.final_time
    , bp.details
    , bp.fa
    , bp.athletic
    , bp.cruxy
    , bp.slopey
    , bp.crimpy
    , bp.sharp
    , bp.technical
    , bp.power
    , bp.endurance
    , bp.overhang
    , bp.vertical
    , bp.slab
    , bp.roof
    , bp.scary
    FROM boulder_problems bp
    JOIN boulder_grades bg ON (bp.v_grade = bg.hueco AND bg.8a_points>=250)
    WHERE 1
        AND completed = 'COMPLETED'
    ORDER BY days_since, session_start
    ;"""

    res = db.query(qry)

    for row in res:
        row = row
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val])+'"'
                # if i == 16:
                    # print row[i]
                    # print 

        append_csv.writerow(row)
        

def process_tried():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_triedLog.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Days Since"
        , "Date"
        , "Start Time"
        , "End Time"
        , "Boulder Name"
        , "Area"
        , "Sub Area"
        , "V Grade"
        , "Return Interest"
        , "Session #"
        , "Attempts"
        , "Minutes"
        , "Comment"
    ]
    append_csv.writerow(csv_header)
    
    qry = """SELECT DATEDIFF(NOW(), bp.session_date) AS days_since
    , bp.session_date
    , bp.session_start
    , bp.final_time AS session_end
    , bp.boulder_name
    , bp.area
    , bp.sub_area
    , bp.v_grade
    , bp.return_interest
    , bp.session_num
    , bp.session_attempts
    , bp.session_minutes
    , bp.comment
    FROM boulder_problems bp
    WHERE 1
        AND bp.completed IS NULL
        AND bp.session_date > '0000-00-00'
    ORDER BY days_since, session_start
    ;"""

    res = db.query(qry)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val])+'"'
        append_csv.writerow(row)


def process_returnInterest():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_returnInterest.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Area"
    , "Return Interest"
    , "Boulder Name"
    , "Sub Area"
    , "V Grade"
    , "Total Attempts"
    , "Total Minutes"
    , "Total Sessions"
    , "Details"
    ]
    append_csv.writerow(csv_header)
    
    qry = """SELECT bp.area
    , bp.return_interest
    , bp.boulder_name
    , bp.sub_area
    , bp.v_grade
    , bp.total_attempts
    , bp.total_minutes
    , bp.total_sessions
    , bp.details
    FROM boulder_problems bp
    JOIN(
        SELECT boulder_name
        , area
        , MAX(session_date) AS session_date
        FROM boulder_problems
        GROUP BY boulder_name, area
    ) md USING (boulder_name, area, session_date)
    LEFT JOIN boulder_problems bpc ON (bp.boulder_name = bpc.boulder_name
        AND bp.area = bpc.area
        AND (bp.sub_area IS NULL OR bp.sub_area = bpc.sub_area)
        AND bpc.completed = 'COMPLETED'
    )
    WHERE 1
        AND bpc.completed IS NULL
    ORDER BY bp.area, bp.return_interest DESC
    ;"""

    res = db.query(qry)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val])+'"'
        append_csv.writerow(row)


def process_breakdown():
    csv_path = "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_yearlyBreakdown.csv"
    csv_file = open(csv_path, "wb")
    append_csv = csv.writer(csv_file)
    csv_header = ["Row"
        , "Year"
        , "V Grade"
        , "Days"
        , "Sessions"
        , "Distinct Boulders"
        , "Completed"
        , "Flashed"
        , "Total Attempts"
        , "Total Minutes"
        , "Completion Rate"
        , "Success Rate"
        , "Flash Rate"
        , "Avg Attempts/Completion"
        , "Avg Minutes/Completion"
        , "Bounty Extra Soft"
        , "Soft"
        , "Hard"
        , "FA"
        , "ATHLETIC"
        , "CRUXY"
        , "SLOPEY"
        , "CRIMPY"
        , "SHARP"
        , "TECHNICAL"
        , "POWER"
        , "ENDURANCE"
        , "OVERHANG"
        , "VERTICAL"
        , "SLAB"
        , "ROOF"
        , "SCARY"
    ]
    append_csv.writerow(csv_header)
    
    qry = """SELECT CAST(IF(Year='All-Time' AND V_Grade = 'All', @row := 1, @row := @row+1) AS UNSIGNED) AS `row`
    , Year
    , IF(V_Grade='all'
        , V_Grade
        , IF(RIGHT(V_Grade,1)=0
            , CONCAT('V',ROUND(V_GRADE))
            , CONCAT('V',FLOOR(V_Grade),'/',CEILING(V_Grade)))
    ) AS v_grade
    , Days
    , Sessions
    , Distinct_Boulders
    , Completed
    , Flashed
    , Total_Attempts
    , Total_Minutes
    , ROUND(Completed/Distinct_Boulders,3) AS Completion_Rate
    , ROUND(Completed/Sessions,3) AS Success_Rate
    , ROUND(Flashed/Distinct_Boulders,3) AS Flash_Rate
    , ROUND(Completed_Attempts/Completed) AS Avg_Attempts_Per_Completion
    , ROUND(Completed_Minutes/Completed) AS Avg_Minutes_Per_Completion
    , BOUNTY AS BOUNTY_EXTRA_SOFT
    , SOFT
    , HARD
    , FA
    , ATHLETIC
    , CRUXY
    , SLOPEY
    , CRIMPY
    , SHARP
    , TECHNICAL
    , POWER
    , ENDURANCE
    , OVERHANG
    , VERTICAL
    , SLAB
    , ROOF
    , SCARY 
    FROM(    
        SELECT GROUP_CONCAT(DISTINCT YEAR(bp.session_date)) as year
        , GROUP_CONCAT(DISTINCT bp.v_grade) AS V_Grade
        , COUNT(DISTINCT bp.session_date) AS DAYS
        , COUNT(*) AS SESSIONS
        , COUNT(DISTINCT CONCAT(boulder_name, area, sub_area)) AS Distinct_Boulders
        , COUNT(DISTINCT IF(completed='COMPLETED', CONCAT(boulder_name, area, sub_area), NULL)) AS COMPLETED
        , COUNT(DISTINCT IF(flash='FLASH', CONCAT(boulder_name, area, sub_area), NULL)) AS FLASHED
        , SUM(session_attempts) AS total_attempts
        , SUM(session_minutes) AS total_minutes
        , SUM(IF(completed='COMPLETED', total_attempts, 0)) AS completed_attempts
        , SUM(IF(completed='COMPLETED', total_minutes, 0)) AS completed_minutes
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'BOUNTY EXTRA SOFT', CONCAT(boulder_name, area, sub_area), NULL)) AS BOUNTY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'SOFT', CONCAT(boulder_name, area, sub_area), NULL)) AS SOFT
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'HARD', CONCAT(boulder_name, area, sub_area), NULL)) AS HARD
        , COUNT(DISTINCT IF(completed='COMPLETED' AND fa = 'FA', CONCAT(boulder_name, area, sub_area), NULL)) AS FA
        , COUNT(DISTINCT IF(completed='COMPLETED' AND athletic = 'ATHLETIC', CONCAT(boulder_name, area, sub_area), NULL)) AS ATHLETIC
        , COUNT(DISTINCT IF(completed='COMPLETED' AND cruxy = 'CRUXY', CONCAT(boulder_name, area, sub_area), NULL)) AS CRUXY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND slopey = 'SLOPEY', CONCAT(boulder_name, area, sub_area), NULL)) AS SLOPEY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND crimpy = 'CRIMPY', CONCAT(boulder_name, area, sub_area), NULL)) AS CRIMPY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND sharp = 'SHARP', CONCAT(boulder_name, area, sub_area), NULL)) AS SHARP
        , COUNT(DISTINCT IF(completed='COMPLETED' AND technical = 'TECHNICAL', CONCAT(boulder_name, area, sub_area), NULL)) AS TECHNICAL
        , COUNT(DISTINCT IF(completed='COMPLETED' AND power = 'POWER', CONCAT(boulder_name, area, sub_area), NULL)) AS POWER
        , COUNT(DISTINCT IF(completed='COMPLETED' AND endurance = 'ENDURANCE', CONCAT(boulder_name, area, sub_area), NULL)) AS ENDURANCE
        , COUNT(DISTINCT IF(completed='COMPLETED' AND overhang = 'OVERHANG', CONCAT(boulder_name, area, sub_area), NULL)) AS OVERHANG
        , COUNT(DISTINCT IF(completed='COMPLETED' AND vertical = 'VERTICAL', CONCAT(boulder_name, area, sub_area), NULL)) AS VERTICAL
        , COUNT(DISTINCT IF(completed='COMPLETED' AND slab = 'SLAB', CONCAT(boulder_name, area, sub_area), NULL)) AS SLAB
        , COUNT(DISTINCT IF(completed='COMPLETED' AND roof = 'ROOF', CONCAT(boulder_name, area, sub_area), NULL)) AS ROOF
        , COUNT(DISTINCT IF(completed='COMPLETED' AND scary = 'SCARY', CONCAT(boulder_name, area, sub_area), NULL)) AS SCARY
        
        FROM boulder_problems bp
        WHERE 1
            AND bp.session_date > '0000-00-00'
        GROUP BY bp.v_grade, YEAR(bp.session_date)
        
        UNION ALL
        
        SELECT GROUP_CONCAT(DISTINCT YEAR(bp.session_date)) as year
        , 'All' AS V_Grade
        , COUNT(DISTINCT bp.session_date) AS DAYS
        , COUNT(*) AS SESSIONS
        , COUNT(DISTINCT CONCAT(boulder_name, area, sub_area)) AS Distinct_Boulders
        , COUNT(DISTINCT IF(completed='COMPLETED', CONCAT(boulder_name, area, sub_area), NULL)) AS COMPLETED
        , COUNT(DISTINCT IF(flash='FLASH', CONCAT(boulder_name, area, sub_area), NULL)) AS FLASHED
        , SUM(session_attempts) AS total_attempts
        , SUM(session_minutes) AS total_minutes
        , SUM(IF(completed='COMPLETED', total_attempts, 0)) AS completed_attempts
        , SUM(IF(completed='COMPLETED', total_minutes, 0)) AS completed_minutes
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'BOUNTY EXTRA SOFT', CONCAT(boulder_name, area, sub_area), NULL)) AS BOUNTY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'SOFT', CONCAT(boulder_name, area, sub_area), NULL)) AS SOFT
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'HARD', CONCAT(boulder_name, area, sub_area), NULL)) AS HARD
        , COUNT(DISTINCT IF(completed='COMPLETED' AND fa = 'FA', CONCAT(boulder_name, area, sub_area), NULL)) AS FA
        , COUNT(DISTINCT IF(completed='COMPLETED' AND athletic = 'ATHLETIC', CONCAT(boulder_name, area, sub_area), NULL)) AS ATHLETIC
        , COUNT(DISTINCT IF(completed='COMPLETED' AND cruxy = 'CRUXY', CONCAT(boulder_name, area, sub_area), NULL)) AS CRUXY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND slopey = 'SLOPEY', CONCAT(boulder_name, area, sub_area), NULL)) AS SLOPEY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND crimpy = 'CRIMPY', CONCAT(boulder_name, area, sub_area), NULL)) AS CRIMPY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND sharp = 'SHARP', CONCAT(boulder_name, area, sub_area), NULL)) AS SHARP
        , COUNT(DISTINCT IF(completed='COMPLETED' AND technical = 'TECHNICAL', CONCAT(boulder_name, area, sub_area), NULL)) AS TECHNICAL
        , COUNT(DISTINCT IF(completed='COMPLETED' AND power = 'POWER', CONCAT(boulder_name, area, sub_area), NULL)) AS POWER
        , COUNT(DISTINCT IF(completed='COMPLETED' AND endurance = 'ENDURANCE', CONCAT(boulder_name, area, sub_area), NULL)) AS ENDURANCE
        , COUNT(DISTINCT IF(completed='COMPLETED' AND overhang = 'OVERHANG', CONCAT(boulder_name, area, sub_area), NULL)) AS OVERHANG
        , COUNT(DISTINCT IF(completed='COMPLETED' AND vertical = 'VERTICAL', CONCAT(boulder_name, area, sub_area), NULL)) AS VERTICAL
        , COUNT(DISTINCT IF(completed='COMPLETED' AND slab = 'SLAB', CONCAT(boulder_name, area, sub_area), NULL)) AS SLAB
        , COUNT(DISTINCT IF(completed='COMPLETED' AND roof = 'ROOF', CONCAT(boulder_name, area, sub_area), NULL)) AS ROOF
        , COUNT(DISTINCT IF(completed='COMPLETED' AND scary = 'SCARY', CONCAT(boulder_name, area, sub_area), NULL)) AS SCARY
        FROM boulder_problems bp
        WHERE 1
            AND bp.session_date > '0000-00-00'
        GROUP BY YEAR(bp.session_date)
        
        UNION ALL
        
        SELECT 'All-Time' as year
        , COALESCE(bp.v_grade, 'All') AS V_Grade
        , COUNT(DISTINCT bp.session_date) AS DAYS
        , COUNT(*) AS SESSIONS
        , COUNT(DISTINCT CONCAT(boulder_name, area, sub_area)) AS Distinct_Boulders
        , COUNT(DISTINCT IF(completed='COMPLETED', CONCAT(boulder_name, area, sub_area), NULL)) AS COMPLETED
        , COUNT(DISTINCT IF(flash='FLASH', CONCAT(boulder_name, area, sub_area), NULL)) AS FLASHED
        , SUM(session_attempts) AS total_attempts
        , SUM(session_minutes) AS total_minutes
        , SUM(IF(completed='COMPLETED', total_attempts, 0)) AS completed_attempts
        , SUM(IF(completed='COMPLETED', total_minutes, 0)) AS completed_minutes
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'BOUNTY EXTRA SOFT', CONCAT(boulder_name, area, sub_area), NULL)) AS BOUNTY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'SOFT', CONCAT(boulder_name, area, sub_area), NULL)) AS SOFT
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'HARD', CONCAT(boulder_name, area, sub_area), NULL)) AS HARD
        , COUNT(DISTINCT IF(completed='COMPLETED' AND fa = 'FA', CONCAT(boulder_name, area, sub_area), NULL)) AS FA
        , COUNT(DISTINCT IF(completed='COMPLETED' AND athletic = 'ATHLETIC', CONCAT(boulder_name, area, sub_area), NULL)) AS ATHLETIC
        , COUNT(DISTINCT IF(completed='COMPLETED' AND cruxy = 'CRUXY', CONCAT(boulder_name, area, sub_area), NULL)) AS CRUXY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND slopey = 'SLOPEY', CONCAT(boulder_name, area, sub_area), NULL)) AS SLOPEY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND crimpy = 'CRIMPY', CONCAT(boulder_name, area, sub_area), NULL)) AS CRIMPY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND sharp = 'SHARP', CONCAT(boulder_name, area, sub_area), NULL)) AS SHARP
        , COUNT(DISTINCT IF(completed='COMPLETED' AND technical = 'TECHNICAL', CONCAT(boulder_name, area, sub_area), NULL)) AS TECHNICAL
        , COUNT(DISTINCT IF(completed='COMPLETED' AND power = 'POWER', CONCAT(boulder_name, area, sub_area), NULL)) AS POWER
        , COUNT(DISTINCT IF(completed='COMPLETED' AND endurance = 'ENDURANCE', CONCAT(boulder_name, area, sub_area), NULL)) AS ENDURANCE
        , COUNT(DISTINCT IF(completed='COMPLETED' AND overhang = 'OVERHANG', CONCAT(boulder_name, area, sub_area), NULL)) AS OVERHANG
        , COUNT(DISTINCT IF(completed='COMPLETED' AND vertical = 'VERTICAL', CONCAT(boulder_name, area, sub_area), NULL)) AS VERTICAL
        , COUNT(DISTINCT IF(completed='COMPLETED' AND slab = 'SLAB', CONCAT(boulder_name, area, sub_area), NULL)) AS SLAB
        , COUNT(DISTINCT IF(completed='COMPLETED' AND roof = 'ROOF', CONCAT(boulder_name, area, sub_area), NULL)) AS ROOF
        , COUNT(DISTINCT IF(completed='COMPLETED' AND scary = 'SCARY', CONCAT(boulder_name, area, sub_area), NULL)) AS SCARY
        FROM boulder_problems bp
        WHERE 1
            AND bp.session_date > '0000-00-00'
        GROUP BY bp.v_grade WITH ROLLUP
        
        UNION ALL

        SELECT 'Last 365' as year
        , COALESCE(bp.v_grade, 'All') AS V_Grade
        , COUNT(DISTINCT bp.session_date) AS DAYS
        , COUNT(*) AS SESSIONS
        , COUNT(DISTINCT CONCAT(boulder_name, area, sub_area)) AS Distinct_Boulders
        , COUNT(DISTINCT IF(completed='COMPLETED', CONCAT(boulder_name, area, sub_area), NULL)) AS COMPLETED
        , COUNT(DISTINCT IF(flash='FLASH', CONCAT(boulder_name, area, sub_area), NULL)) AS FLASHED
        , SUM(session_attempts) AS total_attempts
        , SUM(session_minutes) AS total_minutes
        , SUM(IF(completed='COMPLETED', total_attempts, 0)) AS completed_attempts
        , SUM(IF(completed='COMPLETED', total_minutes, 0)) AS completed_minutes
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'BOUNTY EXTRA SOFT', CONCAT(boulder_name, area, sub_area), NULL)) AS BOUNTY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'SOFT', CONCAT(boulder_name, area, sub_area), NULL)) AS SOFT
        , COUNT(DISTINCT IF(completed='COMPLETED' AND soft_hard = 'HARD', CONCAT(boulder_name, area, sub_area), NULL)) AS HARD
        , COUNT(DISTINCT IF(completed='COMPLETED' AND fa = 'FA', CONCAT(boulder_name, area, sub_area), NULL)) AS FA
        , COUNT(DISTINCT IF(completed='COMPLETED' AND athletic = 'ATHLETIC', CONCAT(boulder_name, area, sub_area), NULL)) AS ATHLETIC
        , COUNT(DISTINCT IF(completed='COMPLETED' AND cruxy = 'CRUXY', CONCAT(boulder_name, area, sub_area), NULL)) AS CRUXY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND slopey = 'SLOPEY', CONCAT(boulder_name, area, sub_area), NULL)) AS SLOPEY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND crimpy = 'CRIMPY', CONCAT(boulder_name, area, sub_area), NULL)) AS CRIMPY
        , COUNT(DISTINCT IF(completed='COMPLETED' AND sharp = 'SHARP', CONCAT(boulder_name, area, sub_area), NULL)) AS SHARP
        , COUNT(DISTINCT IF(completed='COMPLETED' AND technical = 'TECHNICAL', CONCAT(boulder_name, area, sub_area), NULL)) AS TECHNICAL
        , COUNT(DISTINCT IF(completed='COMPLETED' AND power = 'POWER', CONCAT(boulder_name, area, sub_area), NULL)) AS POWER
        , COUNT(DISTINCT IF(completed='COMPLETED' AND endurance = 'ENDURANCE', CONCAT(boulder_name, area, sub_area), NULL)) AS ENDURANCE
        , COUNT(DISTINCT IF(completed='COMPLETED' AND overhang = 'OVERHANG', CONCAT(boulder_name, area, sub_area), NULL)) AS OVERHANG
        , COUNT(DISTINCT IF(completed='COMPLETED' AND vertical = 'VERTICAL', CONCAT(boulder_name, area, sub_area), NULL)) AS VERTICAL
        , COUNT(DISTINCT IF(completed='COMPLETED' AND slab = 'SLAB', CONCAT(boulder_name, area, sub_area), NULL)) AS SLAB
        , COUNT(DISTINCT IF(completed='COMPLETED' AND roof = 'ROOF', CONCAT(boulder_name, area, sub_area), NULL)) AS ROOF
        , COUNT(DISTINCT IF(completed='COMPLETED' AND scary = 'SCARY', CONCAT(boulder_name, area, sub_area), NULL)) AS SCARY
        FROM boulder_problems bp
        WHERE 1
            AND bp.session_date > '0000-00-00'
            AND bp.session_date > DATE_ADD(NOW(), INTERVAL -365 DAY)
        GROUP BY bp.v_grade WITH ROLLUP
    ) a
    ORDER BY IF(year='all-time', 2, IF(year='Last 365', 1, 0)) DESC, CAST(year AS UNSIGNED) DESC, IF(V_Grade='all', 1, 0) DESC, CAST(a.v_grade AS DECIMAL(3,1)) DESC
    ;"""

    res = db.query(qry)

    for row in res:
        row = list(row)
        for i, val in enumerate(row):
            if type(val) in (str,unicode):
                row[i] = '"' + "".join([l if ord(l) < 128 else "" for l in val])+'"'
        append_csv.writerow(row)


if __name__ == "__main__":     
    initiate()
