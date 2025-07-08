import praw

def get_reddit():
    reddit = praw.Reddit(
        client_id='d6PhF1j_wq2xvhOWhpZ7kA',
        client_secret='dmFNcPLk1XsMlP1tsqvaNAki-pOjNw',
        password='Elaine-xgz@0309',
        user_agent='my user agent for college project, by Xinwei',
        username='Born-Medicine-4623'
    )
    reddit.read_only = True
    return reddit