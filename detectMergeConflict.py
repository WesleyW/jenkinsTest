import os
import json
import requests

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = os.environ['ghUsername']
PASSWORD = os.environ['ghPassword']

# The repository to add this issue to
REPO_OWNER = os.environ['repoOwner']
REPO_NAME = os.environ['repoName']

def make_github_issue(title, body=None, labels=[]):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    
    url = 'https://api.github.com/repos/%s/%s/pulls/2' % (REPO_OWNER, REPO_NAME)
    
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Create our issue
#     issue = {'title': title,
#              'body': body,
#              'labels': labels}
    # Add the issue to our repository
#     r = session.post(url, json.dumps(issue))
    r = session.get(url)
    content = json.loads(r.content)
    print content['mergeable']
#     if r.status_code == 201:
#         print ('Successfully created Issue {0:s}'.format(title))
#     else:
#         print ('Could not create Issue {0:s}'.format(title))
#         print ('Response:', r.content)
        
make_github_issue("TITLE")
