import os

def pretty_time(input_seconds: int):
    if input_seconds < 0:
        return "0 seconds"
    minutes, seconds = divmod(input_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    final_string_to_join = []
    if weeks > 0:
        final_string_to_join.append(f"{weeks} {'weeks' if weeks != 1 else 'week'}")
    if days > 0:
        final_string_to_join.append(f"{days} {'days' if days != 1 else 'day'}")
    if hours > 0:
        final_string_to_join.append(f"{hours} {'hours' if hours != 1 else 'hour'}")
    if minutes > 0:
        final_string_to_join.append(f"{minutes} {'minutes' if minutes != 1 else 'minute'}")
    if seconds > 0:
        final_string_to_join.append(f"{seconds} {'seconds' if seconds != 1 else 'second'}")

    if len(final_string_to_join) > 1:
        final_string = ", ".join(final_string_to_join[:-1]) + f", and {final_string_to_join[-1]}"
    else:
        final_string = ", ".join(final_string_to_join)
    return final_string


def list_files(root_path, files=[], endswith=".mp3"):
    list = os.listdir(root_path)
    folders = [x for x in list if os.path.isdir(os.path.join(root_path, x))]
    file_entries = [
        os.path.join(root_path, x) for x in list
        if os.path.isfile(os.path.join(root_path, x)) and x.endswith(endswith)
    ]
    files.extend(file_entries)
    for folder in folders:
        files = list_files(os.path.join(root_path, folder), files)
    return files


def list_files_relative(root_path, folder_path, files=[], endswith=".mp3"):
    list = os.listdir(os.path.join(root_path, folder_path))
    folders = [x for x in list if os.path.isdir(os.path.join(root_path, folder_path, x))]
    file_entries = [os.path.join(folder_path, x) for x in list
                    if os.path.isfile(os.path.join(root_path, folder_path, x)) and x.endswith(endswith)
                    ]
    files.extend(file_entries)
    for folder in folders:
        files = list_files_relative(root_path, os.path.join(folder_path, folder), files)
    return files
