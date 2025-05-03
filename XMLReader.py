import xml.etree.ElementTree as ET
import videoCreator
import tags
import whisper_api
import os

def remove(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Find the index of </data>
    data_end_index = content.find('</data>')

    # Remove text after </data>
    if data_end_index != -1:
        content = content[:data_end_index + len('</data>')]

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

def create_directories():
    # Specify the directory paths
    script_film_path = "./ScriptFilm"
    thrash_image_path = "./ScriptFilm/thrash/image"
    video_path = "./ScriptFilm/videos"

    # Create directories if they don't exist
    try:
        os.makedirs(script_film_path)
        print(f"Directory '{script_film_path}' created.")
    except FileExistsError:
        print(f"Directory '{script_film_path}' already exists.")

    try:
        os.makedirs(thrash_image_path)
        print(f"Directory '{thrash_image_path}' created.")
    except FileExistsError:
        print(f"Directory '{thrash_image_path}' already exists.")

    try:
        os.makedirs(video_path)
        print(f"Directory '{video_path}' created.")
    except FileExistsError:
        print(f"Directory '{video_path}' already exists.")

def Read(xml, cap, task_complete_event):
    create_directories()
    api_key = ""
    lang = ""
    outputname = ""
    print(xml)
    root = ET.fromstring(xml)
    vertical = True
    # Extract the directory part of the file path
    for child in root:
        if(child.tag == "head"):
            api_key = child.find("pexel").get("key")
            outputname = child.find("output").get("name")
            lang = child.find("lang").get("lang")
            if child.find("vertical") is not None:
                vertical = True
            elif child.find("horizontal") is not None:
                vertical = False
        if (child.tag == "body"):
            for count, data in enumerate(child):
               if(data.tag == "pexelimg"):
                   tags.pexelimg(data, count, api_key, lang, vertical)
               if(data.tag == "pexelvideo"):
                   tags.pexelvideo(data, count, api_key, lang, vertical)
               if (data.tag == "googleimg"):
                   tags.googleimg(data, count, lang, vertical)
               if(data.tag == "image"):
                    tags.image(data,count, lang, vertical)
               if(data.tag == "video"):
                   tags.video(data, count, lang, vertical)

            outputname = outputname.replace(':', '')


            if cap:
                nam = "./ScriptFilm/thrash/poloczony.mp4"
                videoCreator.merge_videos("./ScriptFilm/videos", nam)
                whisper_api.extract_audio(nam, "a.mp3")
                c, e = whisper_api.getCaption("a.mp3")
                print(c, e)
                nam = "napisy.mp4"
                videoCreator.add_captions("./ScriptFilm/thrash/poloczony.mp4", nam, c, e)
                print(c, e)
                videoCreator.connect_video_to_audio(nam, "a.mp3", outputname+".mp4", vertical)
                print(c, e)
            else:
                videoCreator.merge_videos("./ScriptFilm/videos", outputname+".mp4")
            if (os.path.exists("a.mp3")):
                os.remove("a.mp3")
    videoCreator.remove_files_in_folder("./ScriptFilm/thrash")
    videoCreator.remove_files_in_folder("./ScriptFilm/thrash/image")
    task_complete_event.set()