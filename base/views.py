import re
import sys
import math

from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView, FormView
from sympy import *
from sympy.printing.latex import latex
from sympy.parsing.sympy_parser import parse_expr

from base.forms import SearchForm, ExpressionForm


class MathComputer:

    def check(self, parsedf, x, f, a, b):
        der = lambdify(x, diff(parsedf, x))
        if f(a)*f(b) <= 0 and der(a)*der(b) >= 0:
            return True
        else:
            return False

    def choose(self, f, a, b):
        mid = (a+b)/2.0
        if f(a)*f(mid) <= 0:
            return a
        else:
            return b

    def __init__(self, exprf, from_=0, to_=1):
        a = from_ if from_ else 0
        b = to_ if to_ else 1
        self.x = symbols('x')
        self.parsedf = parse_expr(exprf)
        self.f = lambdify(self.x, self.parsedf)
        self.m = diff(self.parsedf, self.x)
        self.derivative = lambdify(self.x, self.m)
        while self.check(self.parsedf, self.x, self.f, a, b) != True or math.fabs(a-b) > 0.1:
            if a == self.choose(self.f, a, b):
                b = (a+b)/2.0
            else:
                a = (a+b)/2.0
        self.x0 = (a+b)/2.0

    def checkConditions(self, x0, f, parsedf):
        x = self.x
        der = lambdify(x, diff(parsedf, x))
        der2 = lambdify(x, diff(diff(parsedf, x), x))
        h0 = math.fabs(- f(x0)/der(x0))
        M = math.fabs(der2(x0))
        m = math.fabs(der(x0))
        if f(x0)*der(x0) != 0 and 2*h0*M <= m:
            return True
        else:
            return False

    def newton(self):
        if self.checkConditions(self.x0, self.f, self.parsedf):
            tmpx0 = self.x0
            x1 = tmpx0 - self.f(tmpx0)/self.derivative(tmpx0)
            while math.fabs(tmpx0-x1) > 10**(-15):
                tmpx0 = x1
                x1 = tmpx0 - self.f(tmpx0)/self.derivative(tmpx0)
            print x1
            return x1
        else:
            print "It isn't solving in this interval"

    def tangent(self):
        if self.checkConditions(self.x0, self.f, self.parsedf):
            derx0 = self.derivative(self.x0)
            tmpx0 = self.x0
            x1 = tmpx0 - self.f(tmpx0)/derx0
            while math.fabs(tmpx0-x1) > 10**(-5):
                tmpx0 = x1
                x1 = tmpx0 - self.f(tmpx0)/derx0
            print x1
            return x1
        else:
            print "It isn't solving in this interval"

    def secant(self):
        if self.checkConditions(self.x0, self.f, self.parsedf):
            tmpx0 = self.x0
            x1 = tmpx0 - self.f(tmpx0)/self.derivative(self.x0)
            x2 = x1 - self.f(x1)*((x1 - tmpx0)/(self.f(x1) - self.f(tmpx0)))
            while math.fabs(x2-x1) > 10**(-5):
                tmpx0 = x1
                x1 = x2
                x2 =  x1 - self.f(x1)*((x1 - tmpx0)/(self.f(x1) - self.f(tmpx0)))
            print x2
            return x2
        else:
            print "It isn't solving in this interval"

    def chords(self):
        if self.checkConditions(self.x0, self.f, self.parsedf):
            x1 = self.x0 - self.f(self.x0)/self.derivative(self.x0)
            x2 = x1 - self.f(x1)*((x1 - self.x0)/(self.f(x1) - self.f(self.x0)))
            while math.fabs(x2-x1) > 10**(-5):
                x1 = x2
                x2 = x1 - self.f(x1)*((x1 - self.x0)/(self.f(x1) - self.f(self.x0)))
            print x2
            return x2
        else:
            print "It isn't solving in this interval"

    def latex_print(expr):
        return latex(parse_expr(expr), mode='equation', itex=True)


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
            from_ = form.cleaned_data['from_']
            to_ = form.cleaned_data['to_']
            computer = MathComputer(expr, from_, to_)
            computer.newton()
            computer.tangent()
            computer.secant()
            computer.chords()
            add_context['data'] = MathComputer.latex_print(expr)
        else:
            raise ValidationError('Illegal data')
    return render_to_response('index.html', add_context, context_instance)
