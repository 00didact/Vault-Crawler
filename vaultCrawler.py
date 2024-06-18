import requests
import re
import time
from sortROM import unpack_and_sort_files
from sortROM import remove_trailing_spaces
from urllib.parse import urlparse
from datetime import datetime
import os
import signal

current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")


def download_file(media_id):
    url = f"https://download3.vimm.net/download/?mediaId={media_id}"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Referer":"https://vimm.net/"
    }
    try:
        response = requests.get(url, stream=True, headers=headers)
        if response.status_code == 200:
            content_disposition = response.headers.get('Content-Disposition')
            content_length = int(response.headers.get('Content-Length', 0))
            if content_length > 128*1024*1024:
                logging(f"Request: {media_id} - file size exceeds 128MB. Skipping download.")
                response.close()
                return
            content = response.content
            if any(ext in content for ext in (b".gba", b".gbc", b".nes", b".gb", b".nez", b".smc", b".sfc", b".smd", b".md", b".gen", b".gg", b".n64", b".z64", b".nds", b".a26", b".a52", b".sms", b".a78", b".pce", b".32x")):
                if content_disposition:
                    parenthesis_match = re.search(r'\(.*?\)', content_disposition)
                    if parenthesis_match:
                        parenthesis_string = parenthesis_match.group()
                        country_code_match = re.search(r'(USA|Tr)', parenthesis_string)
                        if country_code_match:
                            country_code = country_code_match.group()
                            filename_match = re.search(r'filename="([^"]+?)"', content_disposition)
                            if filename_match:
                                filename = filename_match.group(1)
                                with open("/mnt/vimm_vault/" + filename, 'wb') as file:
                                    for chunk in response.iter_content(chunk_size=131072): # download in 128KB chunks
                                        file.write(chunk)
                                logging(f"Request: {media_id} - File '{filename}' downloaded successfully. Country code: {country_code}")
                            else:
                                logging(f"Request: {media_id} - No filename found in the Content-Disposition header.")
                        else:
                            country_code = parenthesis_string
                            logging(f"Request: {media_id} - Incorrect country code in the Content-Disposition header. Country code: {country_code}")
                            time.sleep(1)
                    else:
                        logging(f"Request: {media_id} - No parenthesis-enclosed string found in the Content-Disposition header.")
                else:
                    logging(f"Request: {media_id} - No Content-Disposition header found in the response.")
            else:
                if response.status_code == 200:
                    # has to rebuild filename-match because ???
                    filename_match = re.search(r'filename="([^"]+?)\(.*?USA.*?\).*?"', content_disposition)
                    filename = filename_match.group(1)
                    logging(f"Request: {media_id} - File '{filename}' is not in the allowed console list.")
                else:
                    logging(f"Request: {media_id}- Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging(f"Request: {media_id} - An error occurred while downloading the file: {str(e)}")
    except Exception as e:
        logging(f"Request: {media_id} - An unexpected error occurred: {str(e)}")
    
# def wait_for_keypress():
#     print("Waiting to exit. Press any key...")
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     try:
#         tty.setraw(fd)
#         sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
def handle_interrupt(signum, frame):
    print("Interrupt signal received. Exiting...")
    print("Done sorting at " + time.strftime("%Y-%m-%d %H:%M:%S") + "!")
    exit(0)
     
def logging(message):
    log_file = "log.txt"
    timestamp = datetime.now().strftime("[%m-%d-%y %H:%M:%S]")
    log_entry = f"{timestamp} {message}\n"
    
    print(message)
    
    if not os.path.exists(log_file):
        with open(log_file, 'w') as file:
            file.write(log_entry)
    else:
        with open(log_file, 'a') as file:
            file.write(log_entry)

if __name__ == "__main__":
    print("Starting the crawl at " + current_time + "!")
    for media_id in [str(i).zfill(5) for i in range(2765, 99999)]:
            download_file(media_id)
    print("Unpacking, sorting, and clearing files. Please wait...")
    unpack_and_sort_files()
    for files in os.listdir(CHANGE_ME):
        remove_trailing_spaces(files)
    signal.signal(signal.SIGINT, handle_interrupt)
    print("Done sorting at " + current_time + "!")
    # wait_for_keypress()
    exit()