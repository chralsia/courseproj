import re

from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView, FormView
from sympy import *
from sympy.printing.latex import latex
from sympy.printing.mathml import mathml
from sympy.parsing.sympy_parser import parse_expr

from base.forms import SearchForm, ExpressionForm


def main(request):
    add_context = {}
    context_instance = RequestContext(request)
    context_instance.push({
                'form': SearchForm(),
                'menu': 'main',
                'expr_form': ExpressionForm(),
            })
    if request.method == 'POST':
        form = ExpressionForm(request.POST)
        if form.is_valid():
            expr = form.cleaned_data['expression']
            add_context['data'] = latex(parse_expr(expr), mode='equation', itex=True)
        else:
            raise ValidationError('Illegal data')
    return render_to_response('index.html', add_context, context_instance)
