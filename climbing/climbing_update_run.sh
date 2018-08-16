SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

python 8a_scraper.py

wait

python completed_to_tried.py

wait

python update_climbing_csvs.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_completed.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_completed.html -c "Connor Reed - Completed Boulder Problems" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_completed.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_triedLog.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_triedLog.html -c "Connor Reed - Attempted Boulder Problems" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_triedLog.html"

cd /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/boulders_completed.html
git add Tables/boulders_triedLog.html
git add csvs/boulders_completed.csv
git add csvs/boulders_triedLog.csv
git add csvs/boulders_returnInterest.csv
git commit -m "update climbing dataset"
git push