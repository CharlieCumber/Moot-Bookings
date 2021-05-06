from os import environ
from slack_sdk import WebClient

def send_expression_notification(expression):
    client = WebClient(token=environ.get('SLACK_BOT_TOKEN'))

    blocks = []
    blocks.append({ "type": "header", "text": {"type": "plain_text", "text": f":partyparrot: EOI - {expression.country}", "emoji": True }})
    blocks.append({ "type": "section", "text": {"type": "mrkdwn", "text": f"*{expression.org_name}*\n{expression.contact_full_name}, {expression.contact_position}\n<mailto:{expression.contact_email}|{expression.contact_email}>\n" }})
    blocks.append({ "type": "section", "text": {"type": "mrkdwn", "text": f"*Participants*     {expression.participants}\n*IST*                    {expression.IST}\n*CMT*                 {expression.CMT}\n" }})

    client.chat_postMessage(channel=environ.get('SLACK_CHANNEL_EOI'), blocks=blocks)
