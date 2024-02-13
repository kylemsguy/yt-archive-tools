import os
import sys

import json
import requests
import argparse

apikey = ""
channelid = "UC4WvIIAo89_AzGUh1AZ6Dkg"  # Rosemi Lovelock
base_url = "https://holodex.net/api/v2/"
limit = 50


def handle_http_codes(status_code):
    if status_code == 403:
        raise RuntimeError("Invalid Holodex API key")
    elif status_code != 200:
        print(f"Unexpected HTTP status code (status code: {status_code})")


def get_channel_info(apikey, channelid):
    endpoint = base_url + f"channels/{channelid}"
    r = requests.get(
        endpoint, 
        headers={"X-APIKEY": apikey},
    )

    handle_http_codes(r.status_code)

    return r.json()


def get_membersonly(apikey, channelid):
    endpoint = base_url + 'videos'
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

    handle_http_codes(r.status_code)    
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
        print(f"Mismatch in video count.", file=sys.stderr)
    print(f"DEBUG: Expected item count: {total}. Got {len(video_data)} items", file=sys.stderr)
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
    # parser.add_argument("-v", "--videometa-outfile", default="videometa.json", help="Saves a list of URLs for use with yt-dlp to the provided file.")
    parser.add_argument("-u", "--output-urls", help="The file to save the URL list to (no URLs will be saved if omitted)")
    parser.add_argument("channelid", help="The channel ID of the channel you wish to query")
    args = parser.parse_args()

    if args.apikey:
        apikey = args.apikey
    elif 'HOLODEX_API_KEY' in os.environ:
        apikey = os.environ['HOLODEX_API_KEY']
    else:
        apikey = input("Please provide your Holodex API key: ")
    
    channelid = args.channelid

    print("Getting channel info...")
    channelinfo = get_channel_info(apikey, channelid)

    channel_en_name = channelinfo['english_name'].replace(" ", "_") if 'english_name' in channelinfo else channelid
    print(f"Using {channel_en_name=}")

    channelinfo_filename = f"{channel_en_name}-channelinfo.json"
    print("Writing channel metadata to file")
    with open(channelinfo_filename, 'w') as outfile:
        json.dump(channelinfo, outfile, indent=4)

    print(f"Fetching data from holodex for channel with ID {channelid}")
    data = get_membersonly(apikey, channelid)

    videodata_filename = f"{channel_en_name}-membervideo-data.json"
    print(f"Outputting video metadata to {videodata_filename}")
    with open(videodata_filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    if args.output_urls:
        output_urls = args.output_urls
        print(f"Outputting URLs to {output_urls}")
        urls = extract_videourls(data)
        with open(output_urls, 'w') as outfile:
            for u in urls:
                print(u, file=outfile)
