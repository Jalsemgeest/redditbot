from datetime import datetime
from dateutil.relativedelta import relativedelta
from enum import Enum

class FunState(Enum):
	UNKNOWN = 1
	WINNER = 2
	WINNER_EXISTS = 3
	LOSER = 4

class FunGame():
	def __init__(self, bot):
		self.bot = bot

	def attemptFun(self, comment):
		# We should only respond to direct replies to the thread
		if comment.parent_id.startswith('t1'):
			print('Not handling a comment that is not top level')
			return

		funState = self.checkForFun(comment)
		id = comment.submission.id
		if funState == FunState.WINNER:
			funSub = self.bot.trackedFunSubmissions[id]
			time = funSub['datetime']
			originalTime = datetime.fromtimestamp(time/1000)
			now = datetime.now()
			delta = relativedelta(now, originalTime)
			deltaString = self.getDeltaString(delta)

			# Reply to the post and then store that it's been won.
			author = str(comment.author)
			self.bot.trackedFunSubmissions[id]['winner'] = author
			comment.reply(body='Congratulations! You won! It took ' + deltaString + ' for someone to be crowned a winner!')
			# Handle updating the users badge count
		elif funState == FunState.WINNER_EXISTS:
			existingWinner = self.bot.trackedFunSubmissions[id]['winner']
			# reply with the winner
			print('Existing winner is ', existingWinner)
			comment.reply(body='It looks like ' + existingWinner + '  has already won.')

		elif funState == FunState.LOSER:
			print('Did not win')
			comment.reply(body='That was an incorrect guess.')
			# Reply with this


	def checkForFun(self, comment):
		funGuess = comment.body.split(' ')[1]
		targettedId = comment.submission.id
		if targettedId in self.bot.trackedFunSubmissions:
			if len(self.bot.trackedFunSubmissions[targettedId]['winner']) > 0:
					return FunState.WINNER_EXISTS
			if self.bot.trackedFunSubmissions[targettedId]['hash'] == funGuess:
				return FunState.WINNER
		return FunState.LOSER

	def getDeltaString(self, delta):
		timeString = ''
		if delta.years > 0:
			if delta.years == 1:
				timeString += '1 year, '
			else:
				timeString += str(delta.years) + ' years, '
		if delta.months > 0:
			if delta.months == 1:
				timeString += '1 month, '
			else:
				timeString += str(delta.months) + ' months, '
		if delta.days > 0:
			if delta.days == 1:
				timeString += '1 day, '
			else:
				timeString += str(delta.days) + ' days, '
		if delta.minutes > 0:
			if delta.minutes == 1:
				timeString += '1 minute, '
			else:
				timeString += str(delta.minutes) + ' minutes, '
		if delta.seconds == 1:
			timeString += 'and 1 second'
		else:
			timeString += 'and ' + str(delta.seconds) + ' seconds'
		return timeString

