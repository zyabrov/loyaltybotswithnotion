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
    print('Got Manychat Request')
    manychat_data = request.get_json()
    print(manychat_data)
    user = functions.User(manychat_id=manychat_data['id'])
    user.manychat_data = manychat_data
    response = ''
    """
    if api_method == 'GetNotionUserInfo':
        response = notion.get_user_data(user)
        
    """
    if api_method == 'ArrayToString':
        response = user.manychat_data['array']
        print(response)
    return response


def update_manychat_id(user):
    user.page_id = user.manychat_data['custom_fields']['notion_page_id']
    notion.update_manychat_id(user.page_id, user.specialist_manychat_id)
    response = {'status': 'ok', 'notion_page_url': user.notion_page_url}
    return response
