# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_overhead = fields.Boolean('Is Overhead?')

    def button_bom_weight(self):
        return self.mapped('product_variant_id').button_bom_weight()
