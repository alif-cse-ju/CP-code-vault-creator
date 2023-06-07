import os
import sys
import json
import requests
from time import sleep
from bs4 import BeautifulSoup

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from extensions import EXTENSIONS
from UploadToGitHub import upload_solution_type1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}

def get_submission_info(username):
    cur = 0

    while True:
        submissions = json.loads(requests.get(f'https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={username}&from_second={cur}').text)
        if not submissions:
            break

        for submission in submissions:
            if submission['result'] == 'AC':
                try:
                    yield {
                        'language': submission['language'],
                        'contest_id': submission['contest_id'],
                        'problem_id': submission['problem_id'],
                        'solution_id': submission['id'],
                        'link': f'https://atcoder.jp/contests/{submission["contest_id"]}/submissions/{submission["id"]}',
                    }

                except KeyError:
                    pass

            cur = submission['epoch_second'] + 1

        sleep(1)

def get_code(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.select_one('#submission-code').text

def get_solutions(username):
    all_info = list(get_submission_info(username))[::-1]
    responses = map(lambda info: requests.get(info['link'], headers=headers), all_info)
    for response, info in zip(responses, all_info):
        code = get_code(response.text)
        yield {
            'file_extension': EXTENSIONS[info['language']],
            'contest_id': info['contest_id'],
            'problem_id': info['problem_id'],
            'solution_id': info['solution_id'],
            'link': info['link'],
            'solution': code,
        }

def atcoder_uploader(atcoder_username, repo):
    ac_submission_cnt = 0
    for solution in get_solutions(atcoder_username):
        ac_submission_cnt += 1
        upload_solution_type1('AtCoder', solution, repo)

    return ac_submission_cnt