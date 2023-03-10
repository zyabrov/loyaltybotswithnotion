import requests
from flask import request

"""
def array_to_string(array):
    text = None
    for string in array:
        if text is None:
            text = string
        else:
            text = text + '\n' + string
    response = {
        'text': text,
        'quantity': len(array)
    }

    return response

"""

def list_to_diclist(names, list_to_change):
    return dict(zip(names, list_to_change))


class User:
    def __init__(self, manychat_id):
        self.id = manychat_id
        self.name = None
        self.manychat_data = None
        self.notion_page_id = None
        self.notion_page_url = None

    def get_newuser_manychat_data(self, manychat_data):
        self.manychat_data = manychat_data
        self.name = self.manychat_data['name']
        self.profile_pic = self.manychat_data['profile_pic']
        self.live_chat_url = self.manychat_data['live_chat_url']
        self.subscribed = self.manychat_data['subscribed']
        self.last_seen = self.manychat_data['last_seen']
        self.ig_username = self.manychat_data['ig_username']
        self.ig_id = self.manychat_data['ig_id']
        self.last_growth_tool = self.manychat_data['last_growth_tool']

    def get_manychat_value(self, field, iscustom):
        iscustom = None
        if iscustom:
            value = self.manychat_data['custom_fields'][field]
        else:
            value = self.manychat_data[field]
        return value


class Manychat:
    def __init__(self) -> None:
        self.data = None

    def get(self) -> dict:
        self.data = request.get_json()
        return self.data


class Notion:
    def __init__(self, notion_token):
        self.url = None
        self.token = notion_token
        self.headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            'Authorization': f"Bearer {self.token}"
        }
        self.json = None
        self.response = None
        self.page_id = None
        self.database_id = None
        self.response = None

    def get_page_data(self, page_id):
        self.page_id = page_id
        self.url = f'https://api.notion.com/v1/pages{self.page_id}'
        self.response = requests.get(self.url, headers=self.headers)

    def new_user_page(self, database_id, user):
        self.database_id = database_id
        self.url = 'https://api.notion.com/v1/pages'
        self.user = user
        self.json = {
            "parent": {
                "database_id": self.database_id
            },
            "properties": {
                "title": {
                    "title": [{
                        "text": {
                            "content": user.name
                        }
                    }]
                },
                "????'??": {
                    "type": "rich_text",
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": user.name
                        }
                    }]
                },
                "Manychat ID": {
                    "type": "number",
                    "number": user.id
                },
                "Instagram Username": {
                    "type": "rich_text",
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": user.ig_username
                        }
                    }]
                },
                "Instagram ID": {
                    "type": "number",
                    "number": user.ig_id
                },
                "???????? ????????????????????": {
                    "type": "date",
                    "date": {
                        "start": user.subscribed
                    }
                },
                "?????????????? ??????????????????": {
                    "type": "date",
                    "date": {
                        "start": user.last_seen
                    }
                }
            },
            "children": []
        }
        self.create_page()

    def create_page(self):
        self.response = requests.post(self.url, json=self.json, headers=self.headers)
        return self.response

    def request_accepted(self, page_id, specialist_notion_id):
        self.page_id = page_id
        self.specialist_notion_id = specialist_notion_id

        self.json = {
            'properties': {
                "????????": {"select": {"name": "?????????? ????????????????"}},
                "????????????????????": {"people": [{"id": self.specialist_notion_id}]}
            }
        }
        self.update_page_properties()

    def update_manychat_id(self, page_id, manychat_id):
        self.page_id = page_id
        self.manychat_id = int(manychat_id)
        self.json = {
            "properties": {
                "Manychat ID": {"type": "number", "number": self.manychat_id}
            }
        }
        self.update_page_properties()

    def update_page_properties(self):
        self.url = f"https://api.notion.com/v1/pages/{self.page_id}"
        response = requests.patch(self.url, json=self.json, headers=self.headers)
        print("notion request: ", response.content, response.status_code, response.headers.items())
