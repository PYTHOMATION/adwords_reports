MICRO_FACTOR = 10**6


def reg_and_micro(number):
    """ takes a bid amount and identifies if it's micro or regular format. Then returns both formats.
    CAUTION: There might be currencies where this doesn't make sense
    """
    is_micro = number >= 0.01 * MICRO_FACTOR  # >= 10k must be micro
    if is_micro:
        regular = micro_to_reg(number)
        micro = reg_to_micro(regular)  # for formatting
    else:
        micro = reg_to_micro(number)
        regular = micro_to_reg(micro)  # for formatting
    return regular, micro


def reg_to_micro(number):
    """ Convert a number to a micro amount:
        - times one million
        - and rounded to multiples of 10k """
    assert isinstance(number, (float, int))
    return int(round(float(number) * MICRO_FACTOR, -4))


def micro_to_reg(number):
    """ Convert micro amount to regular euro amount
        - divided by one million
        - and rounded to 2 fractional digits """
    assert isinstance(number, (float, int))
    return round(float(number) / MICRO_FACTOR, 2)
