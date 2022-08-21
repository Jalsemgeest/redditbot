import re
from enum import Enum

class CommentResponse(Enum):
	UNKNOWN = 1
	HELP = 2
	GAME = 3

def parseComment(comment):
	if re.search("^help", comment.body, re.IGNORECASE):
		return CommentResponse.HELP
	elif re.search("^game", comment.body, re.IGNORECASE):
		return CommentResponse.GAME
	return CommentResponse.UNKNOWN
