#!/bin/sh
channelname="Rosemi_Lovelock"
outputfilename='%(upload_date)s-%(title)s-%(id)s.%(ext)s'

# To download members data, make sure you have all the member video URLs in membersurls.txt or change this filename
memberurlsfile="membersurls.txt"

yt-dlp -a "$membersurlsfile" --cookies-from-browser firefox --no-abort-on-error --sub-langs all --write-subs --embed-subs --add-metadata --write-description --write-thumbnail --embed-thumbnail --embed-metadata --embed-info-json --write-info-json --match-filter !is_live --download-archive "members.txt" "https://www.youtube.com/@${channelname}/membership" -o "members/$outputfilename"
yt-dlp --cookies-from-browser firefox --no-abort-on-error --sub-langs all --write-subs --embed-subs --add-metadata --write-description --write-thumbnail --embed-thumbnail --embed-metadata --embed-info-json --write-info-json --match-filter !is_live --download-archive "streams.txt" "https://www.youtube.com/@${channelname}/streams" -o "streams/$outputfilename"
yt-dlp --cookies-from-browser firefox --no-abort-on-error --sub-langs all --write-subs --embed-subs --add-metadata --write-description --write-thumbnail --embed-thumbnail --embed-metadata --embed-info-json --write-info-json --match-filter !is_live --download-archive "shorts.txt" "https://www.youtube.com/@${channelname}/shorts" -o "shorts/$outputfilename"
yt-dlp --cookies-from-browser firefox --no-abort-on-error --sub-langs all --write-subs --embed-subs --add-metadata --write-description --write-thumbnail --embed-thumbnail --embed-metadata --embed-info-json --write-info-json --match-filter !is_live --download-archive "videos.txt" "https://www.youtube.com/@${channelname}/videos" -o "videos/$outputfilename"

# Old command for downloading members content only (no longer works due to YT changes)
# yt-dlp --cookies-from-browser firefox --no-abort-on-error --sub-langs all --write-subs --embed-subs --add-metadata --write-description --write-thumbnail --embed-thumbnail --embed-metadata --embed-info-json --write-info-json --match-filter !is_live --download-archive "members.txt" "https://www.youtube.com/@${channelname}/membership" -o "members/$outputfilename"