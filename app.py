import os
import uuid
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient

from gcloud import create_permission, search_role
from payload import approve_dm, form, reject_dm, reject_text, request_text, success_text

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_PRIVATE_CHANNEL_ID = os.getenv("SLACK_PRIVATE_CHANNEL_ID")

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)

# get perms available from GCP
perm_list = search_role()

perm_request_cache = {}


@app.command("/sesame")
@app.shortcut("request_iam_permission")
def open_modal(ack, body, client: WebClient):
    # Acknowledge the command request
    ack()

    user_id = body["user"]["id"]

    user_response = app.client.users_info(user=user_id)
    user_email = user_response["user"]["profile"]["email"]

    # generate form config
    form_config = form(perms=perm_list, user_email=user_email)

    print(form_config)

    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view=form_config,
    )


@app.view("perm_form")
def handle_view_submission_events(ack, body, client: WebClient):
    ack()

    user_id = body["user"]["id"]
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
            "duration": duration,
            "email": email,
            "channel": channel,
            "timestamp": timestamp,
            "user_id": user_id,
        }
        print(perm_request_cache)


@app.action("request-approved")
def handle_request_approval(ack, body, client: WebClient):
    ack()

    key = body["actions"][0]["value"]
    approver = body["user"]["username"]

    perm_request = perm_request_cache.pop(key, None)

    project = perm_request["project"]
    duration = perm_request["duration"]
    email = perm_request["email"]
    roles = perm_request["perms"]
    user_id = perm_request["user_id"]

    # send text in channel
    success_config = success_text(
        project=project,
        perms=roles,
        duration=duration,
        email=email,
    )

    client.chat_update(
        channel=perm_request["channel"],
        ts=perm_request["timestamp"],
        text="IAM permission approved",
        blocks=success_config,
    )

    if perm_request != None:
        create_permission(
            project=project,
            duration=float(duration),
            email=email,
            roles=roles,
        )

    # send DM to perm requester
    success_dm_config = approve_dm(
        approver=approver,
        project=project,
        perms=roles,
        duration=duration,
        email=email,
    )

    client.chat_postMessage(
        channel=user_id,
        text="IAM permission approved",
        blocks=success_dm_config,
    )


@app.action("request-denied")
def handle_request_rejection(ack, body, client: WebClient):
    ack()

    key = body["actions"][0]["value"]
    approver = body["user"]["username"]

    perm_request = perm_request_cache.pop(key, None)

    project = perm_request["project"]
    duration = perm_request["duration"]
    email = perm_request["email"]
    roles = perm_request["perms"]
    user_id = perm_request["user_id"]

    # send text in channel
    rejection_config = reject_text(
        project=project,
        perms=roles,
        duration=duration,
        email=email,
    )

    client.chat_update(
        channel=perm_request["channel"],
        ts=perm_request["timestamp"],
        text="IAM permission rejected",
        blocks=rejection_config,
    )

    # send DM to perm requester
    reject_dm_config = reject_dm(
        approver=approver,
        project=project,
        perms=roles,
        duration=duration,
        email=email,
    )

    client.chat_postMessage(
        channel=user_id,
        text="IAM permission rejected",
        blocks=reject_dm_config,
    )


@app.action("perm_select-action")
def handle_some_action(ack, body):
    ack()
    print(body)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
