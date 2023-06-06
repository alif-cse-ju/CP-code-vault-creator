import logging
from extensions import EXTENSIONS
from github import GithubException

def upload_to_github(repo, git_path, content):
    folder_path = '/'.join(git_path.split('/')[:-1])

    try:
        all_paths = [file.path for file in repo.get_contents(folder_path)]

    except GithubException:
        all_paths = []

    if git_path not in all_paths:
        repo.create_file(git_path, 'Initial commit', content, branch="main")

def upload_solution_type1(website, solution, repo):

    try:
        lang = solution["language"].lower()

        extension = 'txt'
        for key, value in EXTENSIONS.items():
            if key in lang:
                extension = value
                break

        path = f'{website}/{solution["contest_id"]}/{solution["problem_id"]}/{solution["solution_id"]}.{extension}'

        upload_to_github(repo, path, solution['solution'])

    except Exception as e:
        logging.error(f'{e} for {solution}')