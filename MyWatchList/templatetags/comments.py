from django import template
from MyWatchList.models import CommentModel, ReplyModel


register = template.Library()

@register.inclusion_tag("Main/blocks/comments.html",takes_context=True)
def commentslist(context, item):
    return {
        "comments": CommentModel.comments.get_comments(item).order_by('-id'),
        "user":context['user']
    }

@register.inclusion_tag("Main/blocks/replys.html")
def LastReply(item):
    return {
        "replys": ReplyModel.objects.filter(item=item).order_by('-id').last()
    }

@register.inclusion_tag("Main/blocks/replys.html")
def ReplyList(item):
    return {
        "replys": ReplyModel.objects.filter(item=item).order_by('-id')
    }

@register.inclusion_tag("Main/blocks/AddComment.html", takes_context=True)
def addcomments(context, item, action ="addCommentMovie"):

    from MyWatchList.forms import CommentForm
    comment_form = CommentForm()
    return {
        "user": context['user'],
        "commentform": comment_form,
        "item": item,
        "action":action
    }

@register.inclusion_tag("Main/blocks/AddReply.html", takes_context=True)
def addreply(context, item):

    from MyWatchList.forms import ReplyForm
    comment_form = ReplyForm()
    
    return {
        "user": context['user'],
        "replyform": comment_form,
        "item":item,
    }



