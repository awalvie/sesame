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
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Choose Permission",
                    },
                    "accessory": {
                        "type": "multi_static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select ermissions you need",
                            "emoji": True,
                        },
                        "options": multi_select_option_list,
                        "action_id": "perm_select-action",
                    },
                },
                {
                    "type": "input",
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
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Choose duration",
                        "emoji": True,
                    },
                },
                {
                    "type": "input",
                    "element": {"type": "email_text_input"},
                    "label": {
                        "type": "plain_text",
                        "text": "Enter your company email",
                        "emoji": True,
                    },
                },
            ],
        }
    )
