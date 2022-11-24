import os
from dotenv import load_dotenv
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

payload_file = open("payload.json")
payload = json.load(payload_file)
payload_file.close()

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)


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
        view=payload["form"],
    )


@app.view("")
def handle_view_submission_events(ack, body, logger):
    ack()
    print(body)
    logger.info(body)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
