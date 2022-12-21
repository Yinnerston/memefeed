import praw
import pmaw
from csv import reader

# Auth information is contained in praw.ini file. See setup.md
reddit = praw.Reddit('memefeedbot')
cache_dir = './cache'
# Comment this out if you need
reddit.read_only = True

pushshift = pmaw.PushshiftAPI(praw=reddit)
# Load csv subreddit list
# with open('data/subreddits.csv', newline='') as subreddits_csv:
#     subreddit_reader = reader(subreddits_csv)
#     for row in subreddit_reader:
#         for subreddit in row:
#             print('-----' + subreddit + '-----')
#             # Get submissions over the last day
#             # TODO: Change settings
#             daily_posts = pushshift.search_submissions(subreddit=subreddit ,mem_safe=True, search_window=1, limit=5, cache_dir='data')
#             for post in daily_posts:
#                 print(post)


posts = reddit.subreddit("anime_irl").top(time_filter="day", limit=10)
for post in posts:
    print(post.title)

print("-----")
daily_posts = pushshift.search_submissions(subreddit='anime_irl', limit=5)
print(daily_posts)
for post in daily_posts:
    print(post)

# Considerations:
# Failure recovery --> Responses are cached, should I retry until finished?
# What about rate limits?

