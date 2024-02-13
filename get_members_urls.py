import json
import requests

apikey = ""
channelid = "UC4WvIIAo89_AzGUh1AZ6Dkg"  # Rosemi Lovelock
endpoint = "https://holodex.net/api/v2/videos"
limit = 50

def get_membersonly(apikey, channelid):
    offset = 0
    video_data = []

    r = requests.get(
        endpoint, 
        headers={"X-APIKEY": apikey},
        params={
            "paginated": "yes",
            "channel_id": channelid,
            "topic": "membersonly",
            "limit": limit,
            "offset": offset,
        }
    )

    response = r.json()

    total = response['total']
    items = response['items']

    while items:
        video_data.extend(items)
        offset += limit

        r = requests.get(
            endpoint, 
            headers={"X-APIKEY": apikey},
            params={
                # "paginated": "yes",
                "channel_id": channelid,
                "topic": "membersonly",
                "limit": limit,
                "offset": offset,
            }
        )
        items = r.json()

    # Sanity check
    if len(video_data) != total:
        print(f"Mismatch in video count.")
    print(f"Expected: {total}. Got {len(video_data)}")
    return video_data

def extract_videourls(videodata):
    urls = []
    for v in videodata:
        vid = v['id']
        urls.append(f"https://youtube.com/watch?v={vid}")
    return urls


if __name__ == "__main__":
    data = get_membersonly(apikey, channelid)
    with open("videometa.json", 'w') as outfile:
        json.dump(data, outfile, indent=4)

    urls = extract_videourls(data)
    with open("urlstodownload.txt", 'w') as outfile:
        for u in urls:
            print(u, file=outfile)
