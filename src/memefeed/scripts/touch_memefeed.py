"""
Open memefeed.xyz using Chrome through Selenium to refresh/initialize caches
"""
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://memefeed.xyz")
driver.get("https://memefeed.xyz/?page=2&sort_by=")
subreddits = [
    "anime_irl",
    "Animemes",
    "goodanimemes",
    "HistoryMemes",
    "me_irl",
    "MEOW_IRL",
    "starterpacks",
    "wholesomememes",
    "evangelionmemes",
    "HistoryAnimemes",
    "woof_irl",
    "surrealmemes",
]
for subreddit in subreddits:
    driver.get(
        "https://memefeed.xyz/search/results?q=&subreddit=%s&author=&sort_by=0"
        % subreddit
    )
    driver.get("https://memefeed.xyz/subreddit/%s" % subreddit)
