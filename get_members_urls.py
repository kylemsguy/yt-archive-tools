import os
import sys

import json
import requests
import argparse

apikey = ""
channelid = "UC4WvIIAo89_AzGUh1AZ6Dkg"  # Rosemi Lovelock
endpoint = "https://holodex.net/api/v2/videos"
limit = 50

def loadapikey():
    global apikey
    with open("apikey.txt") as infile:
        apikey = infile.read().strip()

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
    parser = argparse.ArgumentParser(
        description="Requests member stream data from Holodex",
    )
    parser.add_argument("--apikey", help="Your Holodex API key. Can also be passed in using the HOLODEX_API_KEY environment variable.")
    parser.add_argument("-v", "--videometa-outfile", default="videometa.json", help="The file to save the raw video metadata to (default: videometa.json)")
    parser.add_argument("-u", "--urls-outfile", default="urlstodownload.txt", help="The file to save the URL list to (default: urlstodownload.txt)")
    parser.add_argument("channelid", help="The channel ID of the channel you wish to query")
    args = parser.parse_args()

    if args.apikey:
        apikey = args.apikey
    elif 'HOLODEX_API_KEY' in os.environ:
        apikey = os.environ['HOLODEX_API_KEY']
    else:
        apikey = input("Please provide your Holodex API key: ")
    
    channelid = args.channelid

    data = get_membersonly(apikey, channelid)
    with open(args.videometa_outfile, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    urls = extract_videourls(data)
    with open(args.urls_outfile, 'w') as outfile:
        for u in urls:
            print(u, file=outfile)
