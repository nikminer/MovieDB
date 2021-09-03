from django import template
from MyWatchList.models import CommentModel


register = template.Library()

@register.inclusion_tag("Main/blocks/comments.html",takes_context=True)
def commentslist(context, item):
    return {
        "comments": CommentModel.comments.get_comments(item).order_by('-id'),
        "user":context['user']
    }


@register.inclusion_tag("Main/blocks/AddComment.html", takes_context=True)
def addcomments(context, item, action ="addCommentMovie"):

    from MyWatchList.forms.Comments import CommentForm
    comment_form = CommentForm()
    return {
        "user": context['user'],
        "commentform": comment_form,
        "item": item,
        "action":action
    }




