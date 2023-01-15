from scripts.reddit_etl import RedditETL
from datetime import datetime, timedelta
from reddit.models import Submission

RedditETL().run_pipeline()
prev_day = datetime.now().astimezone() - timedelta(days=1)
print(
    "Submissions in the last 24 hours:",
    Submission.objects.filter(created_utc__gte=prev_day).count(),
)
