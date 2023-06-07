import os
import sys
import json
import requests
from bs4 import BeautifulSoup

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from UploadToGitHub import upload_solution_type1

async def scrape_codechef(problem):
    try:
        solutionPage = await requests.get(problem.url)
        searchString = "var meta_info = "
        soup = BeautifulSoup(solutionPage.text, 'html.parser')

        html = solutionPage.text.split("\n")

        for line in html:
            for j in range(min(len(line), 5)):
                if line[j:j + len(searchString)] == searchString:
                    metaDataText = line[j + len(searchString):-1]
                    obj = json.loads(metaDataText)
                    problem['solution'] = obj['data']['plaintext']
                    problem['file_extension'] = 'txt'
                    problem['is_ac'] = False
                    if 'languageExtension' in obj['data'] and len(obj['data']['languageExtension']) > 0:
                        problem['file_extension'] = obj['data']['languageExtension']
                    if 'solutionResult' in obj['data'] and obj['data']['solutionResult'] == 'AC':
                        problem['is_ac'] = True
                    return

    except Exception as error:
        print(f"[error in scraping {problem.url} from codechef]\t{error}")


def codechef_uploader(codechef_username, repo):
    try:
        solutionPage = requests.get(f"https://www.codechef.com/users/{codechef_username}")
        soup = BeautifulSoup(solutionPage.text, 'html.parser')

        submissions = []

        for h5 in soup.find_all('h5'):
            if h5.text.startswith('Fully Solved'):
                for link in h5.find_next('article').find_all('a'):
                    submissions.append("https://www.codechef.com" + link['href'])
                break

        for url in submissions:
            statusPage = requests.get(url)
            soup = BeautifulSoup(statusPage.text, 'html.parser')

            arr = url.split('/')
            isPractice = False
            for i in range(1, len(arr)):
                if arr[i] == 'status' and arr[i - 1].endswith('codechef.com'):
                    isPractice = True
                    break

            contestName = "Practice" if isPractice else soup.select("#breadcrumb > div:nth-child(3)")[0].text
            
            ### here comes the error

            problemName = soup.select("#breadcrumb > div:nth-child(3)")[0].text if isPractice else soup.select("#breadcrumb > div:nth-child(4)")[0].text


            for a in soup.select("div.tablebox-section.l-float a"):
                link = a['href']
                if link.startswith("/viewsolution/"):
                    problem = {}
                    problem['url'] = "https://www.codechef.com" + link
                    problem['name'] = problemName
                    problem['contest_name'] = 'Codechef - ' + contestName
                    scrape_codechef(problem)
                    if problem['is_ac'] == True:
                        upload_solution_type1('CodeChef', problem, repo)

    except Exception as error:
        print(error)