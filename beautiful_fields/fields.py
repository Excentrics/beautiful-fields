# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core import validators
from django.utils import formats
from django.core.exceptions import ValidationError

from beautiful_fields.widgets import RangeWidget
from beautiful_fields.validators import validate_international_phonenumber
from phonenumbers.phonenumberutil import NumberParseException
from beautiful_fields.phonenumber import to_python as phonenumber_to_python


'''
#---------------------------------
import logging
from django.conf import settings
logger = logging.getLogger(settings.PROJECT_NAME)
#---------------------------------
'''

#==============================================================================
# RangeMixin
#==============================================================================
class RangeMixin(object):

    def __init__(self, *args, **kwargs):
        self.min_value = kwargs.pop('min_value', None)
        self.max_value = kwargs.pop('max_value', None)
        super(RangeMixin, self).__init__(*args, **kwargs)


#==============================================================================
# RangeField
#==============================================================================
class RangeField(forms.Field):
    widget = RangeWidget
    default_error_messages = {
        'invalid_start': _(u'Enter a valid start value.'),
        'invalid_end': _(u'Enter a valid end value.'),
        'invalid_range': _(u'Ensure that start value of range is less than or equal end value.'),
        'max_range_value': _(u'Ensure that end value of range is less than or equal to %(limit_value)s.'),
        'min_range_value': _(u'Ensure that start value of range is greater than or equal to %(limit_value)s.'),
    }

    def __init__(self, max_value=None, min_value=None, *args, **kwargs):
        if not 'initial' in kwargs:
            kwargs['initial'] = [None, None]
        super(RangeField, self).__init__(*args, **kwargs)
        self.min_value, self.max_value = min_value, max_value

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        self._max_value = value
        self.widget.max_value = value

    @property
    def min_value(self):
        return self._min_value

    @min_value.setter
    def min_value(self, value):
        self._min_value = value
        self.widget.min_value = value

    def bound_data(self, data, initial):
        if isinstance(initial, RangeMixin):
            self.min_value = initial.min_value
            self.max_value = initial.max_value
        return data

    def prepare_value(self, value):
        if isinstance(value, RangeMixin):
            self.min_value = value.min_value
            self.max_value = value.max_value
        return value

    def to_python(self, value):
        """
        Returns the result range of float. Returns None for empty values.
        """
        value = super(RangeField, self).to_python(value)
        for x in value:
            if not x in validators.EMPTY_VALUES:
                break
        else:
            return None
        n = len(value)
        if self.localize:
            for i in range(n):
                value[i] = formats.sanitize_separators(value[i])
        error_messages = (self.error_messages['invalid_start'], self.error_messages['invalid_end'])
        for i in range(n):
            try:
                value[i] = float(value[i])
            except (ValueError, TypeError):
                raise ValidationError(error_messages[i])

        if value[0] > value[1]:
            raise ValidationError(self.error_messages['invalid_range'])
        if not self.min_value is None and self.min_value > value[0]:
            raise ValidationError(self.error_messages['min_range_value'] % {'limit_value': self.min_value})
        if not self.max_value is None and self.max_value < value[1]:
            raise ValidationError(self.error_messages['max_range_value'] % {'limit_value': self.max_value})

        #logger.debug("\n\n\n\n\n to_python: %s \n\n\n\n\n" % value)

        return value


class PhoneNumberField(forms.CharField):

    default_error_messages = {
        'invalid': _(u'Enter a valid phone number.'),
    }
    default_validators = [validate_international_phonenumber]

    def to_python(self, value):
        phone_number = phonenumber_to_python(value)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages['invalid'])
        return phone_number
