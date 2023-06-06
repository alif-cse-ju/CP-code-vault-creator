from github import Github
from github.GithubException import UnknownObjectException
from Scrapers import (AtCoder, Codeforces)


def main():
    atcoder_username = input('AtCoder Username: ')         # alif_cse_ju
    codeforces_username = input('Codeforces Username: ')   # alif_cse_ju


    # Accessing github repository
    access_token = input('GitHub access token: ')
    git = Github(access_token)
    repo_name = 'CP-code-vault'
    try:
        repo = git.get_user().get_repo(repo_name)
    except UnknownObjectException:
        repo = git.get_user().create_repo(repo_name)

    

    # Executing scrapers
    if(atcoder_username):
        AtCoder.atcoder_uploader(atcoder_username, repo)

    if(codeforces_username):
        Codeforces.codeforces_uploader(codeforces_username, repo)
 


if __name__ == '__main__':
    main()
