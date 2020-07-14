import logging
import random
import requests
import json

## Configurations
logging.basicConfig(level=logging.WARNING, \
                    filename='GitHubBOT.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

## GLOBALS
TOKEN = "YOUR TOKEN HERE | SCOPE OF TOKEN SHOULD BE REPOS + FORK + YOUR_CHOICE"
#STARTING_USERNAME = '1UC1F3R616' # Example: torvalds


## Fetching User Followers
def all_followers(username):
    followers = requests.get('https://api.github.com/users/{}/followers'.format(username), \
                     headers={'Authorization': 'token {}'.format(TOKEN)})
    followers = followers.text
    followers = json.loads(followers)
    
    followers_list = []
    for user in followers:
        followers_list.append(user.get('login'))
    logging.debug(str(followers_list)) # DEBUG
    return followers_list

## Get all Repos
def all_repos(username):
    repos = requests.get('https://api.github.com/users/{}/repos'.format(username), \
                     headers={'Authorization': 'token {}'.format(TOKEN)})
    repos = repos.text
    repos = json.loads(repos)

    repos_list = []
    for repo in repos:
        repos_list.append(repo.get('full_name'))
    logging.debug(str(repos_list)) # DEBUG
    return repos_list
    

## Follow A User
def follow_user(username):
    try:
        # If it's self then don't go deep
        if (username == 'D-E-F-E-A-T'): # Replace with self username
            logging.info('[-] {} is Already Followed'.format(username)) # INFO
            print('[-] {} is Already Followed'.format(username))
            return 404
        
        # Check if Already Followed
        followed = requests.get('https://api.github.com/user/following/{}'.format(username), \
                         headers={'Authorization': 'token {}'.format(TOKEN)})

        if followed.status_code == 204:
            logging.info('[-] {} is Already Followed'.format(username)) # INFO
            print('[-] {} is Already Followed'.format(username))
            return 404
        
        r = requests.put('https://api.github.com/user/following/{}'.format(username), \
                         headers={'Authorization': 'token {}'.format(TOKEN)})
        if(r.status_code == 204): # 204 is OK
            print('Followed {}'.format(username))
            logging.info('Followed {}'.format(username)) # INFO
        else:
            logging.warning("! {}: Failed to Follow {}".format(str(r.status_code), username)) # WARNING
            print("! {}: Failed to Follow {}".format(str(r.status_code), username))
        return 200
    except:
        logging.error('! Error in Following {}'.format(follow_user)) #ERROR
        print('! Error in Following {}'.format(follow_user))
        return 200

## Fork a Repo
def fork_repo(repo_name):
    try:
        # No fork for self
        if (repo_name.split('/')[0] == 'D-E-F-E-A-T') # replace with self username:
            return
        
        # Check if Already Forked -- Since users are filltered so it's OK :/
        # Saving API and code because it will cost 1 request any way if we are checking using get
        
        r = requests.post('https://api.github.com/repos/{}/forks'.format(repo_name), \
                         headers={'Authorization': 'token {}'.format(TOKEN)})
        if (r.status_code == 202): # 202 is OK
            logging.info('Forked {}'.format(repo_name)) # INFO
            print('Forked {}'.format(repo_name))
        else:
            logging.warning("! {}: Fork Failed for {}".format(str(r.status_code), repo_name)) # WARNING
            print("! {}: Fork Failed for {}".format(str(r.status_code), repo_name))
    except:
        logging.error('! Error in Forking {}'.format(repo_name)) #ERROR
        print('! Error in Forking {}'.format(repo_name))
    
## Star a Repo | Getting 404, not a scope issue
def star_repo(repo_name):
    r = requests.post('https://api.github.com/user/starred/{}'.format(repo_name), \
                     headers={'Authorization': 'token {}'.format(TOKEN)})
    print(r.status_code)


def run(username):
    
    # Follow a Random Person
    followers = all_followers(username)
    followers_copy = list(followers)
    followers_len = len(followers)
    if followers_len!=0: # Let it be Wild / Follow less than Half a users
        while(followers_len > 0):
            index = (len(followers_copy)-1)%(random.choice((1, 1000))) # Random Selection of Person
            if follow_user(followers_copy.pop(index)) == 404: # Remove any person already followed
                followers.pop(index)
                followers_len -= 1
            followers_len -= random.choice((1, 10)) # Decrease this to go Wild
    del followers_copy

    repos = []
    for person in range(len(followers)%8): # Let it be full for wild | Forking repos from only 8 users
        repos += all_repos(followers[person]) # Don't use append without iteration
    repos_copy = list(repos)
    repos_length = len(repos)
    
    # Fork a random Repo
    if repos_length!=0: # Let it be Wild / Fork less than Half a repos
        while(repos_length > 0):
            fork_repo(repos_copy.pop())
            repos_length -= random.choice((1, 30)) # Increase this number to make fork lesser

    del repos
    del repos_copy

    # Depth == 10
    for x in range(10):
        try:
            run(followers.pop())
        except:
            print('No More Followers')

run('manikandanraji')
    
    
