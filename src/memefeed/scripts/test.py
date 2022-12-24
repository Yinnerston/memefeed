import praw
import psaw

r = praw.Reddit("memefeedbot")
r.read_only = True
api = psaw.PushshiftAPI(r)
