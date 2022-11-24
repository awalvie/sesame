import os
import uuid
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from gcloud import create_permission, search_role
from payload import form, request_text

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_PRIVATE_CHANNEL_ID = os.getenv("SLACK_PRIVATE_CHANNEL_ID")

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)

# get perms available from GCP
perm_list = search_role()

# generate form config
form_config = form(perm_list)

perm_request_cache = {}


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


@app.view("perm_form")
def handle_view_submission_events(ack, body, client):
    ack()
    values = body["view"]["state"]["values"]
    project = values["project_choice"]["project_choice-action"]["selected_option"][
        "value"
    ]
    duration = values["duration_choice"]["duration_select-action"]["selected_option"][
        "value"
    ]
    email = values["email_input"]["email-action"]["value"]

    permDictList = values["permission_choice"]["perm_select-action"]["selected_options"]
    perms = []

    for perm in permDictList:
        perms.append(perm["value"])

    key = uuid.uuid4().hex

    request_config = request_text(project, perms, duration, email, key)

    result = client.chat_postMessage(
        channel=SLACK_PRIVATE_CHANNEL_ID,
        text="IAM permission requested",
        blocks=request_config,
    )

    if result["ok"]:
        timestamp = result["ts"]
        channel = result["channel"]
        perm_request_cache[key] = {
            "project": project,
            "perms": perms,
            "duration": float(duration),
            "email": email,
            "channel": channel,
            "timestamp": timestamp,
        }
        print(perm_request_cache)


@app.message("send")
def send_text(ack, client):
    ack()

    request_config = request_text(
        project="development",
        perms=[
            "roles/accesscontextmanager.gcpAccessAdmin",
            "roles/accessapproval.viewer",
        ],
        duration="30",
        email="vaibhav@deepsource.io",
    )

    print(request_config)

    result = client.chat_postMessage(
        channel=SLACK_PRIVATE_CHANNEL_ID,
        text="IAM permission requested",
        blocks=request_config,
    )

    print(result)


@app.action("request-approved")
def handle_request_approval(ack, body):
    ack()

    key = body["actions"][0]["value"]
    perm_request = perm_request_cache.pop(key, None)

    print("CALLING GCP")
    print(perm_request)

    if perm_request != None:
        create_permission(
            project=perm_request["project"],
            duration=perm_request["duration"],
            email=perm_request["email"],
            roles=perm_request["perms"],
        )


@app.action("request-denied")
def handle_some_action(ack, body):
    ack()
    print(body)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
