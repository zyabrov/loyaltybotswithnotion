import requests


class User:
    def __init__(self):
        self.specialist_manychat_id = None
        self.tg_id = None
        self.tg_username = None
        self.notion_page_id = None
        self.specialist_notion_id = None
        self.manychat_data = None
        self.notion_page_url = None

    def get_manychat_data(self, manychat_data):
        self.manychat_data = manychat_data
        self.specialist_manychat_id = manychat_data['id']
        self.tg_id = self.manychat_data['custom_fields']['запит_telegram_id']
        self.tg_username = self.manychat_data['custom_fields']['запит_telegram_username']
        self.tg_url = self.manychat_data['custom_fields']['запит_telegram_url']
        self.notion_page_id = self.manychat_data['custom_fields']['запит_notion_page_id']
        self.phone = self.manychat_data['phone']
        self.specialist_notion_id = self.manychat_data['custom_fields']['notion_user_id']


    def get_manychat_value(self, field, iscustom):
        value = None
        if iscustom == True:
            value = self.manychat_data['custom_fields'][field]
        else:
            value = self.manychat_data[field]
        return value


class Specialist(User):
    def __init__(self):
        super.__init__(self)


class Admin(User):
    def __init__(self, user_id):
        super.__init__(self,user_id)



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


    def get_data(self):
        pass


    def request_accepted(self, page_id, specialist_notion_id):
        self.page_id = page_id
        self.specialist_notion_id = specialist_notion_id

        self.json = {
            'properties': {
                "Етап": { "select": { "name": "Запит прийнято" }},
                "Спеціаліст": { "people": [{ "id": self.specialist_notion_id }] }
                }
            }
        self.update_page_properties()

    def update_manychat_id(self, page_id, manychat_id):
        self.page_id = page_id
        self.manychat_id = int(manychat_id)
        self.json = {
            "properties": {
                "Manychat ID": { "type": "number", "number": self.manychat_id }
                }
            }
        self.update_page_properties()

    def update_page_properties(self):
        self.url = f"https://api.notion.com/v1/pages/{self.page_id}"
        response = requests.patch(self.url, json=self.json, headers=self.headers)
        print("notion request: ", response.content, response.status_code, response.headers.items())