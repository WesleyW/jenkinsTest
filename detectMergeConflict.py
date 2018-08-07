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

if response == None:
    raise 'No response from GitHub.'

content = json.loads(response.content)

if not content['mergeable']:
    comment_url = 'https://api.github.com/repos/%s/%s/issues/2/comments' % (REPO_OWNER, REPO_NAME)
    comment = {"body": "Your pull request has resulted in a merge conflict error."}
    print session.post(comment_url, json.load(comment)).content + "\n____________________________\n"
    
    label_url = 'https://api.github.com/repos/%s/%s/issues/2/labels' % (REPO_OWNER, REPO_NAME)
    label = ["pr: don't merge - has merge conflicts"]
    print session.post(label_url, json.load(label)).content
else:
    print "File has not merge conflicts."
