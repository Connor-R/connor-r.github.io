SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

updateDate=$( date +"%b %d, %Y" )


python update_fantasy_football.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_fantasy_football.csv /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/fantasy_football.html -c "SV Ballers Fantasy Football History (Last Updated $updateDate)" -o -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/fantasy_football.html"


cd /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/fantasy_football.html
git add csvs/personal_fantasy_football.csv
git commit -m "update fantasy football"
git push