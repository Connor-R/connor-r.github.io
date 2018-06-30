SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

python processing/8a_parser.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_completed.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_completed.html -c "Connor Reed - Completed Boulder Problems" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_completed.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/boulders_undone.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_undone.html -c "Connor Reed - Desired Boulder Problems" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/boulders_undone.html"

cd /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/boulders_completed.html
git add Tables/boulders_undone.html
git add csvs/boulders_completed.csv
git add csvs/boulders_undone.csv
git commit -m "update climbing dataset"
git push