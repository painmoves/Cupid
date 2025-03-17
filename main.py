import os
import re
import colorama
from colorama import Fore
colorama.init(autoreset=True)

font = f"""{Fore.CYAN}

                                                                  __           __    
                                       _________ ___  ____ ______/ /_   __  __/ /___ 
                                      / ___/ __ `__ \/ __ `/ ___/ __/  / / / / / __ \ 
                                     (__  ) / / / / / /_/ / /  / /_   / /_/ / / /_/ /
                                    /____/_/ /_/ /_/\__,_/_/   \__/   \__,_/_/ .___/ 
                                                                            /_/      

                                   {Fore.GREEN}[{Fore.CYAN}Make sure all of your ULP are in the files folder{Fore.GREEN}]{Fore.CYAN}                         
                                        """


BASE_PATH = "files"
RESULTS_PATH = "results"
print(font)
KEYWORD = input(f"                                   {Fore.GREEN}[{Fore.CYAN}KEYWORD{Fore.GREEN}] ")
KEYWORDS = [f"{KEYWORD}"]

def sanitize_filename(filename):
    return ''.join(c for c in filename if c.isascii()) if filename else "unknown.txt"

def create_keyword_folder(keyword):
    keyword_clean = keyword.replace(".", "_")
    keyword_folder = os.path.join(RESULTS_PATH, f"ulp-{keyword_clean}")
    if not os.path.exists(keyword_folder):
        os.makedirs(keyword_folder)
    return keyword_folder

async def process_file(file_path):
    files_to_send = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:

            # Lis le contenu du fichier une seule fois
            file_content = f.readlines()

            for keyword in KEYWORDS:
                keyword_folder = create_keyword_folder(keyword)
                keyword_clean = keyword.replace('.', '_')
                file_to_send_path = f"results/ulp-{keyword_clean}/filtered_results_{keyword_clean}.txt"
                
                results_found = False
                pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)

                for line in file_content:
                    if pattern.search(line):
                        print(f"                                   {Fore.GREEN}[{Fore.CYAN}+{Fore.GREEN}] Found '{keyword}': {line.strip()}")
                        with open(file_to_send_path, "a", encoding="utf-8") as rf:
                            rf.write(line)
                        results_found = True

                if results_found and os.path.getsize(file_to_send_path) > 0:
                    files_to_send.append(file_to_send_path)


    except Exception as e:
        pass

async def check_new_files():
    files_processed = 0
    total_files = len([filename for filename in os.listdir(BASE_PATH) if filename.endswith(".txt")])

    for filename in os.listdir(BASE_PATH):
        if filename.endswith(".txt"):
            file_path = os.path.join(BASE_PATH, filename)
            if os.path.exists(file_path):
                await process_file(file_path)
                files_processed += 1
                print(f"                                   {Fore.GREEN}[{Fore.CYAN}+{Fore.GREEN}] Files processed: {files_processed}/{total_files}")
    
    return files_processed == total_files

async def main():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    
    if not os.path.exists(RESULTS_PATH):
        os.makedirs(RESULTS_PATH)
    
    while True:
        try:
            all_files_processed = await check_new_files()
            if all_files_processed:
                print(f"                                   {Fore.GREEN}[{Fore.CYAN}+{Fore.GREEN}] Finished!")
                break
        except Exception as e:
            print(f"                                   {Fore.GREEN}[{Fore.CYAN}+{Fore.GREEN}] Error: {e}")
        await asyncio.sleep(2)

asyncio.run(main())
