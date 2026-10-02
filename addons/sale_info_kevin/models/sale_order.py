from odoo import api, fields, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    priorite = fields.Selection(
        [('normale', 'Normale'), ('urgente', 'Urgente')], default='normale')
    nb_articles = fields.Float(
        string="Nombre d'articles", compute='_compute_nb_articles', store=True)

    @api.depends('order_line.product_uom_qty')
    def _compute_nb_articles(self):
        for order in self:
            order.nb_articles = sum(order.order_line.mapped('product_uom_qty'))

    @api.constrains('priorite', 'nb_articles')
    def _check_urgence(self):
        for order in self:
            if order.priorite == 'urgente' and order.nb_articles > 100:
                raise ValidationError("Une commande urgente ne peut pas dépasser 100 articles.")