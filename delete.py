from datetime import datetime, timedelta
import praw
import logging

logger = logging.getLogger(__package__)
logger.setLevel(logging.NOTSET)
logger.addHandler(logging.StreamHandler())

REDDIT_HARDLIMIT = 1000 - 1

def main(days_limit=365, number_limit=None):
	r = praw.Reddit(user_agent='python:reddit-privacy-delete:0.1 (by /u/timendum)')
	r.login(disable_warning=True)
	user = r.user
	# Limits
	if number_limit is not None and number_limit > REDDIT_HARDLIMIT:
		number_limit = REDDIT_HARDLIMIT
	elif number_limit is None:
		number_limit = REDDIT_HARDLIMIT
	created_limit = datetime.now() - timedelta(days=days_limit)
	print('Criteria: user %s\'s submissions and comments older then %s days OR then the %dth content' % (user.name, created_limit.isoformat(), number_limit))
	# Submission
	submitted = user.get_submitted(sort='new', limit=None)
	check(submitted, number_limit, created_limit)
	# Comments
	comments = user.get_comments(sort='new', limit=None)
	check(comments, number_limit, created_limit)

def check(contents, number_limit, created_limit):
	count = 0
	for e in contents:
		time = e.created
		submitted = datetime.fromtimestamp(time)
		if submitted < created_limit:
			print('Deleting ' + e.permalink)
			e.delete()
			continue

		if count >= number_limit:
			print('Deleting ' + e.permalink)
			e.delete()
		else:
			count += 1

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