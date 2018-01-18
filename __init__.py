# This file is part of the purchase_margin module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import purchase
from . import purchase_request


def register():
    Pool.register(
        purchase.PurchaseLine,
        module='purchase_margin', type_='model')
    Pool.register(
        purchase_request.CreatePurchase,
        module='purchase_margin', type_='wizard')
