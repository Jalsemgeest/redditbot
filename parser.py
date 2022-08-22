import re
import copy
from enum import Enum

class CommentResponse(Enum):
	UNKNOWN = 1
	HELP = 2
	FLAIR_CHANGE = 3
	FLAIR_NONE = 4

class SubmissionResponse(Enum):
	UNKNOWN = 1
	FUN = 2

class Parser():
	def __init__(self, bot):
		self.bot = bot

	def parseComment(self, comment):
		if re.search('^help', comment.body, re.IGNORECASE):
			return CommentResponse.HELP
		elif re.search('!flair\ {1}[A-Za-z]*\ {1}[A-Za-z]*\ {1}[A-Za-z]*$', comment.body, re.IGNORECASE):
			return CommentResponse.FLAIR_CHANGE
		elif re.search('!noflair', comment.body, re.IGNORECASE):
			return CommentResponse.FLAIR_NONE
		return CommentResponse.UNKNOWN

	def parseSubmission(self, submission):
		flair = None
		print('Parsing submission')
		for (key, value) in self.bot.FLAIR_TYPES.items():
			if value['type'] == 'SUBMISSION':
				# This is required purely do ensure that the template_id matches what is expected.
				if value['id'] == submission.link_flair_template_id and key == submission.link_flair_text:
					flair = key
					break
		if flair == 'Fun':
			return SubmissionResponse.FUN
		return SubmissionResponse.UNKNOWN