from django import template
from Main.models import Comment
from django.shortcuts import render
register = template.Library()

@register.inclusion_tag("Main/blocks/comments.html")
def commentslist(item):
    return {
        "comments": Comment.comments.get_comments(item).order_by('-id')
    }




