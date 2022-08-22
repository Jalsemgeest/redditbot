import os
import parser
import praw
from communication import Communication
from mod_helper import ModHelper

class Bot():
	def __init__(self, botName='JakeEhBot', subreddit='jakeehbottesting', silent=True):
		self.silent = silent
		self.log('Initializing bot.')
		self.FLAIR_TYPES = {}
		self.MODS = []
		self.botName = botName
		self.reddit = praw.Reddit(botName)
		self.subredditName = subreddit
		self.subreddit = self.reddit.subreddit(subreddit)
		self.comms = Communication()
		self.populateFlairTypes()
		self.populateMods()
		self.modHelper = ModHelper(self)
		self.readOrCreateLogs()

	def populateFlairTypes(self):
		for flair in self.subreddit.flair.templates:
			self.FLAIR_TYPES[flair['text']] = {
				'id': flair['id'],
				'css_class': flair['css_class']
			}
		self.log('Retrieved flairs: ', self.FLAIR_TYPES)
	
	def populateMods(self):
		for mod in self.subreddit.moderator():
			self.MODS.append(mod.name)

	def listen(self):
		# Will listen to new comments and posts.
		self.submissionStream = self.subreddit.stream.submissions(pause_after=-1)
		self.commentStream = self.subreddit.stream.comments(pause_after=-1) 
		try:
			while True:
				for submission in self.submissionStream:
					if submission is None:
						break
					if submission.id not in self.submissions_replied_to:
						self.log(submission)
						self.log(submission.score)
						self.log(submission.title)
						self.log(submission.selftext)
						# submission.reply('Thanks for posting!')
						self.submissions_replied_to.append(submission.id)
				for comment in self.commentStream:
					if comment is None:
						break
					if comment.id not in self.comments_replied_to:
						self.log(comment.body)
						self.log(comment.id)
						if comment.author != self.botName:
							self.handleComment(comment)
						self.comments_replied_to.append(comment.id)
		except KeyboardInterrupt:
			self.log("Stopped listening")
			self.saveState()
		
	
	def handleComment(self, comment):
		self.log("Attemping to handle comment: ", comment.id)
		type = parser.parseComment(comment)
		match type:
			case parser.CommentResponse.HELP:
				self.comms.help(comment)
			case parser.CommentResponse.FLAIR_CHANGE:
				if self.isMod(comment.author):
					self.modHelper.handleFlairChange(comment)
			case parser.CommentResponse.FLAIR_NONE:
				if self.isMod(comment.author):
					self.modHelper.handleFlairNone(comment)
			case parser.CommentResponse.UNKNOWN:
				self.log("Comment has no response needed: ", comment.id)

	def isMod(self, user):
		# Check if the user is a mod
		return user in self.MODS

	def readOrCreateLogs(self):
		if not os.path.isfile("new_submissions_reponded_to.txt"):
			self.submissions_replied_to = []
		else:
			with open("new_submissions_reponded_to.txt", "r") as f:
				self.submissions_replied_to = f.read()
				self.submissions_replied_to = self.submissions_replied_to.split("\n")
				self.submissions_replied_to = list(filter(None, self.submissions_replied_to))
				f.close()

		if not os.path.isfile("new_comments_reponded_to.txt"):
			self.comments_replied_to = []
		else:
			with open("new_comments_reponded_to.txt", "r") as f:
				self.comments_replied_to = f.read()
				self.comments_replied_to = self.comments_replied_to.split("\n")
				self.comments_replied_to = list(filter(None, self.comments_replied_to))
				f.close()

	def log(self, *toPrint):
		if not self.silent:
			print(toPrint)

	def saveState(self):
		# We could 
		with open("new_submissions_reponded_to.txt", "w") as f:
			for post_id in self.submissions_replied_to:
				f.write(post_id + "\n")
			f.close()

		with open("new_comments_reponded_to.txt", "w") as f:
			for post_id in self.comments_replied_to:
				f.write(post_id + "\n")
			f.close()
		self.log("Saved data to files.")
