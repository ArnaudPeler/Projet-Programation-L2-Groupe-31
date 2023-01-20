from markdown import *
import os
def get_user_tags(user_folder: str) -> list[str]:
    tags = []
    for each in os.listdir(user_folder):
        with open(os.path.join(user_folder,each), 'r') as file:
            file_tags = detect_tag(file.read())
        if file_tags:
            for tag in file_tags:
                if not tags in tags:
                    tags.append(tag)
    return tags