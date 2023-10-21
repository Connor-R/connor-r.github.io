# Shell script to update the connor-r git folder


updateDate=$( date +"%b %d, %Y" )

git pull
git add *
git commit -m "connor-r.github.io daily update ($updateDate)"
git push
git repack -f -d --depth=250 --window=250