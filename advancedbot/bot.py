import os
import parser
import praw
import filehelper
from parser import Parser
from communication import Communication
from fungame import FunGame
from mod_helper import ModHelper

# Things I want to add support for:
# - Random hash generated and stored for comment thread with specific flair
# - Maybe a game or something... but probably not a priority... ;)

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
		self.trackedFunSubmissions = filehelper.readTrackedFunSubmissions()
		self.comms = Communication(self)
		self.funGame = FunGame(self)
		self.populateFlairTypes()
		self.populateMods()
		self.modHelper = ModHelper(self)
		self.parser = Parser(self)
		self.readOrCreateLogs()

	def populateFlairTypes(self):
		for flair in self.subreddit.flair.templates:
			self.FLAIR_TYPES[flair['text']] = {
				'id': flair['id'],
				'css_class': flair['css_class'],
				'type': 'USER',
			}
		for flair in self.subreddit.flair.link_templates:
			self.FLAIR_TYPES[flair['text']] = {
				'id': flair['id'],
				'css_class': flair['css_class'],
				'type': 'SUBMISSION',
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
						if submission.author != self.botName:
							self.handleSubmission(submission)
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
	
	def handleSubmission(self, submission):
		self.log("Attempting to handle submission: ", submission.id)
		type = self.parser.parseSubmission(submission)
		match type:
			case parser.SubmissionResponse.FUN:
				if self.isMod(submission.author):
					self.modHelper.handleFunSubmission(submission)
			case parser.SubmissionResponse.UNKNOWN:
				self.log("Submission has no response needed: ", submission.id)

	def handleComment(self, comment):
		self.log("Attemping to handle comment: ", comment.id)
		type = self.parser.parseComment(comment)
		match type:
			case parser.CommentResponse.HELP:
				self.comms.help(comment)
			case parser.CommentResponse.FLAIR_CHANGE:
				if self.isMod(comment.author):
					self.modHelper.handleFlairChange(comment)
			case parser.CommentResponse.FLAIR_NONE:
				if self.isMod(comment.author):
					self.modHelper.handleFlairNone(comment)
			case parser.CommentResponse.FUN_ATTEMPT:
				self.funGame.attemptFun(comment)
			case parser.CommentResponse.UNKNOWN:
				self.log("Comment has no response needed: ", comment.id)

	def isMod(self, user):
		# Check if the user is a mod
		return user in self.MODS

	def readOrCreateLogs(self):
		self.submissions_replied_to = filehelper.readSubmissions()
		self.comments_replied_to = filehelper.readComments()

	def log(self, *toPrint):
		if not self.silent:
			print(toPrint)

	def saveState(self):
		# We could
		filehelper.writeSubmissions(self.submissions_replied_to)
		filehelper.writeComments(self.comments_replied_to)
		print("tracked")
		print(self.trackedFunSubmissions)
		filehelper.writeTrackedFunSubmissions(self.trackedFunSubmissions)
