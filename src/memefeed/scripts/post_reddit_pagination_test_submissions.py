"""
Need to create a reddit script app and add it to the praw.ini file under the name "memefeedscript"
Script to add submissions to r/test_memefeed for pagination testing.
"""
import praw


r = praw.Reddit("memefeedscript")
meow = r.subreddit("meow_irl").top(time_filter="year", limit=50)
dataset = [
    submission.url
    for submission in meow
    if submission.url.endswith(".jpg")
    and submission.url.startswith("https://i.redd.it/")
]
for idx, entry in enumerate(dataset):
    # Change the subreddit to your own test subreddit if you want.
    r.subreddit("test_memefeed").submit("Test Post Pagination: " + str(idx), url=entry)


# r.subreddit("test_memefeed").submit("Test Post Pagination: Final", url="https://i.redd.it/upmhjg0nm8k81.jpg")
"""
Ids of example submissions created through this script: 
ids = ['107fh18', '107fh1j', '107fh1v', '107fh26', '107fh2n', '107fh2y', '107fh3g', '107fh3q', '107fh3z', '107fh46', '107fh4c', '107fh4k', '107fh58', '107fh5g', '107fh5q', '107fh5y', '107fh68', '107fh6b', '107fh6i', '107fh6r', '107fh72', '107fh7c', '107fh7q', '107fh83', '107fh8s', '107fh94', '107fh9j', '107fha0', '107fhac', '107fhaq', '107fhb3', '107fhbd', '107fhbm', '107fhbv', '107fhc3', '107fhce', '107fhcq', '107fhd3', '107fhdd', '107fhdp']
fullnames = ['t3_107fh18', 't3_107fh1j', 't3_107fh1v', 't3_107fh26', 't3_107fh2n', 't3_107fh2y', 't3_107fh3g', 't3_107fh3q', 't3_107fh3z', 't3_107fh46', 't3_107fh4c', 't3_107fh4k', 't3_107fh58', 't3_107fh5g', 't3_107fh5q', 't3_107fh5y', 't3_107fh68', 't3_107fh6b', 't3_107fh6i', 't3_107fh6r', 't3_107fh72', 't3_107fh7c', 't3_107fh7q', 't3_107fh83', 't3_107fh8s', 't3_107fh94', 't3_107fh9j', 't3_107fha0', 't3_107fhac', 't3_107fhaq', 't3_107fhb3', 't3_107fhbd', 't3_107fhbm', 't3_107fhbv', 't3_107fhc3', 't3_107fhce', 't3_107fhcq', 't3_107fhd3', 't3_107fhdd', 't3_107fhdp']
"""
