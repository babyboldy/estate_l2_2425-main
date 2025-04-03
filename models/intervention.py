# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EstateIntervention(models.Model):
    _name = 'estate.intervention'
    _description = 'Intervention'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Référence", required=True, tracking=True)
    date = fields.Date(string="Date", default=fields.Date.today, tracking=True)
    description = fields.Text(string="Description")
    propriete_id = fields.Many2one('estate.propriete', string="Propriété", required=True, tracking=True)
    type = fields.Selection([
        ('reparation', 'Réparation'),
        ('entretien', 'Entretien')
    ], string="Type", required=True, tracking=True)
    etat = fields.Selection([
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée')
    ], string="État", default="planifiee", tracking=True)
