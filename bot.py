import praw
class Bot():
	def __init__(self, botName='JakeEhBot', subreddit='jakeehbottesting', silent=True):
		self.silent = silent
		self.log('Initializing bot.')
		self.FLAIR_TYPES = {}
		self.reddit = praw.Reddit(botName)
		self.subredditName = subreddit
		self.subreddit = self.reddit.subreddit(subreddit)
		self.populateFlairTypes()

	def populateFlairTypes(self):
		for flair in self.subreddit.flair.templates:
			self.FLAIR_TYPES[flair['text']] = flair['id']
		self.log('Retrieved flairs: ', self.FLAIR_TYPES)

	def listen(self):
		# Will listen to new comments and posts.
		print('Unimplemented')

	def log(self, *toPrint):
		if not self.silent:
			print(toPrint)

	def saveFlairs(self):
		# Will save flairs
		print('Unimplemented')
