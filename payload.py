import json
from typing import List, TypedDict


class PermSet(TypedDict):
    description: str
    etag: str
    name: str
    stage: str
    title: str


class OptionText(TypedDict):
    text: str
    emoji: bool
    type: str


class SelectOption(TypedDict):
    text: OptionText
    value: str


def form(perms: List[PermSet] = []):

    multi_select_option_list: List[SelectOption] = []

    for perm in perms:

        formatted_perm: SelectOption = {
            "text": {
                "text": perm.get("title", "Perm title"),
                "type": "plain_text",
                "emoji": True,
            },
            "value": perm.get("name", "Permission name"),
        }

        multi_select_option_list.append(formatted_perm)

    return json.dumps(
        {
            "title": {"type": "plain_text", "text": "Open Sesame", "emoji": True},
            "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
            "type": "modal",
            "callback_id": "perm_form",
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": ":wave: Hey, please fill this form to request permission from infra team.",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "input",
                    "block_id": "project_choice",
                    "label": {
                        "type": "plain_text",
                        "text": "Select project",
                        "emoji": True,
                    },
                    "element": {
                        "type": "radio_buttons",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Development",
                                    "emoji": True,
                                },
                                "value": "deepsource-development",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Production",
                                    "emoji": True,
                                },
                                "value": "deepsource-production",
                            },
                        ],
                        "action_id": "project_choice-action",
                    },
                },
                {
                    "type": "section",
                    "block_id": "permission_choice",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Choose Permission",
                    },
                    "accessory": {
                        "type": "multi_static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select permissions you need",
                            "emoji": True,
                        },
                        "options": multi_select_option_list,
                        "action_id": "perm_select-action",
                    },
                },
                {
                    "type": "input",
                    "block_id": "duration_choice",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a duration",
                            "emoji": True,
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "10m",
                                    "emoji": True,
                                },
                                "value": "10",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "30m",
                                    "emoji": True,
                                },
                                "value": "30",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "1 hour",
                                    "emoji": True,
                                },
                                "value": "60",
                            },
                        ],
                        "action_id": "duration_select-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Choose duration",
                        "emoji": True,
                    },
                },
                {
                    "type": "input",
                    "block_id": "email_input",
                    "element": {
                        "type": "email_text_input",
                        "action_id": "email-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Enter your company email",
                        "emoji": True,
                    },
                },
            ],
        }
    )


def request_text(project: str, perms: List[str], duration: str, email: str, key: str):
    perm_string = ":construction: Permissions: " + ", ".join(
        map(lambda x: f"`{x}`", perms)
    )
    project_string = ":gear: Project: " + project
    email_string = ":mailbox: User email: " + email
    duration_string = ":timer_clock: Duration: " + duration

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You have a new permission request:",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": perm_string,
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": project_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": email_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": duration_string},
        },
        {
            "type": "actions",
            "block_id": "approval_choice",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "emoji": True, "text": "Approve"},
                    "style": "primary",
                    "value": key,
                    "action_id": "request-approved",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "emoji": True, "text": "Deny"},
                    "style": "danger",
                    "value": key,
                    "action_id": "request-denied",
                },
            ],
        },
    ]


def success_text(
    project: str,
    perms: List[str],
    duration: str,
    email: str,
):
    perm_string = ":white_check_mark: Permissions: " + ", ".join(
        map(lambda x: f"`{x}`", perms)
    )
    project_string = ":gear: Project: " + project
    email_string = ":mailbox: User email: " + email
    duration_string = ":timer_clock: Duration: " + duration

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You have a new permission request:",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": perm_string,
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": project_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": email_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": duration_string},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":tada: Permission successfully provided.",
            },
        },
    ]


def reject_text(
    project: str,
    perms: List[str],
    duration: str,
    email: str,
):
    perm_string = ":x: Permissions: " + ", ".join(map(lambda x: f"`{x}`", perms))
    project_string = ":gear: Project: " + project
    email_string = ":mailbox: User email: " + email
    duration_string = ":timer_clock: Duration: " + duration

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You have a new permission request:",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": perm_string,
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": project_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": email_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": duration_string},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":no_entry: Permission request denied.",
            },
        },
    ]


def approve_dm(
    approver: str,
    project: str,
    perms: List[str],
    duration: str,
    email: str,
):
    title_string = "The following permission request has been approved by @" + approver
    perm_string = ":white_check_mark: Permissions: " + ", ".join(
        map(lambda x: f"`{x}`", perms)
    )
    project_string = ":gear: Project: " + project
    email_string = ":mailbox: User email: " + email
    duration_string = ":timer_clock: Duration: " + duration

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": title_string,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": perm_string,
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": project_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": email_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": duration_string},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":tada: Permission successfully provided.",
            },
        },
    ]


def reject_dm(
    approver: str,
    project: str,
    perms: List[str],
    duration: str,
    email: str,
):
    title_string = "The following permission request has been rejected by @" + approver
    perm_string = ":x: Permissions: " + ", ".join(map(lambda x: f"`{x}`", perms))
    project_string = ":gear: Project: " + project
    email_string = ":mailbox: User email: " + email
    duration_string = ":timer_clock: Duration: " + duration

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": title_string,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": perm_string,
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": project_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": email_string},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": duration_string},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":no_entry: Permission request denied.",
            },
        },
    ]
