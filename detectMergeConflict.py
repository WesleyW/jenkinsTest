import os
import json
import requests
import time

#Authentication, repository, and pull request information
USERNAME = os.environ['ghUsername']
PASSWORD = os.environ['ghPassword']
REPO_OWNER = os.environ['repoOwner']
REPO_NAME = os.environ['repoName']
PR_ID = os.environ['CHANGE_ID']

#Creates session to make requests to Github repo.
session = requests.Session()
session.auth = (USERNAME, PASSWORD)

MERGE_CONFLICT_COMMENT = 'Your pull request has resulted in a merge conflict error.'
MERGE_CONFLICT_LABEL = "pr: don't merge - has merge conflicts"

#Returns whether the PR is mergeable - i.e. has no merge conflicts
def get_mergeable_value():
    pr_url = 'https://api.github.com/repos/%s/%s/pulls/%s' % (REPO_OWNER, REPO_NAME, PR_ID)
    response = session.get(pr_url)

    if response == None:
        raise 'No response from GitHub.'

    responseJson = json.loads(response.content)
    if 'mergeable' not in responseJson.keys():
        raise ValueError('Could not check for merge conflicts in response - most likely due to bad credentials.\nResponse:\n' + response.content)
    return json.loads(response.content)['mergeable']

#Check if Github has finished calculating merge conflicts every 5 seconds. Raises error after more than 30 seconds.
def get_mergeable():
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
def check_comments():
    comment_url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (REPO_OWNER, REPO_NAME, PR_ID)
    response = session.get(comment_url)
    
    if response == None: #Technically it means github didn't respond so should raise error or send new request but eh...
        return False
    
    responseJson = json.loads(response.content)
    for comment in responseJson:
        if comment['body'] == MERGE_CONFLICT_COMMENT:
            return comment['id']
    return False

#Deletes comment with corresponding id. Call if message exists but there are no merge conflicts
def delete_comment(id):
    delete_url = 'https://api.github.com/repos/%s/%s/issues/comments/%d' % (REPO_OWNER, REPO_NAME, id)
    session.delete(delete_url)
    
#Returns true if PR has merge conflict label, else false.
def check_labels():
    label_url = 'https://api.github.com/repos/%s/%s/issues/%s/labels' % (REPO_OWNER, REPO_NAME, PR_ID)
    response = session.get(label_url)
    
    if response == None: #Technically it means github didn't respond so should raise error or send new request but eh...
        return False
    
    responseJson = json.loads(response.content)
    print responseJson
    for label in responseJson:
        if label['name'] == MERGE_CONFLICT_LABEL:
            return True
    return False

#Deletes merge conflict label. Call if label is tagged but no merge conflict exists.
def delete_label():
    delete_url = 'https://api.github.com/repos/%s/%s/issues/%s/%s' % (REPO_OWNER, REPO_NAME, PR_ID, MERGE_CONFLICT_LABEL)
    session.delete(delete_url)



mergeable = get_mergeable()
comment_id = check_comments()
has_label = check_labels()

if mergeable:
    print "PR does NOT have merge conflicts."
    if comment_id:
        delete_comment(id)
        print "Deleted merge conflict message from pull request."
    if has_label:
        delete_label()
        print "Deleted merge conflict label."
else:
    print "PR has merge conflicts."
    if comment_id:
        print "Merge conflict message was already posted."
    else:
        comment_url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (REPO_OWNER, REPO_NAME, PR_ID)
        comment = {"body": MERGE_CONFLICT_COMMENT}
        session.post(comment_url, json=comment)
        print "Posted merge conflict message."
        
    if has_label:
        print "Merge conflict label was already added."
    else:
        label_url = 'https://api.github.com/repos/%s/%s/issues/%s/labels' % (REPO_OWNER, REPO_NAME, PR_ID)
        session.post(label_url, json=[MERGE_CONFLICT_LABEL])
        print "Added merge conflict label."
