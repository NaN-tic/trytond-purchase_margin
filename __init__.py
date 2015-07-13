# This file is part of the purchase_margin module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .purchase import *

def register():
    Pool.register(
        PurchaseLine,
        module='purchase_margin', type_='model')
