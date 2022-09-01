import ast
import uuid
import json
import os

def readTrackedFunSubmissions():
	try:
		with open("tracked-submissions.fun", "rb") as in_file:
			data = in_file.read()
			if len(data) > 0:
				dictData = data.decode('utf-8')
				dict = ast.literal_eval(dictData)
				return dict
			return {}
	except FileNotFoundError:
		return {}

def writeTrackedFunSubmissions(trackedFunSubmissions):
	print(trackedFunSubmissions)
	with open("tracked-submissions.fun", "wb") as out_file:
		encoded = json.dumps(trackedFunSubmissions, indent=2).encode('utf-8')
		out_file.write(encoded)

def readSubmissions():
	submissions_replied_to = []
	if not os.path.isfile("new_submissions_reponded_to.txt"):
		submissions_replied_to = []
	else:
		with open("new_submissions_reponded_to.txt", "r") as f:
			submissions_replied_to = f.read()
			submissions_replied_to = submissions_replied_to.split("\n")
			submissions_replied_to = list(filter(None, submissions_replied_to))
			f.close()
	return submissions_replied_to

def writeSubmissions(submissions):
	with open("new_submissions_reponded_to.txt", "w") as f:
			for post_id in submissions:
				f.write(post_id + "\n")

def readComments():
	comments_replied_to = []
	if not os.path.isfile("new_comments_reponded_to.txt"):
		comments_replied_to = []
	else:
		with open("new_comments_reponded_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))
			f.close()
	return comments_replied_to

def writeComments(comments):
	with open("new_comments_reponded_to.txt", "w") as f:
			for post_id in comments:
				f.write(post_id + "\n")