from django import template
from django.template import Library
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from pygments.lexers import HtmlLexer
from pygments.lexers import guess_lexer

import logging
 
register = template.Library() 

logger = logging.getLogger('dashboard')
 
@register.filter(name='pygmentize')
@stringfilter
def pygmentize(text, language): 
	#logger.debug('language : %s' % language)
	try:
		lexer = get_lexer_by_name(language, encoding='UTF-8')
		#lexer = guess_lexer(text)
	except:
		lexer = HtmlLexer()
	return mark_safe(highlight(text, lexer, HtmlFormatter()))
