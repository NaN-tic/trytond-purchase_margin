# This file is part of the purchase_margin module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from math import fabs
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.config import config as config_
DIGITS = int(config_.get('digits', 'unit_price_digits', 4))

__all__ = ['PurchaseLine']
__metaclass__ = PoolMeta


class PurchaseLine:
    __name__ = 'purchase.line'
    list_price = fields.Numeric('List Price', digits=(16, DIGITS),
        states={
            'invisible': Eval('type') != 'line',
            }, depends=['type'])
    margin = fields.Function(fields.Numeric('Margin',
            digits=(16, Eval('_parent_purchase', {}).get('currency_digits', 2)),
            states={
                'invisible': Eval('type') != 'line',
                'readonly': ~Eval('_parent_purchase'),
                },
            depends=['type', 'amount']),
        'on_change_with_margin')
    margin_percent = fields.Function(fields.Numeric('Margin (%)',
            digits=(16, 4), states={
                'invisible': Eval('type') != 'line',
                }, depends=['type']),
        'on_change_with_margin_percent')

    @staticmethod
    def default_list_price():
        return Decimal(0)

    def get_list_price(self):
        return Decimal(str(fabs(self.quantity))) * (self.list_price or
                Decimal(0))

    def on_change_product(self):
        Product = Pool().get('product.product')

        res = super(PurchaseLine, self).on_change_product()

        list_price = Decimal(0)
        if self.product:
            list_price = Product.get_sale_price([self.product],
                    self.quantity or 0)[self.product.id]
        res['list_price'] = list_price
        return res

    @fields.depends('type', 'product', 'quantity', 'list_price',
        '_parent_purchase.currency', '_parent_purchase.lines', methods=['amount'])
    def on_change_with_margin(self, name=None):
        '''
        Return the margin of each purchase lines
        '''
        Currency = Pool().get('currency.currency')

        if self.type != 'line':
            return

        if not self.purchase or not self.purchase.currency or not self.list_price \
                or not self.quantity or (self.list_price <= Decimal(0)):
            return

        currency = self.purchase.currency

        if self.quantity:
            sale_price = Decimal(str(self.quantity)) * (self.list_price)
        else:
            sale_price = Decimal(0)
        self.amount = self.on_change_with_amount()
        return Currency.round(currency, sale_price - self.amount)

    @fields.depends('type', 'product', 'quantity', 'list_price',
        '_parent_purchase.currency', '_parent_purchase.lines', methods=['margin'])
    def on_change_with_margin_percent(self, name=None):
        if self.type != 'line':
            return

        self.margin = self.on_change_with_margin()
        if not self.margin:
            return

        if not self.quantity:
            return
        if not self.list_price:
            return Decimal('1.0')
        cost = self.get_list_price()
        return (self.margin / cost).quantize(Decimal('0.0001'))
