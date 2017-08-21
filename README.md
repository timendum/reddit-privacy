# Reddit privacy
A personal project to improve your privacy on [Reddit](http://reddit.com)

## Installation
Clone the repository

    git clone https://github.com/timendum/reddit-privacy.git

Create a Python virtual env and install the requirements

    virtualenv reddit-privacy
    pip install -r requirements.txt

Copy `PRAW.ini.template` to `PRAW.ini` and add your username and password

## Client Key (Reddit API Key)

First, you will need to create a [reddit app](https://www.reddit.com/prefs/apps/).
[Go to Reddit](https://www.reddit.com/prefs/apps/) to create reddit app,
then click "create app" (or it might say "create another app...").

You can name it whatever then select "script". You can enter whatever you want
for the description and for the url you can enter the github url for this
project (https://github.com/timendum/reddit-privacy.git).

Once you enter in the info, you should see a page with a
'personal use key' (in tiny print towards the top left), and a 'secret'. Copy
the 'personal use key' to the PRAW.ini to the client_id and the 'secret' to
the client_secret.

Your PRAW.ini file should look like this:

    [DEFAULT]
    username: your_user_name
    password: your_reddit_password
    client_id: personal_user_script_from_app
    client_secret: secret_from_app

## Delete
The `delete.py` script remove your oldest submissions and comments,
to prevent them to be used for profilation or snooping.

### Usage
Launch the script, by default your credential will be fetched from `PRAW.ini`
or will be asked on the prompt.

    python delete.py -t [days [number]]

You can pass _days_ and _number_ arguments, to change the limits of the script,
by default it delete submissions and comments older than 183 days (~6 months)
and older content if you have more than 900 on history.

The _-t_ option perform a test: the programm will only write what would be deleted
but it will not peform the remove.

#### Examples

    $ python delete.py

To delete **everythying**:

    $ python delete.py 0

To delete anything more than 90 days old:

    $ python delete.py 90
