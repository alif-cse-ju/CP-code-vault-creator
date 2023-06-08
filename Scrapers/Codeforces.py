import os
import sys
import time
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from extensions import EXTENSIONS
from UploadToGitHub import upload_to_github

from selenium import webdriver
from selenium.webdriver.common.by import By

chromedriver_path = "E:\\319_Alif(27)\\CP\\CP-code-vault-creator\\chromedriver_win32"
os.environ['PATH'] += chromedriver_path



def handle_login(codeforces_username, codeforces_password):
    driver = webdriver.Chrome()
    driver.implicitly_wait(40)

    # Login Page handle
    driver.get("https://codeforces.com/enter")
    login = driver.find_element(By.ID, "handleOrEmail")
    password = driver.find_element(By.ID, "password")
    login.send_keys(codeforces_username)
    password.send_keys(codeforces_password)
    btn = driver.find_element(By.CSS_SELECTOR, ".submit")
    btn.click()
    time.sleep(3)

    return driver




def find_contest_base(contest_name):
    contest_base = contest_name.split()[0]
    if contest_base == "Codeforces":
        contest_base_2 = contest_name.split()[1]
        if contest_base_2 == "Global":
            contest_base = "Codeforces Global Round"
        else:
            contest_base = "Codeforces Round"
    elif contest_base == "Hello" or contest_base.startswith("Good"):
        contest_base = "Codeforces Round"
    elif contest_base == "Educational":
        contest_base = "Educational Round"
    elif contest_base == "Technocup":
        contest_base = "Technocup"
    else:
        contest_base = "Others"

    return contest_base




def codeforces_uploader(codeforces_username, codeforces_password, repo):
    ac_submission_cnt = 0
    first_submission_id_of_last_update = '208856669' # Update this after every time you run this program

    
    driver = handle_login(codeforces_username, codeforces_password)

    # Submission Page handle
    driver.get(f"https://codeforces.com/submissions/{codeforces_username}")
    page_numbers = driver.find_elements_by_css_selector('span.page-index')

    for i in range(8, int(page_numbers[-1].text)+1):


        print("---> " + str(i))

        driver.get(f"https://codeforces.com/submissions/{codeforces_username}/page/{i}")
        time.sleep(1)
        
        table_row = driver.find_elements(By.TAG_NAME, "tr") # every row is selected
        table_row = table_row[1:-2]
        
        ii = 0
        while ii < len(table_row):

            row = table_row[ii]
            table_col = row.find_elements(By.TAG_NAME, "td")

            verdict = table_col[5].text
            verdict = verdict.strip()

            if verdict != 'Accepted':
                ii += 1
                continue


            solution_id = table_col[0].text
            solution_id = solution_id.strip()

            if(solution_id == first_submission_id_of_last_update):
                return ac_submission_cnt
            
            name = table_col[3].text
            name = name.strip()

            language = table_col[4].text
            language = language.strip()

            
            btn = table_col[0].find_element(By.CSS_SELECTOR, ".view-source")
            btn.click()
            time.sleep(2)


            span_element = driver.find_elements(By.CSS_SELECTOR, 'span.source-popup-header')
            start_index = span_element[1].text.find("contest: ") + len("contest: ")
            end_index = span_element[1].text.find(",", start_index)
            contest_name = span_element[1].text[start_index:end_index].strip()

            solution_code = ''
            code = driver.find_elements(By.TAG_NAME, "code")  
            for line in code:
                solution_code += (line.text)
            
            
            # insurance
            if len(solution_code) == 0:
                time.sleep(3)
                print("got one")
                close = driver.find_element(By.CSS_SELECTOR, ".close")
                close.click()
                time.sleep(2)
                continue
            
                
            
            for c in "\/:*?\"<>|": # folder name can't have these character
                name = name.replace(c, '-')

            solution = {}
            solution['contest_name'] = contest_name
            solution['name'] = name
            solution['solution_id'] = solution_id
            solution['solution'] = solution_code
            solution['file_extension'] = EXTENSIONS[language]

            try:
                contest_base = find_contest_base(contest_name)
                path = f'Codeforces/{contest_base}/{solution["contest_name"]}/{solution["name"]}/{solution["solution_id"]}.{solution["file_extension"]}'
                upload_to_github(repo, path, solution['solution'])

            except Exception as e:
                logging.error(f'{e} for {solution}')
            
            close = driver.find_element(By.CSS_SELECTOR, ".close")
            close.click()
            
            
            ii += 1
            ac_submission_cnt += 1
            time.sleep(1)

    return ac_submission_cnt