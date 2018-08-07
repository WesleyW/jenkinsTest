import os
import json
import requests

#Authentication and repository information
USERNAME = os.environ['ghUsername']
PASSWORD = os.environ['ghPassword']
REPO_OWNER = os.environ['repoOwner']
REPO_NAME = os.environ['repoName']

pr_url = 'https://api.github.com/repos/%s/%s/pulls/2' % (REPO_OWNER, REPO_NAME)

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
response = session.get(pr_url)

if response == null:
    raise 'No response from GitHub.'

content = json.loads(response).content

if not content.mergeable:
    comment_url = 'https://api.github.com/repos/%s/%s/issues/2/comments' % (REPO_OWNER, REPO_NAME)
    comment = {"body": "Your pull request has resulted in a merge conflict error."}
    session.post(comment_url, comment)
    
    label_url = 'https://api.github.com/repos/%s/%s/issues/2/labels' % (REPO_OWNER, REPO_NAME)
    label = "pr: don't merge - has merge conflicts"
    session.post(label_url, label)
