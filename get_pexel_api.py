from pathlib import Path
import json
import os
import requests
import tqdm
from pexels_api import API
import sys

m = 0
def download_pexels(query, image_path, name, PEXELS_API_KEY):
    global m
    api = API(PEXELS_API_KEY)
    image_path = image_path
    try:
        # Step 1: Getting the first image URL and meta information
        api.search(query, page=1, results_per_page=1)
        photos = api.get_entries()

        if not photos:
            print("No photos found for the given query.")
            m += 1
            print(query[(m % len(query))] + query[(m + 1) % len(query)])
            if m > 10:
                m = 0
                return download_pexels("whatever", image_path, name, PEXELS_API_KEY)
            return download_pexels(query[(m % len(query))] + query[(m +1) % len(query)],
                                         image_path, name, PEXELS_API_KEY)

        photo = photos[0]
        photo_info = vars(photo)['_Photo__photo']
        url = photo_info['src']['original']

        file_path = os.path.join(image_path, f"{name}.png")

        if not os.path.isfile(file_path):
            response = requests.get(url, stream=True)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded: {file_path}")
            return file_path
        else:
            print(f"File {file_path} already exists")
            return file_path

    except Exception as e:
        print(f"Error: {e}")
        return None
n = 0
def download_video_pexels(query, fname, api_key, root_dir="./"):
    global n
    # Define Pexels API URL for videos
    api_url = "https://api.pexels.com/videos/search"
    #fname = "./ScriptFilm/thrash/"+fname
    index = 0
    headers = {"Authorization": api_key}

    # Define parameters for the API request
    params = {"query": query, "per_page": 1}  # Set to 1 to download only one video

    try:
        # Make the API request
        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Extract the download URL of the first video (if available)
            if data.get("videos"):
                download_url = data["videos"][0].get("video_files", [])[0].get("link")
                if download_url:
                    fpath = Path(root_dir, fname)

                    # Check if the file already exists
                    if fpath.exists():
                        print("Exists:", fpath)
                        return "exists"
                    else:
                        # Download the video
                        response = requests.get(download_url)
                        with open(str(fpath), "wb") as file:
                            file.write(response.content)
                        print("Downloaded:", fpath)
                        return os.path.join(fpath)
                else:
                    print("No download URL found for the video.")
            else:
                print("No videos found for the query.")
                n += 1
                print(query[(n % len(query))] + query[(n + 1) % len(query)])
                if n > 10:
                    n = 0
                    return download_video_pexels("whatever", fname, api_key, root_dir)
                return download_video_pexels(query[(n % len(query))] + query[(n + 1) % len(query)],
                                             fname, api_key, root_dir)


        else:
            print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"Error: {e}")
        index += 1  # Increment index on error

    return ""
