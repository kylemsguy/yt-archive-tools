# YT Archival Utilities

Currently a WIP project. Currently has the following utilities:

## get_members_urls.py
Fetches all Membership content from Holodex (requires a Holodex API key).
Outputs three files:
- Channel metadata (`{channel_en_name}-channelinfo.json`)
- Metadata for all Membership videos (`{channel_en_name}-membervideo-data.json`)
- URLs of all Membership videos (default filename is `membersurls.txt`) to be passed into `yt-dlp -a membersurls.txt`

## dl.sh
A shell script that runs yt-dlp on 3 classes of videos
- Membership videos (requires a `membersurls.txt` and cookies either from `cookies.txt` or from a browser; the script uses Firefox. It's the most reliable option.)
- Streams
- Shorts
- Videos
