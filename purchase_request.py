# This file is part of the purchase_margin module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['CreatePurchase']


class CreatePurchase:
    __metaclass__ = PoolMeta
    __name__ = 'purchase.request.create_purchase'

    @classmethod
    def compute_purchase_line(cls, request, purchase):
        Product = Pool().get('product.product')

        with Transaction().set_context(uom=request.uom.id,
                customer=request.party.id,
                currency=request.currency.id):
            prices = Product.get_sale_price(
                [request.product], request.quantity or 0)

        line = super(CreatePurchase, cls).compute_purchase_line(
            request, purchase)
        line.list_price = prices[request.product.id]
        return line
