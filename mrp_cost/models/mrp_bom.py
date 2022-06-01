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


class MrpBomLine(models.Model):
    """MRP BOM OverHeads Loss Percent"""
    _inherit = 'mrp.bom.line'

    loss_percent = fields.Float('Loss %', help="BOM Componenets Loss %")
    is_supplementary_product = fields.Boolean('Is Supplementary Product?', default=False)
    quantity_ratio_percent = fields.Float("Quantity Ratio (%)")
    quantity_coefficient = fields.Integer("Quantity Coefficient")
    coefficent_parameters = fields.Selection([('percentage_with_co', '% with Co.'),
                                              ('only_co', 'Only Co.')], string="Coefficent", default=False)
    product_qty = fields.Float(compute='_compute_product_qty', store=True)

    @api.depends('coefficent_parameters', 'quantity_ratio_percent', 'quantity_coefficient', 'bom_id.weight')
    def _compute_product_qty(self):
        for line in self:
            if line.coefficent_parameters == 'percentage_with_co':
                line.product_qty = line.bom_id.weight * ((line.quantity_ratio_percent / 100) / (line.quantity_coefficient or 1))
            elif line.coefficent_parameters == 'only_co':
                line.product_qty = line.bom_id.product_qty / (line.quantity_coefficient or 1)
