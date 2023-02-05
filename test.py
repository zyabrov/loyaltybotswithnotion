{
    "parent": {
        "database_id": {{gaf_3381606}}
    },
    "properties": {
        "title": {
            "title": [{
                "text": {
                    "content": "{{full_name}}"
                }
            }]
        },
        "Manychat ID": {
            "type": "number",
            "number": {{user_id}}
        },
        "Instagram Username": {
            "type": "rich_text",
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "{{ig_username}}"
                }
            }]
        },
        "Підписник": {
                "type": "select",
                "select": {
                "name": "{{is_ig_account_follower}}"
                }
        },
        "Коли запустив бот": {
            "type": "date",
            "date": {
                "start": {{subscribed|format:datetime(SHORT)|to_json:true}}
            }
        },
        "Остання взаємодія": {
            "type": "date",
            "date": {
                "start": {{last_ig_seen|format:datetime(SHORT)|to_json:true}}
            }
        }                
    },
}