from django import template
from django.template import Variable

register = template.Library()


@register.tag(name="person")
def do_person(parser, token):
	try:
		# split_contents() knows not to split quoted strings.
		tag_name, person_expr = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

	return PersonNode(person_expr)


class PersonNode(template.Node):
    def __init__(self, person_expr):
    	self.person = template.Variable(person_expr)

    def render(self, context):
    	try:
    		person = self.person.resolve(context)

    		return """<a href="/finances/person/{}">{}</a>""".format(
    			person.id,
    			person.nick_name,
    		)
    	except template.VariableDoesNotExist:
    		return "<Unknown>"

