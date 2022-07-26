import threading
import time

from pydub import AudioSegment
from pydub.utils import mediainfo
import os

import misc

root_path = r"C:\Users\mahas\Music\Plex Music"
dest_path = r"C:\Users\mahas\Music\Normalized"
max_db = -12

semaphore = threading.BoundedSemaphore(os.cpu_count())
lock = threading.Lock()
completed = 0


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def normalize_audio(file_path, dest_folder, target_dBFS=0):
    semaphore.acquire()
    global completed
    try:
        file_dest = os.path.join(dest_folder, os.path.basename(file_path))
        if os.path.exists(file_dest):
            lock.acquire()
            completed += 1
            lock.release()
            print(f"File exists: {os.path.split(file_path)[-1]}\n"
                  f"Skipping...\n"
                  f"Completed: {completed}/{len(files)}\n")
        else:
            start_time = time.time()
            sound = AudioSegment.from_file(file_path)
            normalized_sound = match_target_amplitude(sound, target_dBFS)
            tags = mediainfo(file_path)["TAG"]
            try:
                os.makedirs(dest_folder)
            except:
                pass

            normalized_sound.export(os.path.join(dest_folder, os.path.basename(file_path)), format="mp3", tags=tags)
            end_time = time.time()
            lock.acquire()
            completed += 1
            lock.release()
            print(f"Normalized: {os.path.split(file_path)[-1]}\nTime Taken: {round(end_time - start_time, 2)} seconds\n"
                  f"Completed: {completed}/{len(files)}\n")
    except:
        print(f"Error: {os.path.split(file_path)[-1]}")
    semaphore.release()


files = misc.list_files(root_path)
relative_files = misc.list_files_relative(root_path, "")

threads_list = []

for i in range(len(files)):
    file_path = files[i]
    dest_folder = os.path.join(dest_path, *os.path.split(relative_files[i])[:-1])
    thread = threading.Thread(target=normalize_audio, args=(file_path, dest_folder, max_db))
    threads_list.append(thread)

time_start = time.time()
for thread in threads_list:
    thread.start()

for thread in threads_list:
    thread.join()
time_end = time.time()
print("=" * 20)
print(f"Total time taken: {misc.pretty_time(int(time_end - time_start))}")
