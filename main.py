from github import Github
from github.GithubException import UnknownObjectException
from Scrapers import (AtCoder, Codeforces, CodeChef)


def main():
    atcoder_username = ''          # alif_cse_ju
    codeforces_username = ''       # alif_cse_ju
    codeforces_password = ''
    codechef_username = ''         # alif_cse_ju


    # Accessing github repository
    access_token = ''
    git = Github(access_token)
    repo_name = 'CP-code-vault'
    try:
        repo = git.get_user().get_repo(repo_name)
    except UnknownObjectException:
        repo = git.get_user().create_repo(repo_name)

    

    # Executing scrapers
    if(atcoder_username):
        ac_submission_cnt = AtCoder.atcoder_uploader(atcoder_username, repo)
        print('Problem uploaded from AtCoder = ') + ac_submission_cnt
 
    if(codeforces_username):
        ac_submission_cnt = Codeforces.codeforces_uploader(codeforces_username, codeforces_password, repo)
        print('Problem uploaded from Codeforces = ' + str(ac_submission_cnt))

    if(codechef_username):
        ac_submission_cnt = CodeChef.codechef_uploader(codechef_username, repo)
        print('Problem uploaded from Codechef = ' + str(ac_submission_cnt))
 


if __name__ == '__main__':
    main()