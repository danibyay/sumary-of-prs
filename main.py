from github_get_pr_summary import get_pr_summary
from gmail_send_message import gmail_send_message
import sys

if __name__ == "__main__":
  github_token = str(sys.argv[1])
  email_dest = 'danybecerr+testing@gmail.com'
  pr_summary_message = get_pr_summary(github_token)
  #gmail_send_message(email_dest, pr_summary_message)

  # option to print to the console instead of send email
  print(pr_summary_message)


