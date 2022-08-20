from signal import pause
import praw

reddit = praw.Reddit('JakeEhBot')

subreddit = reddit.subreddit('jakeehbottesting')

# for submission in subreddit.hot(limit=5):
# 	print("Title: ", submission.title)

submissionStream = subreddit.stream.submissions(pause_after=-1)
commentStream = subreddit.stream.comments(pause_after=-1) 

# This will block and continually fetch new comments within a thread.
while True:
	for submission in submissionStream:
		if submission is None:
			break
		print(submission)
		print(submission.score)
		print(submission.title)
		print(submission.selftext)
	for comment in commentStream:
		if comment is None:
			break
		print(comment.body)