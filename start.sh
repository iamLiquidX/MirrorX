pip3 -qq install --upgrade yt-dlp
sed -n -i '/max-concurrent-downloads/q;p' /app/aria.conf
tracker_list=`curl -Ns https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt | awk '$1' | tr '\n' ',' | cat`
echo -e "\nmax-concurrent-downloads=4\nbt-tracker=$tracker_list" >> /app/aria.conf
aria2c --conf-path=/app/aria.conf
python3 -m bot