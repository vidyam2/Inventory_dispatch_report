from odoo import models, fields, tools


class DispatchReport(models.Model):
    _name = 'dispatch.report'
    _description = 'Dispatch Report'
    _auto = False
    _order = 'schedule_date desc'

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_barcode = fields.Char(string='Product Barcode', readonly=True)
    internal_reference = fields.Char(string='Internal Reference', readonly=True)
    uom_id = fields.Many2one('uom.uom', string='UoM', readonly=True)
    total_demand = fields.Float(string='Total Demand', readonly=True)
    qty_delivered = fields.Float(string='Quantity Delivered', readonly=True)
    qty_to_deliver = fields.Float(string='Quantity to be Delivered', readonly=True)
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position', readonly=True)
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', readonly=True)
    schedule_date = fields.Datetime(string='Schedule Date', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    sm.id AS id,
                    sm.product_id AS product_id,
                    pp.barcode AS product_barcode,
                    pt.default_code AS internal_reference,
                    sm.product_uom AS uom_id,
                    sm.product_uom_qty AS total_demand,
                    sm.quantity AS qty_delivered,
                    (sm.product_uom_qty - sm.quantity) AS qty_to_deliver,
                    so.fiscal_position_id AS fiscal_position_id,
                    so.payment_term_id AS payment_term_id,
                    sm.date AS schedule_date
                FROM stock_move sm
                    INNER JOIN product_product pp ON pp.id = sm.product_id
                    INNER JOIN product_template pt ON pt.id = pp.product_tmpl_id
                    LEFT JOIN sale_order_line sol ON sol.id = sm.sale_line_id
                    LEFT JOIN sale_order so ON so.id = sol.order_id
                WHERE pt.is_storable = true
                    AND sm.state != 'cancel'
            )
        """ % self._table)