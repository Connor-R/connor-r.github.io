SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

python tv_show_counter.py

wait

python tv_show_processing.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/tvShows.csv -o -c "Connor Reed - TV Show Rankings" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/tvShows.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/tvShows.html"


cd ~/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/tvShows.html
git add csvs/tvShows.csv
git commit -m "update tv Shows"
git push
