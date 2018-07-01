SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

python bookmark_parser.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/relevant_bookmarks.csv -o -c "Connor Reed - Bookmarks" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/cr_bookmarks.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/cr_bookmarks.html"


cd ~/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/cr_bookmarks.html
git add csvs/relevant_bookmarks.csv
git commit -m "update bookmarks"
git push
