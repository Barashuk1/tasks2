import os
import shutil
import zipfile
import sys
from concurrent.futures import ThreadPoolExecutor

def normalize(text):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia'
    }

    last_dot_index = text.rfind('.')
    normalized_text = ''

    for i, char in enumerate(text):
        if i < last_dot_index:
            if char.lower() in translit_dict:
                if char.isupper():
                    normalized_text += translit_dict[char.lower()].capitalize()
                else:
                    normalized_text += translit_dict[char.lower()]
            elif char.isalnum():
                normalized_text += char
            else:
                normalized_text += '_'
        else:
            normalized_text += char

    return normalized_text

def move_file(file_path, destination_folder):
    shutil.move(file_path, destination_folder)

def process_files(folder_path, files):
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        normalized_file_name = normalize(file_name)
        extension = file_name.split('.')[-1].upper()
        destination_folder = None

        if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
            destination_folder = 'images'
        elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
            destination_folder = 'video'
        elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
            destination_folder = 'documents'
        elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
            destination_folder = 'audio'
        elif extension in ('ZIP', 'GZ', 'TAR'):
            destination_folder = 'archives'
            archive_folder_name = normalized_file_name.rsplit('.', 1)[0]
            archive_folder_path = os.path.join(folder_path, destination_folder, archive_folder_name)
            os.makedirs(archive_folder_path, exist_ok=True)

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(archive_folder_path)

            continue
        else:
            destination_folder = 'unknown'

        if destination_folder:
            destination_folder_path = os.path.join(folder_path, destination_folder)
            os.makedirs(destination_folder_path, exist_ok=True)

            destination_path = os.path.join(destination_folder_path, normalized_file_name)

            move_file(file_path, destination_path)
            print(f"{file_name} moved to {destination_folder}")
        else:
            print(f"{file_name} has an unknown extension")

def sort(folder_path):
    with ThreadPoolExecutor(max_workers=5) as executor:
        for root, dirs, files in os.walk(folder_path):
            executor.submit(process_files, root, files)

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path)
            except OSError:
                pass

def main():
    if len(sys.argv) == 2:
        folder_path = sys.argv[1]
        if os.path.isdir(folder_path):
            sort(folder_path)
        else:
            print("Enter folder")
    else:
        print("Enter folder")

if __name__ == "__main__":
    main()
