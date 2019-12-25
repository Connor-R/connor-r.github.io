# Shell script to update the connor-r git folder

SHELL=/bin/bash
source "/Users/connordog/.bash_profile"

updateDate=$( date +"%b %d, %Y" )

cd ~/Dropbox/Desktop_Files/Work_Things/connor-r.github.io
git pull
git add *
git commit -m "connor-r.github.io daily update ($updateDate)"
git push