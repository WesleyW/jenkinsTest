# gh = login("WesleyW", pw)
# issue = gh.issue(user, repo, num)
# if issue.is_closed():
#     issue.reopen()

# issue.edit('New issue title', issue.body + '\n------\n**Update:** Text to append')

help('modules')
import os.environ['testPassword']

import os
import json
import requests

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'CHANGEME'
PASSWORD = 'CHANGEME'

# The repository to add this issue to
REPO_OWNER = 'CHANGEME'
REPO_NAME = 'CHANGEME'

def make_github_issue(title, body=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print ('Successfully created Issue {0:s}'.format(title))
    else:
        print ('Could not create Issue {0:s}'.format(title))
        print ('Response:', r.content)
        
make_github_issue("TITLE")
