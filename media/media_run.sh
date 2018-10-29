SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

updateDate=$( date +"%b %d, %Y" )

python bookmark_parser.py

wait 

# python tv_show_counter.py

wait

python tv_show_processing.py

wait

python export_media.py

wait

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/relevant_bookmarks.csv -o -c "Connor Reed - Bookmarks (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/cr_bookmarks.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/cr_bookmarks.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/books.csv -o -c "Connor Reed - Books (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/books.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/books.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/movies.csv -o -c "Connor Reed - Movies (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/movies.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/movies.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/podcasts.csv -o -c "Connor Reed - Podcasts (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/podcasts.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/podcasts.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/tvShows.csv -o -c "Connor Reed - TV Shows (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/tvShows.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/tvShows.html"

cd ~/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/cr_bookmarks.html
git add csvs/relevant_bookmarks.csv
git add Tables/books.html
git add csvs/books.csv
git add Tables/movies.html
git add csvs/movies.csv
git add Tables/podcasts.html
git add csvs/podcasts.csv
git add Tables/tvShows.html
git add csvs/tvShows.csv
git commit -m "update media ($updateDate)"
git push
