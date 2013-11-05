import praw

r = praw.Reddit(user_agent='CapSelAI: comment harvester')
submissions = r.get_subreddit('opensource').get_hot(limit=5)
