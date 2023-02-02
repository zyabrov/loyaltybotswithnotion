from flask import Flask, request
import functions
import credentials

app = Flask(__name__)

notion = functions.Notion(credentials.notion_token)

@app.route('/request_accepted', methods=['POST'])
def manychat_request():
    manychat_data = request.get_json()
    user = functions.User()
    user.get_manychat_data(manychat_data)
    notion.request_accepted(user.notion_page_id, user.specialist_notion_id)
    response = {'status':'ok', 'notion_page_url': user.notion_page_url}
    return response

@app.route('/UpdateSpecialistManychatID', methods=['POST'])
def update_manychat_id():
    manychat_data = request.get_json()
    user = functions.User()
    user.specialist_manychat_id = manychat_data['id']
    user.page_id = manychat_data['custom_fields']['notion_page_id']
    notion.update_manychat_id(user.page_id, user.specialist_manychat_id)
    response = {'status':'ok', 'notion_page_url': user.notion_page_url}
    return response


@app.route('/', methods=['GET'])
def test():
    print('Get request')



@app.route('/notion', methods=['GET', 'POST'])
def notion_request(user):
    pass