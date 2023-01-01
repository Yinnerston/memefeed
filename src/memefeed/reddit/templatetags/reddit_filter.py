from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe
import sentry_sdk
register = template.Library()

@register.filter(name='display_media', needs_autoescape=True)
def display_media(submission, autoescape=True):
    # Define escape function for arguments
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    # Get corresponding html element to media type via submission.domain
    article = None
    tmp_url = None
    try:
        if submission.domain == "i.redd.it" or submission.domain == "i.imgur.com":
            # Image (jpg, png, gif) from reddit or imgur
            tmp_url = esc(submission.url)
            article = f'<a href="{tmp_url}" class="image"><img src="{tmp_url}" alt="" id="{submission.id}"></a>'
        elif submission.domain == "v.redd.it":
            # Video
            pass
            # TODO: Exception on crosspost because keyerror
            # TODO: Video not implemented
            # tmp_url = esc(submission.media["reddit_video"]["fallback_url"])
            # article = f'<a href="{tmp_url}" class="image"><img src="{tmp_url}" alt="" id="{submission.id}"></a>'
            # article = f'<a href="{tmp_url}" class="image"><video poster="{{% static \'reddit/images/thumbs/placeholder.jpg\' %}}" id="{submission.id}"><source src="{tmp_url}" type="video/mp4"></video></a>'
        elif submission.domain == "reddit.com":
            # Gallery
            pass
        else:
            # Other submission.domains
            pass
    except Exception as e:
        # Report exception and do not render
        sentry_sdk.capture_exception(e)

    return mark_safe(article)

