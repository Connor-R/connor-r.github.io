SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

updateDate=$( date +"%b %d, %Y" )


python boulder_cleanup.py

wait

python export_boulder_csvs.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_completed.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_completed.html -c "Connor Reed - Completed Boulder Problems (Last Updated $updateDate)" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_completed.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_triedLog.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_triedLog.html -c "Connor Reed - Attempted Boulder Problems (Last Updated $updateDate)" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_triedLog.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_yearlyBreakdown.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_yearlyBreakdown.html -c "Connor Reed - Bouldering Yearly Breakdown (Last Updated $updateDate)" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_yearlyBreakdown.html"

cd /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/*
git add csvs/*
git commit -m "update climbing dataset"
git push