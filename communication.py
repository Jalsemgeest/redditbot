
class CommunicationHelper():
	def createMessage(arr):
		return '\n\n'.join(arr)

class Communication():
	def __init__(self):
		self.name = 'RPG Game'
	
	# When help is called with a given stream, it will respond to the stream
	# with information on what the bot can do.
	def help(self, stream):
		msg = [
			"Don\'t worry! JakeEhBot is here!",
			"Here are the \'commands\' I currently support:",
			"* _help_: This command - duh.",
			"Mod Only:",
			"* _!flair <user> <flair> <text_nospaces>_: Sets a user's flair to the provided flair with the provided text (default uses default)",
			"* _!noflair <user>_: Sets a users flair to nothing"
		]
		stream.reply(CommunicationHelper.createMessage(msg))

		