from Scrapers import AtCoder
from github import Github
from github.GithubException import UnknownObjectException


def main():
    atcoder_username = input('AtCoder Username: ')

    # Accessing github repository
    access_token = input('GitHub access token: ') #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
    git = Github(access_token)
    repo_name = 'CP-code-vault'
    try:
        repo = git.get_user().get_repo(repo_name)
    except UnknownObjectException:
        repo = git.get_user().create_repo(repo_name)

    
    # Executing scrapers
    if(atcoder_username):
        AtCoder.atcoder_uploader(atcoder_username, repo)
 

if __name__ == '__main__':
    main()