import praw

reddit = praw.Reddit('JakesBot')

subreddit = reddit.subreddit('pythonforengineers')

# for submission in subreddit.hot(limit=5):
# 	print("Title: ", submission.title)

# This will block and continually fetch new comments within a thread.
for comment in subreddit.stream.comments():
    print(comment.body)