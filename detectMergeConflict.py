import os
import json
import requests
import time

#Authentication and repository information
USERNAME = os.environ['ghUsername']
PASSWORD = os.environ['ghPassword']
REPO_OWNER = os.environ['repoOwner']
REPO_NAME = os.environ['repoName']

session = requests.Session()
session.auth = (USERNAME, PASSWORD)

#Returns whether the PR is mergeable - i.e. has no merge conflicts
def get_pr_mergeable():
    pr_url = 'https://api.github.com/repos/%s/%s/pulls/2' % (REPO_OWNER, REPO_NAME)
    response = session.get(pr_url)

    if response == None:
        raise 'No response from GitHub.'

    responseJson = json.loads(response.content)
    print responseJson
    if 'mergeable' not in responseJson.keys():
        raise ValueError('Could not check for merge conflicts in response - most likely due to bad credentials.\nResponse:\n' + response.content)
    return json.loads(response.content)['mergeable']

#Will wait 30 seconds for Github to calculate merge conflicts in this PR
wait_time = 0
mergeable = get_pr_mergeable()
while mergeable == None:
    if wait_time > 30:
        raise 'Github has not calculated PR merge conflicts within 30 seconds. Build again if you would like to check for merge conflict.'
    time.sleep(5)
    wait_time += 5
    mergeable = get_pr_mergeable()
    print '_____________________________________________\nMergeable: ' + str(mergeable) + '\n_____________________'

if not mergeable:
    comment_url = 'https://api.github.com/repos/%s/%s/issues/2/comments' % (REPO_OWNER, REPO_NAME)
    comment = {"body": "Your pull request has resulted in a merge conflict error."}
    print session.post(comment_url, json=comment).content + "\n____________________________\n"
    
    label_url = 'https://api.github.com/repos/%s/%s/issues/2/labels' % (REPO_OWNER, REPO_NAME)
    label = ["pr: don't merge - has merge conflicts"]
    print session.post(label_url, json=label).content
else:
    print "File has no merge conflicts."
