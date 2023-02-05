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

@app.route('/manychat/<api_method>', methods=['POST'])
def manychat_request(api_method):
    manychat_data = request.get_json()
    user = functions.User()
    user.get_manychat_data(manychat_data)
    if api_method == 'UpdateSpecialistManychatID':
        response = update_manychat_id(user)
    elif api_method == 'GetNotionUserInfo':
        response = notion.get_user_data(user)
    elif api_method == 'ArrayToString':
        response = functions.array_to_string(user.manychat_data)
    return response



def update_manychat_id(user):
    user.page_id = user.manychat_data['custom_fields']['notion_page_id']
    notion.update_manychat_id(user.page_id, user.specialist_manychat_id)
    response = {'status':'ok', 'notion_page_url': user.notion_page_url}
    return response


@app.route('/', methods=['GET'])
def test():
    print('Get request')