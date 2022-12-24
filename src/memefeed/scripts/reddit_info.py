"""
Moved draft functions here
"""
# class RedditETLInfo:
#     def __init__(self) -> None:
#         pass



#     def get_daily_posts(self, subreddit):
#         # Pushshift is too buggy...
#         top_submissions = requests.get(f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&after=1d\
#             &fields=id\
#             &size=5")
#         body = []
#         print(top_submissions)
#         print(top_submissions.request.body)
#         print("---")
#         if (top_submissions.status_code == 200):
#             body = top_submissions.request.body
#             print(body)
#             return body
#         else:
#             sentry_sdk.capture_message(top_submissions)


#     def extract_info(self):
#         """
#         You need id to get batches.. 
#         """
#         posts = []
#         with open(RedditETL.SUBREDDITS_CSV, newline="") as subreddits_csv:
#             subreddit_reader = reader(subreddits_csv)
#             for row in subreddit_reader:
#                 # Prune invalid strings / validate strings according to reddit subreddit naming convention
#                 valid_subreddits_in_row = [
#                     sr for sr in row if match("^[A-Za-z0-9_]{3,21}$", sr)
#                 ]
#                 # Iterate over subreddits
#                 new_posts = []
#                 try:
#                     # Get top N posts daily from each subreddit in the list
#                     new_posts = self.reddit.info(subreddits=valid_subreddits_in_row)
#                 except praw.exceptions.PRAWException as err:
#                     # On error, report to Sentry
#                     sentry_sdk.capture_exception(err)
#                 else:
#                     # TODO: Join subreddit --> Subreddit model
#                     # TODO: Join author --> author model
#                     # TODO: Batch load to postgres
#                     posts.append(new_posts)
#         return posts

#     def transform_info(self, info):
#         for generator in info:
#             for batch in generator:
#                 print(batch)
