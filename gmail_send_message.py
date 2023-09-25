# From Googleworkspace's Github
# https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/create_draft.py
# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 

from oauth_quickstart import get_oauth_creds

import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Create and send an email message
# Print the returned  message id
# Returns: Message object, including message id
# use oauth creds
  
def gmail_send_message(dest_email, pr_summary_message):
  """
  Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id
  use oauth creds
  """
  try:
    service = build('gmail', 'v1', credentials=get_oauth_creds())
    message = EmailMessage()

    message.set_content(pr_summary_message)

    message['To'] = dest_email
    message['From'] = 'madajiji@gmail.com'
    message['Subject'] = 'This week\'s pull requests summary'

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
        .decode()

    create_message = {
        'raw': encoded_message
    }
    # pylint: disable=E1101
    send_message = (service.users().messages().send
                    (userId="me", body=create_message).execute())
    print(F'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(F'An error occurred: {error}')
    send_message = None
  return send_message