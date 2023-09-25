import requests
import json
from datetime import datetime, timedelta
from dateutil import parser, tz 

## TODO: Include the status on the first line (change format of message)
## TODO: Validate that response or lists to iterate are not empty, if empty, print message and exit
# or send email that there are no pr meeting the criteria

test_set = [
  ("jaytaph", "gosub-browser"), # 13 in the last week
  ("opentofu", "opentofu"),     # 30 in the last week
  ("geerlingguy", "ansible-for-devops"), # only has one in the last week
  ("robertdebock", "ansible-role-cups"), # zero activity in the last week
  ("actions", "runner-images") # 30 in the last week
]
test_instance = 3

REPO_OWNER = test_set[test_instance][0]
REPO_NAME = test_set[test_instance][1]

# Use the github API to list all pull requests from a given repository
# where state = {open, in draft, closed}
# Returns a list of dictionaries, each pull request object is a dictionary
def get_pull_requests_data(owner, repo, token):
  api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
  headers = {
    "Accept": "application/vnd.github+json", 
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28" 
  }
  params = {"state" : "all"}
  response = requests.get(api_url, headers=headers, params=params)
  return response.json()

# Filter the list of PRs to only have those that have been created in the last week
# Returns a list of dictionaries
def filter_prs_by_age(list_of_prs):
  filtered_list = []
  # get a datetime object of the date of one week ago
  now = datetime.now(tz=tz.tzlocal())
  one_week_ago = now + timedelta(days=-7)
  # evaluate each pr's created_at attribute
  for pr in list_of_prs:
    pr_date_string = pr["created_at"]
    pr_datetime_object = parser.parse(pr_date_string)
    if pr_datetime_object >= one_week_ago:
      filtered_list.append(pr)
    else: 
      # Since they are sorted, the first one that doesnt match is the last one we want to check
      break
  return filtered_list

# Select only main attributes of the PR objects to generate an easy to read summary
# Returns a list of dictionaries
def get_pr_relevant_metadata(list_of_prs):
  trimmed_down_list = []
  for pr in list_of_prs:
    pr_condensed = dict()
    pr_condensed["title"] = pr["title"]
    pr_condensed["state"] = pr["state"]
    pr_condensed["created_at"] = pr["created_at"]
    pr_condensed["html_url"] = pr["html_url"]
    pr_condensed["is_draft"] = pr["draft"]
    trimmed_down_list.append(pr_condensed)
  return trimmed_down_list

# From a json date string extract MM/DD format
# example input: "2011-04-10T20:09:31Z"
# example output: "04/10"
def get_human_date(date_string):
  datetime_object = parser.parse(date_string)
  return f"{datetime_object.month}/{datetime_object.day}"

# Merge the properties state and is_draft into one, for better readability in the summary
# Returns string describing the state of the PR
def get_simpler_status(state, is_draft):
  status = ""
  if is_draft:
    status = "draft"
  else:
    # either open or closed
    status = state
  return status

# Build a string of the summary to be printed or sent as email
def build_summary_message(list_of_prs):
  if len(list_of_prs) == 0:
    message = "There are no pull requests to show"
  else:
    message = "Summary of last week's PRs\n"
    for i in range(len(list_of_prs)):
      title = list_of_prs[i]["title"]
      status = get_simpler_status(list_of_prs[i]["state"], list_of_prs[i]["is_draft"])
      date = get_human_date(list_of_prs[i]["created_at"])
      url = list_of_prs[i]["html_url"]
      message += f"\n{i+1}. {title}\n"
      message += f"PR status is: {status}\n"
      message += f"PR was created on {date}\n"
      message += f"Read more at: {url}\n"
  return message


# Call all the pull requests related functions to return the summary string
def get_pr_summary(github_pat):
  all_prs = get_pull_requests_data(REPO_OWNER, REPO_NAME, github_pat)
  desired_prs = filter_prs_by_age(all_prs)
  pr_extracted_metadata = get_pr_relevant_metadata(desired_prs)
  message = build_summary_message(pr_extracted_metadata)
  return message






