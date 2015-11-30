# coding=utf-8
import os

from django import template


register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value.file.name)

@register.assignment_tag
def total_question(questions, statusId, check_moderation = False):
	if check_moderation:
		answers = questions.filter(moderated=True, nouabookItem_id=statusId)
	else:
		answers = questions.filter(nouabookItem_id=statusId)
	return answers.count if answers else 0

@register.filter
def is_image(value):
	try:
		filename, ext = os.path.splitext(value.file.name)
		if ext in ['.jpg', '.png', '.gif', '.jpeg']:
			return True
		else:
			return False
	except:
		return False