# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class MrpBom(models.Model):
    """MRP BOM OverHeads"""
    _inherit = 'mrp.bom'

    cost_visible = fields.Boolean('Employee Cost Visibility', default=False)
    overhead_line_ids = fields.One2many('mrp.bom.overhead', 'bom_id', 'Overhead Lines')
    total_cost_over_head_percent = fields.Float("Over Head '%' over Total Cost")
    operation_workcenter_ids = fields.One2many('mrp.operation.workcenter', 'bom_id',
                                               'Operation Workcenter')

class MrpBomLine(models.Model):
    """MRP BOM OverHeads Loss Percent"""
    _inherit = 'mrp.bom.line'

    loss_percent = fields.Float('Loss %', help="BOM Componenets Loss %")
    is_supplementary_product = fields.Boolean('Is Supplementary Product?', default=False)
