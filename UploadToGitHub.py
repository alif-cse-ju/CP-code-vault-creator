import logging
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
        level2 = "Contest-Name/ID"
        if "contest_name" in solution.keys():
            level2 = solution["contest_name"]
        else:
            level2 = solution["contest_id"]

        level3 = "Problem-Name/ID"
        if "contest_name" in solution.keys():
            level3 = solution["name"]
        else:
            level3 = solution["problem_id"]

        
        path = f'{website}/{level2}/{level3}/{solution["solution_id"]}.{solution["file_extension"]}'
        upload_to_github(repo, path, solution['solution'])

    except Exception as e:
        logging.error(f'{e} for {solution}')