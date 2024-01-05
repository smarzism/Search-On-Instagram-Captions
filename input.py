from flask import Flask, render_template, request
from instagram_private_api import Client, ClientCompatPatch
from instagram_private_api.errors import ClientError

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usernames = request.form['usernames'].split(',')
        keyword = request.form['keyword']

        try:
            api = Client(username, password)
            results = fetch_instagram_data(api, usernames, keyword)
            return render_template('input.html', results=results, keyword=keyword)

        except ClientError as e:
            return f"ClientError: {e}"
    else:
        return render_template('input.html', results=[])


def fetch_instagram_data(api,usernames, keyword):
    search_results = []

    try:

        for username in usernames:
            user_info = api.username_info(username)
            user_id = user_info['user']['pk']

            posts = api.user_feed(user_id)

            for post in posts.get('items', []):
                caption_text = post.get('caption', {}).get('text', '')
                url_code = post.get('code','')
                if keyword in caption_text:
                    search_results.append({'username': username, 'post_id': url_code, 'caption': caption_text})
                    # search_results.append({'username': username, 'post_id': post['code'], 'caption': caption_text})

        return search_results

    except ClientError as e:
        raise e



# def fetch_instagram_data(api, usernames, keyword):
    # search_results = []

    # try:
    #     for username in usernames:
    #         user_info = api.username_info(username)
    #         user_id = user_info['user']['pk']
    #         posts = api.user_feed(user_id)

    #         for post in posts.get('items', []):
    #             caption_text = post.get('caption', {}).get('text', '')
    #             url_code = post.get('code', '')
    #             if keyword in caption_text:
    #                 search_results.append({'username': username, 'post_id': url_code, 'caption': caption_text})

    #     return search_results

    # except ClientError as e:
    #     raise e

if __name__ == '__main__':
    app.run(debug=True)
