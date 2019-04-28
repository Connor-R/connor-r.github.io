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

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_relevant_bookmarks.csv -o -c "Connor Reed - Bookmarks (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/cr_bookmarks.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/cr_bookmarks.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_books.csv -o -c "Connor Reed - Books (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/books.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/books.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_movies.csv -o -c "Connor Reed - Movies (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/movies.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/movies.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_podcasts.csv -o -c "Connor Reed - Podcasts (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/podcasts.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/podcasts.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_quotes.csv -o -c "Connor Reed - Quotes (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/quotes.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/quotes.html"

csvtotable /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/csvs/personal_tvShows.csv -o -c "Connor Reed - TV Shows (Last Updated $updateDate)" /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/tvShows.html -vs 15
python /Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/google_analytics_appender.py --file_path "/Users/connordog/Dropbox/Desktop_Files/Work_Things/connor-r.github.io/Tables/tvShows.html"

cd ~/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git add Tables/*
git add csvs/*
git commit -m "update media ($updateDate)"
git push
