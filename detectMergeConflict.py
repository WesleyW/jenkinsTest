import os
import json
import requests
import time

#Authentication and repository information
USERNAME = os.environ['ghUsername']
PASSWORD = os.environ['ghPassword']
REPO_OWNER = os.environ['repoOwner']
REPO_NAME = os.environ['repoName']

#Creates session to make requests to Github repo.
session = requests.Session()
session.auth = (USERNAME, PASSWORD)

MERGE_CONFLICT_MSG = 'Your pull request has resulted in a merge conflict error.'

#Returns whether the PR is mergeable - i.e. has no merge conflicts
def get_mergeable_value():
    pr_url = 'https://api.github.com/repos/%s/%s/pulls/2' % (REPO_OWNER, REPO_NAME)
    response = session.get(pr_url)

    if response == None:
        raise 'No response from GitHub.'

    responseJson = json.loads(response.content)
    if 'mergeable' not in responseJson.keys():
        raise ValueError('Could not check for merge conflicts in response - most likely due to bad credentials.\nResponse:\n' + response.content)
    return json.loads(response.content)['mergeable']

#Check if Github has finished calculating merge conflicts every 5 seconds. Raises error after more than 30 seconds.
def get_pr_mergeable():
    wait_time = 0
    mergeable = get_mergeable_value()
    while mergeable == None:
        if wait_time > 30:
            raise 'Github has not calculated PR merge conflicts within 30 seconds. Build again if you would like to check for merge conflict.'
        time.sleep(5)
        wait_time += 5
        mergeable = get_mergeable_value()
    return mergeable

#Returns comment ID if PR already has a merge conflict comment, else false.
def check_pr_comments():
    comment_url = 'https://api.github.com/repos/%s/%s/issues/2/comments' % (REPO_OWNER, REPO_NAME)
    response = session.get(comment_url)
    
    if response == None: #Technically it means github didn't respond so should raise error or send new request but eh...
        return false
    
    responseJson = json.loads(response.content)
    for comment in responseJson:
        if comment['body'] == MERGE_CONFLICT_MSG:
            return comment['id']
    return false

#Deletes comment with corresponding id. Call if message exists but there are no merge conflicts
def delete_comment(id):
    delete_url = 'https://api.github.com/repos/%s/%s/issues/comments/%d' % (REPO_OWNER, REPO_NAME, id)
    session.delete(delete_url)

mergeable = get_pr_mergeable()
comment_id = check_pr_comments()

if mergeable:
    print "PR does NOT have merge conflicts."
    if comment_id:
        delete_comment(id)
        print "Deleted merge conflict message from pull request."
else:
    print "PR has merge conflicts."
    if not comment_id:
        comment_url = 'https://api.github.com/repos/%s/%s/issues/2/comments' % (REPO_OWNER, REPO_NAME)
        comment = {"body": MERGE_CONFLICT_MSG}
        print "Posted merge conflict message."

# if not mergeable:
#     comment_url = 'https://api.github.com/repos/%s/%s/issues/2/comments' % (REPO_OWNER, REPO_NAME)
#     comment = {"body": MERGE_CONFLICT_MSG}
#     print session.post(comment_url, json=comment).content + "\n____________________________\n"
    
#     label_url = 'https://api.github.com/repos/%s/%s/issues/2/labels' % (REPO_OWNER, REPO_NAME)
#     label = ["pr: don't merge - has merge conflicts"]
#     print session.post(label_url, json=label).content
# else:
#     print "File has no merge conflicts."
