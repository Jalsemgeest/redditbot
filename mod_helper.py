import uuid
import time

class ModHelper():
	def __init__(self, botInstance):
		self.bot = botInstance
	
	def handleFlairChange(self, comment):
		flairUser = comment.body.split(' ')[1]
		flairType = comment.body.split(' ')[2]
		flairText = comment.body.split(' ')[3]
		if flairText.upper() == "default":
			flairText = ''
		flairTypes = []
		for type in self.bot.FLAIR_TYPES:
			if self.bot.FLAIR_TYPES[type]['type'] == 'USER':
				flairTypes.append(type)
		# flairTypes = list(self.bot.FLAIR_TYPES.keys())
		if flairType in flairTypes:
			self.__setFlair(user=flairUser, text=flairText, templateId=self.bot.FLAIR_TYPES[flairType]['id'])
	
	def handleFlairNone(self, comment):
		flairUser = comment.body.split(' ')[1]
		self.__setFlair(flairUser)

	def __setFlair(self, user, text='', templateId=None):
		self.bot.log('Will update ', user, '\'s flair to: ', templateId, ' with text: ', text)
		self.bot.subreddit.flair.set(redditor=user, text=text, flair_template_id=templateId)

	def handleFunSubmission(self, submission):
		self.bot.trackedFunSubmissions[submission.id] = {
			'author': submission.author.name,
			'hash': uuid.uuid4().hex,
			'datetime': int(time.time() * 1000),
		}
		print(self.bot.trackedFunSubmissions)
		print(submission.id)

