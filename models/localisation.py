from odoo import models, fields


class Localisation(models.Model):
    _name = 'estate.localisation'
    _description = 'Localisation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    pays = fields.Char("Pays", required=True, tracking=True)
    propriete_id = fields.Many2one('estate.propriete', "Propriété")
    ville = fields.Char("Ville", required=True, tracking=True)
    commune = fields.Char("Commune", tracking=True)
    quartier = fields.Char("Quartier", tracking=True)