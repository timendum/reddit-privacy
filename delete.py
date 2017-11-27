import argparse
from datetime import datetime, timedelta
from operator import attrgetter
import logging
import praw

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

REDDIT_HARDLIMIT = 1000 - 1

def main(days_limit=365, number_limit=None, test=True):
    r = praw.Reddit(user_agent='python:reddit-privacy-delete:0.3 (by /u/timendum)')
    user = r.user.me()
    # Limits
    if number_limit is not None and number_limit > REDDIT_HARDLIMIT:
        number_limit = REDDIT_HARDLIMIT
    elif number_limit is None:
        number_limit = REDDIT_HARDLIMIT
    created_limit = datetime.now() - timedelta(days=days_limit)
    if test:
        print('Printing', end='')
    else:
        print('Deleting', end='')
    print(
        ' {}\'s submissions and comments made before {} OR older than the {}th contet'.format(
            user.name, created_limit.date(), number_limit))
    # Submission
    submitted = set(user.submissions.hot(limit=None))
    submitted = submitted | set(user.submissions.new(limit=None))
    submitted = submitted | set(user.submissions.top(limit=None))
    submitted = submitted | set(user.submissions.controversial(limit=None))
    submitted = sorted(submitted, key=attrgetter('created'), reverse=True)
    check(submitted, number_limit, created_limit, test)
    # Comments
    comments = set(user.comments.hot(limit=None))
    comments = comments | set(user.comments.new(limit=None))
    comments = comments | set(user.comments.top(limit=None))
    comments = comments | set(user.comments.controversial(limit=None))
    comments = sorted(comments, key=attrgetter('created'), reverse=True)
    check(comments, number_limit, created_limit, test)

def check(contents, number_limit, created_limit, test=True):
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
        if not test:
            e.delete()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Remove posts and comments from Reddit.')
    parser.add_argument('days_limit',
                        metavar='DAYS',
                        type=int,
                        nargs='?',
                        default=366 / 2,
                        help='Content older than D days will be deleted')
    parser.add_argument('number_limit',
                        metavar='NUM',
                        type=int,
                        nargs='?',
                        default=900,
                        help='Content older than N-th will be deleted')
    parser.add_argument("-t", "--test",
                        action="store_true",
                        help="Don't delete, perform a test")
    args = parser.parse_args()
    main(args.days_limit, args.number_limit, args.test)
