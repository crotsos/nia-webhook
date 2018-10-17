""" Response beautifier for Google Actions """

from copy import deepcopy

import config


def beautify(intent):
    """ Beautify Nile intent """
    beautified = deepcopy(intent)
    for oper in config.NILE_OPERATIONS:
        beautified = beautified.replace(oper + " ", "  \n&nbsp;&nbsp;&nbsp;&nbsp;**" + oper + "** ")
    return beautified
