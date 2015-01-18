from django import template
from django.template import Variable

register = template.Library()


@register.tag(name="login_form")
def do_login_form(parser, token):
	try:
		# split_contents() knows not to split quoted strings.
		tag_name = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

	return PersonNode(person_expr)
