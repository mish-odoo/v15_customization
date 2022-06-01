# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class MrpBom(models.Model):
    """MRP BOM OverHeads"""
    _inherit = 'mrp.bom'

    cost_visible = fields.Boolean('Employee Cost Visibility', default=False)
    overhead_line_ids = fields.One2many('mrp.bom.overhead', 'bom_id', 'Overhead Lines')
    total_cost_over_head_percent = fields.Float("Over Head '%' over Total Cost")
    operation_workcenter_ids = fields.One2many('mrp.operation.workcenter', 'bom_id',
                                               'Operation Workcenter')
    weight = fields.Float(related='product_tmpl_id.weight', string='Weight', digits='Stock Weight')

    @api.model
    def create(self, values):
        result = super(MrpBom, self).create(values)
        [line.call_onchange() for line in result.bom_line_ids]
        return result

    def write(self, values):
        res = super(MrpBom, self).write(values)
        [line.call_onchange() for line in self.bom_line_ids]
        return res


class MrpBomLine(models.Model):
    """MRP BOM OverHeads Loss Percent"""
    _inherit = 'mrp.bom.line'

    loss_percent = fields.Float('Loss %', help="BOM Componenets Loss %")
    is_supplementary_product = fields.Boolean('Is Supplementary Product?', default=False)
    quantity_ratio_percent = fields.Float("Quantity Ratio (%)")
    quantity_coefficient = fields.Integer("Quantity Coefficient")
    coefficent_parameters = fields.Selection([('percentage_with_co', '% with Co.'),
                                              ('only_co', 'Only Co.')], string="Coefficent", default=False)

    @api.onchange('coefficent_parameters', 'quantity_ratio_percent', 'quantity_coefficient')
    def _onchange_coefficent_parameters(self):
        for line in self:
            if not line.coefficent_parameters:
                continue
            self.call_onchange()

    def call_onchange(self):
        if self.coefficent_parameters == 'percentage_with_co':
            self.product_qty = self.bom_id.weight * ((self.quantity_ratio_percent / 100) / self.quantity_coefficient if self.quantity_coefficient else 1)
        elif self.coefficent_parameters == 'only_co':
            self.product_qty = self.bom_id.product_qty / self.quantity_coefficient if self.quantity_coefficient else 1

