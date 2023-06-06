import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from extensions import EXTENSIONS
from UploadToGitHub import upload_solution_type1

def scrape_codeforces(problem):
    try:
        # Scrape problem source code
        solution_page = requests.get(problem['url'])
        soup = BeautifulSoup(solution_page.content, 'html.parser')
        problem['solution'] = soup.select_one("#program-source-text").get_text()

        api_url = f"https://codeforces.com/api/contest.standings?contestId={problem['contestId']}&from=1&count=1"
        response = requests.get(api_url)
        data = response.json()
        contest_name = "GYM Contest"
        contest_name = data['result']['contest']['name']
        problem['contest_name'] = f"{contest_name}"
        return 1

    except Exception as error:
        # print(f"[Error in scraping {problem['url']} from Codeforces]\t{error}")
        return 0


def codeforces_uploader(codeforces_username, repo):
    failed_list = []
    try:
        submissions = requests.get(f"https://codeforces.com/api/user.status?handle={codeforces_username}").json()["result"]

        for submission in submissions:
            if submission["verdict"] != "OK":
                continue

            problem = {}
            problem['file_extension'] = "txt"
            if submission["programmingLanguage"] in EXTENSIONS:
                problem['file_extension'] = EXTENSIONS[submission["programmingLanguage"]]

            problem['name'] = f"{submission['problem']['index']} - {submission['problem']['name']}"
            problem['solution_id'] = f"{submission['id']}"
            problem['contest_id'] = f"{submission['contestId']}"
            problem['url'] = f"https://codeforces.com/contest/{submission['contestId']}/submission/{submission['id']}"

            ok = scrape_codeforces(problem)
            if ok:
                upload_solution_type1('Codeforces', problem, repo)
            else:
                failed_list.append(problem)

    except Exception as error:
        print(error)


    while len(failed_list) > 0:
        print(len(failed_list))
        new_failed_list = []
        for problem in failed_list:
            ok = scrape_codeforces(problem)
            if ok:
                upload_solution_type1('Codeforces', problem, repo)
            else:
                new_failed_list.append(problem)
        failed_list = new_failed_list
        
        