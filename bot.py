import random
import json
import requests
import logging
import string

logging.basicConfig(level=logging.DEBUG)

with open('config.json') as file:
    config = json.load(file)

NUMBER_OF_USERS = config['number_of_users']
MAX_POSTS_PER_USER = config['max_posts_per_user']
MAX_LIKES_PER_USER = config['max_likes_per_user']

BASE_URL = 'http://127.0.0.1:8000'


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def signup(username, password):
    url = BASE_URL + '/auth/users/'
    data = {
        'username': username,
        'password': password
    }
    resp = requests.post(url, data=data)
    if resp.status_code == 201:
        return data


def login(username, password):
    url = BASE_URL + '/auth/jwt/create/'
    resp = requests.post(url, data={
        'username': username,
        'password': password
    })
    if resp.status_code == 200:
        return resp.json()


def create_post(access_token, text):
    url = BASE_URL + '/posts/'
    data = {'text': text}
    requests.post(url, headers={'Authorization': 'Bearer ' + access_token}, data=data)


def get_posts(access_token):
    url = BASE_URL + '/posts/'
    resp = requests.get(url, headers={'Authorization': 'Bearer ' + access_token})
    return resp.json()


def like_post(access_token, post_id):
    url = BASE_URL + f'/posts/{post_id}/like/'
    requests.post(url, headers={'Authorization': 'Bearer ' + access_token})


class Bot:
    def __init__(self):
        self.users = []
        self.tokens = []

    def run(self):
        self.create_users()
        self.login_all()
        self.create_posts()
        self.like_posts()

    def create_users(self):
        self.users = [signup(username=generate_random_string(8), password=generate_random_string(8)) for _ in
                      range(NUMBER_OF_USERS)]

    def login_all(self):
        self.tokens = [login(username=item['username'], password=item['password'])['access'] for item in self.users]

    def create_posts(self):
        for token in self.tokens:
            for _ in range(MAX_POSTS_PER_USER):
                create_post(token, text=" ".join(
                    [generate_random_string(random.randrange(3, 12)) for _ in range(random.randrange(20, 101))]))

    def like_posts(self):
        if self.tokens:
            posts = get_posts(self.tokens[0])['results']
            for token in self.tokens:
                random.shuffle(posts)
                for post in posts[:MAX_LIKES_PER_USER]:
                    like_post(token, post['id'])


if __name__ == '__main__':
    bot = Bot()
    bot.run()
