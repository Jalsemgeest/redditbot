import os
import praw

reddit = praw.Reddit("JakeEhTestBot")
sub = reddit.subreddit("jakeehbottesting")

subStream = ''
commentStream = ''
subsRepliedTo = []
commentsRepliedTo = []

def readData():
	if not os.path.isfile("new_submissions_reponded_to.txt"):
		subsRepliedTo = []
	else:
		with open("new_submissions_reponded_to.txt", "r") as f:
			subsRepliedTo = f.read()
			subsRepliedTo = subsRepliedTo.split("\n")
			subsRepliedTo = list(filter(None, subsRepliedTo))
	if not os.path.isfile("new_comments_reponded_to.txt"):
		commentsRepliedTo = []
	else:
		with open("new_comments_reponded_to.txt", "r") as f:
			commentsRepliedTo = f.read()
			commentsRepliedTo = commentsRepliedTo.split("\n")
			commentsRepliedTo = list(filter(None, commentsRepliedTo))

def saveData():
	with open("new_submissions_reponded_to.txt", "w") as f:
			for post_id in subsRepliedTo:
				f.write(post_id + "\n")
	with open("new_comments_reponded_to.txt", "w") as f:
			for post_id in commentsRepliedTo:
				f.write(post_id + "\n")

readData()

# Listen to everything
def listen():
	subStream = sub.stream.submissions(pause_after=-1, skip_existing=True)
	commentStream = sub.stream.comments(pause_after=-1, skip_existing=True)
	try:
		while True:
			for submission in subStream:
				if submission is None:
					break
				if submission.id not in subsRepliedTo:
					print(submission.id)
					print(submission.score)
					print(submission.selftext)
					subsRepliedTo.append(submission.id)
					print('Responding to submission titled: ', submission.selftext)
					submission.reply(body='JakeEhTestBot is here to have fun!')
			for comment in commentStream:
				if comment is None:
					break
				if comment.id not in commentsRepliedTo and comment.author != "JakeEhTestBot":
					print(comment.id)
					print(comment.body)
					print(comment.author)
					print('Responding to comment with body: ', comment.body)
					commentsRepliedTo.append(comment.id)
					comment.reply(body='JakeEhTestBot sees this!')
	except KeyboardInterrupt:
		saveData()

listen()
