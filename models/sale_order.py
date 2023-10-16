from odoo import fields, models
import string
import random
from odoo import api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    responsible_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Ответственный за выдачу товара',
        # readonly=False,
        required=True,
    )

    test = fields.Char(
        string='Test',
        compute='_compute_test',
        readonly=False,
        precompute=True,
        store=True
    )

    test_checked = fields.Boolean(
        store=True,
        default=False
    )

    def _get_random_string(self) -> str:
        letters = string.ascii_lowercase
        result_str = ''.join([random.choice(letters) for i in range(10)])
        return result_str

    @api.depends('date_order', 'order_line')
    def _compute_test(self):
        for order in self:
            if not self.test_checked:
                order.test = self._get_random_string()
                self.test_checked = True
                return

            order.test = f'{order.amount_total} - {order.date_order}'

    @api.constrains('test')
    def _check_test_length(self):
        for order in self:
            if order.test and len(order.test) > 50:
                raise ValidationError("Длина текста должна быть меньше 50 символов!")