from typing import List, TypedDict


class PermSet(TypedDict):
    name: str
    year: int


def form(perms: List[PermSet] = []):
    return {
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
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                                "emoji": True,
                            },
                            "value": "value-0",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                                "emoji": True,
                            },
                            "value": "value-1",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                                "emoji": True,
                            },
                            "value": "value-2",
                        },
                    ],
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
