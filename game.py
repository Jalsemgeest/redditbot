
class GameHelper():
	def createMessage(arr):
		return '\n\n'.join(arr)

class Game():
	def __init__(self):
		self.name = 'RPG Game'
	
	# When help is called with a given stream, it will respond to the stream
	# with information on what the bot can do.
	def help(self, stream):
		msg = [
			"Don\'t worry! JakeEhBot is here!",
			"Here are the \'commands\' I currently support:",
			"* _help_: This command - duh.",
			"* _game_: Explains what game I support."
		]
		stream.reply(GameHelper.createMessage(msg))

		