import logging
import random
import requests
import json

"""
Deprecating forking as that causes github to allocate me new memory which I
don't want them to. So from now on Following only.
"""

## Configurations
logging.basicConfig(level=logging.WARNING, \
                    filename='GitHubBOT.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

## GLOBALS
TOKEN = "YOUR TOKEN HERE | SCOPE OF TOKEN SHOULD BE REPOS + FORK + YOUR_CHOICE"


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




def run(username):
    
    # Follow a Random Person
    followers = all_followers(username)
    followers_len = len(followers)
    if followers_len!=0: # Let it be Wild / Follow less than Half a users
        while(followers_len > 0):
            #index = (len(followers)-1)%(random.choice((1, 1000))) # Random Selection of Person
            index = followers_len - 1 # Sequential Selection of Person
            if follow_user(followers[index]) == 404: # Remove any person already followed
                followers.pop(index)
                followers_len -= 1
            followers_len -= random.choice((1, 1)) # Decrease this to go Wild

    
        try:
            run(followers.pop())
        except:
            print('No More Followers')

run('kautukkundan')

    
