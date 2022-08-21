from signal import pause
import praw
import os
from game import Game
from bot import Bot
import parser

bot = Bot(botName='JakeEhBot', subreddit='jakeehbottesting', silent=False)

exit()

# for submission in subreddit.hot(limit=5):
# 	print("Title: ", submission.title)

submissionStream = subreddit.stream.submissions(pause_after=-1)
commentStream = subreddit.stream.comments(pause_after=-1) 

if not os.path.isfile("new_submissions_reponded_to.txt"):
    submissions_replied_to = []
else:
    with open("new_submissions_reponded_to.txt", "r") as f:
       submissions_replied_to = f.read()
       submissions_replied_to = submissions_replied_to.split("\n")
       submissions_replied_to = list(filter(None, submissions_replied_to))
       f.close()

if not os.path.isfile("new_comments_reponded_to.txt"):
    comments_replied_to = []
else:
    with open("new_comments_reponded_to.txt", "r") as f:
       comments_replied_to = f.read()
       comments_replied_to = comments_replied_to.split("\n")
       comments_replied_to = list(filter(None, comments_replied_to))
       f.close()

game = Game()

def handleComment(comment):
	print("Attemping to handle comment: ", comment.id)
	type = parser.parseComment(comment)
	match type:
		case parser.CommentResponse.HELP:
			game.help(comment)
		case parser.CommentResponse.UNKNOWN:
			print("Comment has no response needed: ", comment.id)


# This will block and continually fetch new comments within a thread.
try:
	while True:
		for submission in submissionStream:
			if submission is None:
				break
			if submission.id not in submissions_replied_to:
				print(submission)
				print(submission.score)
				print(submission.title)
				print(submission.selftext)
				# submission.reply('Thanks for posting!')
				submissions_replied_to.append(submission.id)
		for comment in commentStream:
			if comment is None:
				break
			if comment.id not in comments_replied_to:
				print(comment.body)
				print(comment.id)
				if comment.author != "JakeEhBot":
					handleComment(comment)
				comments_replied_to.append(comment.id)
				
except KeyboardInterrupt:
	print("Stopped listening")


with open("new_submissions_reponded_to.txt", "w") as f:
    for post_id in submissions_replied_to:
        f.write(post_id + "\n")
    f.close()

with open("new_comments_reponded_to.txt", "w") as f:
    for post_id in comments_replied_to:
        f.write(post_id + "\n")
    f.close()

print("Saved data to files.")