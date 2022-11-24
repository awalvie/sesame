import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from gcloud import search_role
from payload import form

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)

# get perms available from GCP
perm_list = search_role()

# generate form config
form_config = form(perm_list)


@app.command("/sesame")
@app.shortcut("request_iam_permission")
def open_modal(ack, body, client):
    # Acknowledge the command request
    ack()

    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view=form_config,
    )


@app.view("")
def handle_view_submission_events(ack, body, logger):
    ack()
    print(body)
    logger.info(body)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
