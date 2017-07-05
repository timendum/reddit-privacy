from datetime import datetime, timedelta
import praw
import logging

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

REDDIT_HARDLIMIT = 1000 - 1

def main(days_limit=365, number_limit=None):
	r = praw.Reddit(user_agent='python:reddit-privacy-delete:0.2 (by /u/timendum)')
	user = r.user.me()
	# Limits
	if number_limit is not None and number_limit > REDDIT_HARDLIMIT:
		number_limit = REDDIT_HARDLIMIT
	elif number_limit is None:
		number_limit = REDDIT_HARDLIMIT
	created_limit = datetime.now() - timedelta(days=days_limit)
	print(f'Deleting {user.name}\'s submissions and comments made after {created_limit.date()} OR older than their {number_limit}th post')
	# Submission
	submitted = user.submissions.new(limit=None)
	check(submitted, number_limit, created_limit, True)
	comments = user.comments.new(limit=None)
	check(comments, number_limit, created_limit, True)

def check(contents, number_limit, created_limit, delete=False):
	count = 0
	to_delete = []
	for e in contents:
		time = e.created
		submitted = datetime.fromtimestamp(time)
		if submitted < created_limit:
			to_delete.append(e)
			continue

		if count >= number_limit:
			to_delete.append(e)
			continue
		count += 1
	for e in to_delete:
		if e.saved:
			print('Saved ' + e.permalink)
			continue
		try:
			print('Deleting ' + e.permalink)
		except TypeError:
			print('Deleting ' + e.link_permalink + e.id)
		if delete:
			e.delete()

if __name__ == "__main__":
	import sys
	argv = sys.argv

	if len(argv) > 0 and argv[0] == __file__:
		argv = argv[1:]

	days_limit = 366/2
	if len(argv) > 0:
		days_limit = int(argv[0])
	number_limit = 900
	if len(argv) > 1:
		number_limit = int(argv[1])
	main(days_limit, number_limit)
