from django.core.management.base import BaseCommand
from reddit.models import Submission
from scripts.reddit_etl import RedditETL
import logging
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Run ETL script"

    def handle(self, *args, **kwargs):
        with open("/app/log/reddit_etl.log", "a") as etl_log:
            etl_log.write("Starting ETL:\n")

            RedditETL().run_pipeline()
            cur_day = datetime.now().astimezone()
            prev_day = cur_day - timedelta(days=1)
            tot_count = Submission.objects.filter(created_utc__gte=prev_day).count()
            print(cur_day, "Submissions in the last 24 hours:", tot_count)
            logging.info(
                str(cur_day) + " Submissions in the last 24 hours: " + str(tot_count)
            )

            etl_log.write("Finished ETL:\n")
