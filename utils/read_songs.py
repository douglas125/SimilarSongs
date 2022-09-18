import os
import subprocess
import pandas as pd
from tqdm import tqdm
from pytube import YouTube


def get_song_files():
    files = os.listdir("songs")
    return [x.replace(".csv", "") for x in files]


def get_song_info(file):
    file_path = os.path.join("songs", file + ".csv")
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        return df.to_dict("records")
    else:
        return None


def download_songs(file):
    file_path = os.path.join("songs", file + ".csv")
    os.makedirs("videos", exist_ok=True)
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            try:
                target_file = os.path.join("videos", f"{row.video_id}.mp4")
                if not os.path.isfile(target_file):
                    yt = YouTube(f"http://youtube.com/watch?v={row.video_id}")
                    yt.streams.filter(progressive=True, file_extension="mp4").order_by(
                        "resolution"
                    ).desc().first().download(filename=target_file)

                # crop file with ffmpeg
                cropped_file = target_file.replace(
                    ".mp4", f"_{row.start}_{row.end}.mp4"
                )
                if not os.path.isfile(cropped_file):
                    cmd = [
                        "ffmpeg",
                        "-ss",
                        str(row.start),
                        "-to",
                        str(row.end),
                        "-i",
                        target_file,
                        "-c",
                        "copy",
                        cropped_file,
                    ]
                    subprocess.run(cmd)
            except:
                print(f"Problem with {row.video_id}")


def get_local_names(file):
    file_path = os.path.join("songs", file + ".csv")
    os.makedirs("videos", exist_ok=True)
    if os.path.isfile(file_path):
        local_names = []
        df = pd.read_csv(file_path)
        for idx, row in df.iterrows():
            target_file = f"{row.video_id}.mp4"
            cropped_file = target_file.replace(".mp4", f"_{row.start}_{row.end}.mp4")
            local_names.append(cropped_file)
        df["local_name"] = local_names
        return df.to_dict("records")
    return None
