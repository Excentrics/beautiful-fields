# -*- coding: utf-8 -*-
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from lxml import etree

'''
#---------------------------------
import logging
from django.conf import settings
logger = logging.getLogger(settings.PROJECT_NAME)
#---------------------------------
'''


class RangeWidget(widgets.Widget):

    def __init__(self,
                 attrs=None,
                 max_value=None, min_value=None,
                 template='beautiful_fields/range_widget.html',
                 limits=True, # Show or not limits
                 step=1, # Step of pointer
                 dimension='', # Show this after number. dimension='&nbsp;$'
                 skin=None, # skin='plastic'
                 space=None, # Space method None or 'logarithmic'
                 scale=None, # Labels under slider, '|' — show just line. scale=(0, '|', 50, '|', '100', '|', 250, '|', 500)
                 heterogeneity=None, # (<percentage of point on slider>, <value in that point). heterogeneity=((50, 100), (75, 250)),
                 round=0, # How many numbers allowed after comma
                 single=False,
                 labels=True # 'labels=False' to disable slider labels
    ):
        self.min_value, self.max_value, self.template = min_value, max_value, template
        self.limits, self.step, self.dimension, self.skin = limits, step, dimension, skin
        self.space, self.scale, self.heterogeneity, self.round, self.single = space, scale, heterogeneity, round, single
        self.labels = labels
        super(RangeWidget, self).__init__(attrs)

    def value_from_datadict(self, data, files, name):
        value = data.get(name, '').split(';')
        if len(value) < 2:
            value.append(value[0])
        return value

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'start_value': value[0],
            'end_value': value[1],
            'min_value': self.min_value,
            'max_value': self.max_value,
            'limits': self.limits,
            'step': self.step,
            'dimension': self.dimension,
            'skin': self.skin,
            'space': self.space,
            'scale': self.scale,
            'heterogeneity': self.heterogeneity,
            'round': self.round,
            'single': self.single,
            'labels': self.labels
        }
        return render_to_string(self.template, context)


def make_readonly(form):
    """
    Makes all fields on the form readonly and prevents it from POST hacks.
    """

    def _get_cleaner(_form, field):
        def clean_field():
            return getattr(_form.instance, field, None)
        return clean_field

    for field_name in form.fields.keys():
        form.fields[field_name].widget = ReadOnlyWidget(
            initial_widget=form.fields[field_name].widget)
        setattr(form, "clean_" + field_name,
                _get_cleaner(form, field_name))

    form.is_readonly = True


class ReadOnlyWidget(widgets.Select):
    """
    Renders the content of the initial widget in a hidden <span>. If the
    initial widget has a ``render_readonly()`` method it uses that as display
    text, otherwise it tries to guess by parsing the html of the initial widget.
    """
    input_type = 'readonly'

    def __init__(self, initial_widget, *args, **kwargs):
        self.initial_widget = initial_widget
        super(ReadOnlyWidget, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):

        def guess_readonly_text(original_content):
            root = etree.fromstring("<span>%s</span>" % original_content)
            for element in root:
                if element.tag == 'input':
                    return element.get('value')
                if element.tag == 'select':
                    for option in element:
                        if option.get('selected'):
                            return option.text
                    else:
                        if len(element) == 1:
                            return element[0].text
                if element.tag == 'textarea':
                    return element.text
            return "N/A"

        original_content = self.initial_widget.render(*args, **kwargs)
        try:
            readonly_text = self.initial_widget.render_readonly(*args, **kwargs)
        except AttributeError:
            readonly_text = guess_readonly_text(original_content)

        return mark_safe("""<span class="hidden">%s</span><input type="text" value="%s" disabled="disabled">""" % (
            original_content, readonly_text))



'''
# Phone Number Prefix Widget

#from babel import Locale

from phonenumbers.data import _COUNTRY_CODE_TO_REGION_CODE

from django.utils import translation
from django.forms import Select, TextInput
from django.forms.widgets import MultiWidget


class PhonePrefixSelect(Select):

    initial = None

    def __init__(self, initial=None):
        choices = [('', '---------')]
        #locale = Locale(translation.get_language())
        for prefix, values in _COUNTRY_CODE_TO_REGION_CODE.iteritems():
            prefix = '+%d' % prefix
            if initial and initial in values:
                self.initial = prefix
            for country_code in values:
                #country_name = locale.territories.get(country_code)
                country_name = translation.get_language().upper()
                if country_name:
                    #choices.append((prefix, u'%s %s' % (country_name, prefix)))
                    choices.append((prefix, u'%s %s' % (country_code, prefix)))
        return super(PhonePrefixSelect, self).__init__(choices=sorted(choices, key=lambda item: item[1]))

    def render(self, name, value, *args, **kwargs):
        return super(PhonePrefixSelect, self).render(name, value or self.initial, *args, **kwargs)

class PhoneNumberPrefixWidget(MultiWidget):
    """
    A Widget that splits phone number input into:
    - a country select box for phone prefix
    - an input for local phone number
    """
    def __init__(self, attrs=None, initial=None):
        widgets = (PhonePrefixSelect(initial), TextInput(),)
        super(PhoneNumberPrefixWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            print value
            return str(value).split('.')
        return [None, None]

    def value_from_datadict(self, data, files, name):
        values = super(PhoneNumberPrefixWidget, self).value_from_datadict(data, files, name)
        return '%s.%s' % tuple(values)
'''