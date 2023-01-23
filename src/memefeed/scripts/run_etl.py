"""
Deprecasted by reddit management command.
"""

from scripts.reddit_etl import RedditETL
from datetime import datetime, timedelta
from reddit.models import Submission
import logging

logging.basicConfig(
    filename="/app/memefeed/log/reddit_etl.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)


with open("/app/log/reddit_etl.log", "a") as etl_log:
    etl_log.write("Starting ETL:\n")

    RedditETL().run_pipeline()
    cur_day = datetime.now().astimezone()
    prev_day = cur_day - timedelta(days=1)
    tot_count = Submission.objects.filter(created_utc__gte=prev_day).count()
    print(cur_day, "Submissions in the last 24 hours:", tot_count)
    logging.info(str(cur_day) + " Submissions in the last 24 hours: " + str(tot_count))

    etl_log.write("Finished ETL:\n")
