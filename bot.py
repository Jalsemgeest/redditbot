import praw

reddit = praw.Reddit('JakesBot')

subreddit = reddit.subreddit('learnpython')

for submission in subreddit.hot(limit=5):
	print("Title: ", submission.title)