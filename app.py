import praw
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('secret_key')
USER_AGENT = os.getenv('user_agent')

def create_reddit_client():
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    return reddit

def get_images(client, subreddit_name, limit):
    subreddit = client.subreddit(subreddit_name)
    posts = subreddit.hot(limit=limit)
    for post in posts:
        if post.url.endswith(('.jpg', '.jpeg', '.png', 'gif')):
            response = requests.get(post.url)
            file_path = f"memes/{subreddit_name}_{post.id}{os.path.splitext(post.url)[1]}"
            if not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                    print(f"Downloaded {file_path}")
            else:
                print(f"Skipped {file_path} (already downloaded)")
        else:
            print(f"Skipped {post.url} (not an image)")

client = create_reddit_client()
subreddit_names = ['funny', 'jokes', 'comedy', 'notfunny', 'bonehurtingjuice', 'ComedyCemetery', 'comedyheaven', 'ComedyNecrophilia', 'comedynecromancy', 'comedyamputation', 'okbuddyretard', 'Ooer', 'fifthworldpics', 'infiniteworldproblems', 'DeepFriedMemes', 'nukedmemes', 'blackholedmemes', 'bigbangedmemes', 'QuantumedMemes', 'deletedmemes', 'ScottishPeopleTwitter', 'fakehistoryporn', 'FellowKids', 'me_irl', 'meirl', '2meirl4meirl', 'comedyhomicide', 'comedynuke', 'ComedyHitmen', 'boottoobig', 'ComedyCemeteryLore', 'gametheorymemes', 'THE_PACK', 'AROOOOOOO', 'surrealmemes']  
limit = 20  # 
while True:
    for subreddit_name in subreddit_names:
        get_images(client, subreddit_name, limit)
        time.sleep(3)  
    time.sleep(60)  
