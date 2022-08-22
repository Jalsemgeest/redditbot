import re
from enum import Enum

class CommentResponse(Enum):
	UNKNOWN = 1
	HELP = 2
	FLAIR_CHANGE = 3
	FLAIR_NONE = 4


def parseComment(comment):
	if re.search('^help', comment.body, re.IGNORECASE):
		return CommentResponse.HELP
	elif re.search('!flair\ {1}[A-Za-z]*\ {1}[A-Za-z]*\ {1}[A-Za-z]*$', comment.body, re.IGNORECASE):
		return CommentResponse.FLAIR_CHANGE
	elif re.search('!noflair', comment.body, re.IGNORECASE):
		return CommentResponse.FLAIR_NONE
	return CommentResponse.UNKNOWN
