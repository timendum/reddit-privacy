# Reddit privacy
A personal project to improve your privacy on [Reddit](http://reddit.com)

## Installation
Clone the repository

    git clone https://github.com/timendum/reddit-privacy.git
    
Create a Python virtual env and install the requirements 

    virtualenv reddit-privacy
    pip install -r requirements.txt

Copy `PRAW.ini.template` to `PRAW.ini` and add your username and password

## Delete
The `delete.py` script remove your oldest submissions and comments,
to prevent them to be used for profilation or snooping.

### Usage
Launch the script, by default your credential will be fetched from `PRAW.ini`
or will be asked on the prompt.

    python delete.py [days [number]]
 
You can pass _days_ and _number_ arguments, to change the limits of the script,
by default it delete submissions and comments older than 183 days (~6 months)
and older content if you have more than 900 on history.
