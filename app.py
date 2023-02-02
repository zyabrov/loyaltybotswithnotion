from flask import Flask, request
import functions
import credentials

app = Flask(__name__)

notion = functions.Notion(credentials.notion_token)
manychat = functions.Manychat()

@app.route('/new_member', methods=['POST'])
def add_member():
    manychat_data = manychat.get()
    user_id = manychat_data['id']
    user = functions.User(user_id)
    user.get_newuser_manychat_data(manychat_data)
    notion.new_user_page(credentials.notion_db_id, user=user)
    response = {'status': notion.response.status_code, 'data': notion.response.content}
    return response

@app.route('/UpdateSpecialistManychatID', methods=['POST'])
def update_manychat_id():
    manychat_data = request.get_json()
    user = functions.User()
    user.get_manychat_data(manychat_data)


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