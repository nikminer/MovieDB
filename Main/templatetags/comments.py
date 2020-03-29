from django import template
from MyWatchList.models import CommentModel


register = template.Library()

@register.inclusion_tag("Main/blocks/comments.html")
def commentslist(item):
    return {
        "comments": CommentModel.comments.get_comments(item).order_by('-id')
    }

@register.inclusion_tag("Main/blocks/AddComment.html",takes_context=True)
def addcomments(context):

    from MyWatchList.forms import CommentForm
    comment_form = CommentForm()

    return {
        "user": context['user'],
        "commentform": comment_form,
    }

