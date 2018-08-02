from builtins import str
from builtins import range
from lilacs.util import NUM_STRING_EN, SHORT_SCALE_EN, LONG_SCALE_EN, FRACTION_STRING_EN


def nice_number(number, speech, denominators):
    """ English helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 and a half" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """

    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        # Give up, just represent as a 3 decimal number
        return str(round(number, 3))

    whole, num, den = result

    if not speech:
        if num == 0:
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    den_str = FRACTION_STRING_EN[den]
    if whole == 0:
        if num == 1:
            return_string = 'a {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} and a {}'.format(whole, den_str)
    else:
        return_string = '{} and {} {}'.format(whole, num, den_str)
    if num > 1:
        return_string += 's'
    return return_string


def pronounce_number(num, places=2, short_scale=True, scientific=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
    Returns:
        (str): The pronounced number
    """
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            return pronounce_number(float(n), places, short_scale, False) \
                   + " times ten to the power of " + \
                   pronounce_number(power, places, short_scale, False)
    if short_scale:
        number_names = NUM_STRING_EN.copy()
        number_names.update(SHORT_SCALE_EN)
    else:
        number_names = NUM_STRING_EN.copy()
        number_names.update(LONG_SCALE_EN)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [SHORT_SCALE_EN[n] for n in list(SHORT_SCALE_EN.keys())]
    else:
        hundreds = [LONG_SCALE_EN[n] for n in list(LONG_SCALE_EN.keys())]

    # deal with negatives
    result = ""
    if num < 0:
        result = "negative "
    num = abs(num)

    # check for a direct match
    if num in number_names:
        if num > 90:
            result += "one "
        result += number_names[num]
    else:
        def _sub_thousand(n):
            assert 0 <= n <= 999
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r) if r else "")
            else:
                q, r = divmod(n, 100)
                return digits[q] + " hundred" + (
                    " and " + _sub_thousand(r) if r else "")

        def _short_scale(n):
            n = int(n)
            assert 0 <= n
            return ", ".join(reversed(
                [_sub_thousand(z) + (
                    " " + hundreds[i] if i else "") if z else ""
                 for i, z in enumerate(_split_by_thousands(n))]))

        def _split_by_thousands(n):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, 1000)
                res.append(r)
            return res

        def _split_by_millions(n):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, 1000)
                res.append(r)
            return res

        def _long_scale(n):
            if n >= 10e153:
                return "infinity"
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by_millions(n)):
                if not z:
                    continue
                number = pronounce_number(z, places, True)
                if i % 2 != 0 and i > 1:
                    number += " " + "thousand"
                elif i > 0 and i < 3:
                    number += " " + hundreds[i] + ","
                elif i:
                    number += " " + hundreds[i - 1] + ","
                res.append(number)
            return " ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # Deal with fractional part
    if not num == int(num) and places > 0:
        result += " point"
        place = 10
        while int(num * place) % 10 > 0 and places > 0:
            result += " " + number_names[int(num * place) % 10]
            place *= 10
            places -= 1
    return result


def convert_to_mixed_fraction(number, denominators):
    """
    Convert floats to components of a mixed fraction representation

    Returns the closest fractional representation using the
    provided denominators.  For example, 4.500002 would become
    the whole number 4, the numerator 1 and the denominator 2

    Args:
        number (float): number for convert
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        whole, numerator, denominator (int): Integers of the mixed fraction
    """
    int_number = int(number)
    if int_number == number:
        return int_number, 0, 1  # whole number, no fraction

    frac_number = abs(number - int_number)
    if not denominators:
        denominators = list(range(1, 21))

    for denominator in denominators:
        numerator = abs(frac_number) * denominator
        if abs(numerator - round(numerator)) < 0.01:  # 0.01 accuracy
            break
    else:
        return None

    return int_number, int(round(numerator)), denominator
