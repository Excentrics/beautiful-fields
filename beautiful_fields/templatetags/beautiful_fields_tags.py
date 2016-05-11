from django import template

register = template.Library()

@register.filter
def fast_floatformat(number, places=-1, use_thousand_separator=False):
    """simple_floatformat(number:object, places:int) -> str
    
    Like django.template.defaultfilters.floatformat but not locale aware
    and between 40 and 200 times faster
    """
    try:
        number = float(number)
    except (ValueError, TypeError):
        return number #return ''
    
    # floatformat makes -0.0 == 0.0
    if number == 0:
        number = 0
    
    neg_places = False
    if places < 0:
        places = abs(places)
        neg_places = True
    
    if places == 0:
        # %.0f will truncate rather than round
        number = round(number, places)
    
    # .format is noticably slower than %-formatting, use it only if necessary
    if use_thousand_separator:
        format_str = "{:,.%sf}" % places
        formatted_number = format_str.format(number)
    else:
        format_str = "%%.%sf" % places
        formatted_number = format_str % number
    
    # -places means formatting to places, unless they're all 0 after places
    if neg_places:
        str_number = str(number)
        if not "." in str_number:
            return str_number
        if len(str_number) > len(formatted_number):
            return formatted_number
        int_part, _, _ = formatted_number.partition(".")
        if str_number.rstrip("0")[-1] == ".":
            return int_part
    
    return formatted_number

'''

# TEST AND VALIDATION
from django.template.defaultfilters import floatformat, special_floats
from decimal import Decimal as Decimal


vals = [
    None,
    '',
    1,
    1.9,
    2.0,
    0.1385798798,
    0.2,
    -0.5,
    -0.0,
    -5.0038,
    18343.3582828389,
    Decimal("-0.0"),
    Decimal("5.000083387"),
    Decimal("0E-7"),
    Decimal("780000.388"),
    "-0.5",
    "3.80",
    "foo",
]
vals.extend(special_floats)


def test_floatformat():
    for val in vals:
        yield check_equal, val, floatformat(val), fast_floatformat(val)
        yield check_equal, val, floatformat(val, 7), fast_floatformat(val, 7)
        yield check_equal, val, floatformat(val, -7), fast_floatformat(val, -7)
        yield check_equal, val, floatformat(val, 0), fast_floatformat(val, 0)


def check_equal(orig, a, b):
    assert a == b, '(%s) %s not equal with %s' % (orig, a, b)

'''