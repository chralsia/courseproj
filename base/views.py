from django.template import RequestContext
import re
from django.core.exceptions import ValidationError
from django.shortcuts import render, render_to_response
import pymorphy2 as pm
# Create your views here.
from django.views.generic import TemplateView, FormView
from base.forms import WordForm

verbose_tags = {'Ques': 'вопросительное',
                'Surn': 'фамилия',
                'Vpre': 'Вариант предлога ( со, подо, ...)',
                'sing': 'единственное число',
                'INvl': 'категория совместности',
                'Anph': 'Анафорическое (местоимение)',
                'accs': 'винительный падеж',
                'Subx': 'возможна субстантивация',
                'PRCL': 'частица',
                'Dmns': 'указательное',
                'PRTS': 'причастие (краткое)',
                'Qual': 'качественное',
                'V-be': 'форма на -ье',
                'gent': 'родительный падеж',
                'acc2': 'второй винительный падеж',
                'V-bi': 'форма на -ьи',
                'pssv': 'страдательный залог',
                'Adjx': 'может выступать в роли прилагательного',
                'VOic': 'категория залога',
                'V-ey': 'форма на -ею',
                'Prdx': 'может выступать в роли предикатива',
                'V-oy': 'форма на -ою',
                'Geox': 'топоним',
                'ADJF': 'имя прилагательное (полное)',
                'Fimp': 'деепричастие от глагола несовершенного вида',
                'incl': 'говорящий включён (идем, идемте)',
                'NMbr': 'число',
                'inan': 'неодушевлённое',
                'TRns': 'категория переходности',
                'V-ej': 'форма компаратива на -ей',
                'gen2': 'второй родительный (частичный) падеж',
                'Impe': 'безличный',
                'INFN': 'глагол (инфинитив)',
                'Slng': 'жаргонное',
                'GRND': 'деепричастие',
                'plur': 'множественное число',
                'V-en': 'форма на -енен',
                'ablt': 'творительный падеж',
                'gen1': 'первый родительный падеж',
                'tran': 'переходный',
                'loc2': 'второй предложный (местный) падеж',
                'past': 'прошедшее время', 'Mult': 'многократный',
                'indc': 'изъявительное наклонение',
                'Supr': 'превосходная степень',
                'datv': 'дательный падеж',
                'TEns': 'категория времени',
                'nomn': 'именительный падеж',
                'Coun': 'счётная форма',
                'V-sh': 'деепричастие на -ши',
                'futr': 'будущее время',
                'PErs': 'категория лица',
                'MOod': 'категория наклонения',
                'ASpc': 'категория вида',
                'actv': 'действительный залог',
                'Poss': 'притяжательное',
                'V-ie': 'отчество через -ие-',
                'Anum': 'порядковое', 'Erro': 'опечатка', 'CONJ': 'союз', 'POST': 'часть речи', 'Trad': 'торговая марка', 'PRTF': 'причастие (полное)', '1per': '1 лицо', 'pres': 'настоящее время', 'Dist': 'искажение', 'ADJS': 'имя прилагательное (краткое)', 'intr': 'непереходный', 'Inmx': 'может использоваться как одуш. / неодуш.', 'Init': 'Инициал', 'loc1': 'первый предложный падеж', 'femn': 'женский род', 'Litr': 'литературный вариант', 'ANim': 'одушевлённость / одушевлённость не выражена', '2per': '2 лицо', 'Coll': 'собирательное числительное', 'VERB': 'глагол (личная форма)', 'COMP': 'компаратив', 'Cmp2': 'сравнительная степень на по-', 'impr': 'повелительное наклонение', 'Impx': 'возможно безличное употребление', 'GNdr': 'род / род не выражен', 'excl': 'говорящий не включён в действие (иди, идите)', 'Pltm': 'pluralia tantum', 'neut': 'средний род', 'perf': 'совершенный вид', 'Refl': 'возвратный', 'impf': 'несовершенный вид', 'Prnt': 'вводное слово', 'Patr': 'отчество', 'Sgtm': 'singularia tantum', 'Apro': 'местоименное', 'Abbr': 'аббревиатура', 'loct': 'предложный падеж', 'CAse': 'категория падежа', 'ADVB': 'наречие', 'Fixd': 'неизменяемое', 'Name': 'имя', 'voct': 'звательный падеж', 'anim': 'одушевлённое', 'Arch': 'устаревшее', 'masc': 'мужской род', 'NUMR': 'числительное', 'INTJ': 'междометие', 'PRED': 'предикатив', '3per': '3 лицо', 'Orgn': 'организация', 'NOUN': 'имя существительное', 'Ms-f': 'общий род', 'Infr': 'разговорное', 'NPRO': 'местоимение-существительное', 'Af-p': 'форма после предлога',
                'PREP': 'предлог'
                }


def parse_tag(tg):
    tg_list = re.findall(r'\w+[ ,]?', str(tg))
    tag = ''
    for i in tg_list:
        if re.match(r'\w+ ', i):
            tag += (verbose_tags[i[:-1]] + ' ')
        elif re.match(r'\w+,', i):
            tag += (verbose_tags[i[:-1]] + ',')
        else:
            tag += (verbose_tags[i])
    return tag


class BasicFormView(FormView):
    form_class = WordForm
    template_name = 'index.html'

    def get_request_context(self, request):
        context_instance = RequestContext(request)
        context_instance.push()

    def get(self, request, *args, **kwargs):
        context_instance = RequestContext(request)
        return render_to_response('index.html', {
                'form': WordForm(),
                'menu': 'main',
                'val': '<input type=\"button\" value="Click">'
            }, context_instance)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            anlzr = pm.MorphAnalyzer()
            data = []
            for i in anlzr.parse(form.cleaned_data['word']):
                tag = parse_tag(i.tag)
                data.append({'data': i, 'mth': i.methods_stack[0][0], 'tag': tag})
            context_instance = RequestContext(request)
            return render_to_response('index.html', {
                'data': data,
                'form': WordForm(),
                'menu': 'main',
            }, context_instance)
        else:
            raise ValidationError('Illegal data')


class MainView(BasicFormView):

    def post(self, request, *args, **kwargs):
        pass