# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date


class Location(models.Model):
    _name = 'estate.location'
    _description = 'Location'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("numéro")
    locataire_id = fields.Many2one('res.partner', "Locataire")
    propriete_id = fields.Many2one('estate.propriete', "Propriété")
    date_de_reservation = fields.Date('Date de réservation')
    date_de_debut = fields.Date('Date de début')
    duree_en_annee = fields.Integer("Durée", help="Durée de location en année")
    date_de_fin = fields.Date('Date de fin', compte="_compute_date_de_fin", store=True)
    frequence = fields.Selection([
        ('mensuelle', 'Mensuelle'),
        ('bimestrielle', 'Bimestrielle'),
        ('trimestrielle', 'Trimestrielle'),
        ('semestrielle', 'Semestrielle'),
        ('annuelle', 'Annuelle'),
        ],
        string="Fréquence de paiement",
        default='mensuelle')
    loyer = fields.Integer(compute="_compute_loyer", store=True)
    etat = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('validee', 'Validée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée')], string="Etat",
        default='brouillon')
    etats_des_lieux_ids = fields.One2many('estate.etat.des.lieux', 'location_id', string='Etats des Lieux')
    commune = fields.Char(related='propriete_id.localisation_id.commune', string="Commune", store=True)
    quartier = fields.Char(related='propriete_id.localisation_id.quartier', string="Quartier", store=True)
    ville = fields.Char(related='propriete_id.localisation_id.ville', string="Ville", store=True)
    pays = fields.Char(related='propriete_id.localisation_id.pays', string="Pays", store=True)

    @api.depends('date_de_debut', 'duree_en_annee')
    def _compute_date_de_fin(self):
        for record in self:
            if record.date_de_debut and record.duree_en_annee:
                record.date_de_fin = record.date_de_debut + relativedelta(years=record.duree_en_annee) - relativedelta(days=1)
            else:
                record.date_de_fin = date.today()

    @api.depends('propriete_id', 'frequence')
    def _compute_loyer(self):
        for record in self:
            if record.propriete_id:
                if record.frequence == "mensuelle":
                    record.loyer = record.propriete_id.loyer_mensuel
                elif record.frequence == "bimestrielle":
                    record.loyer = record.propriete_id.loyer_mensuel * 2
                elif record.frequence == "trimestrielle":
                    record.loyer = record.propriete_id.loyer_mensuel * 3
                elif record.frequence == "semestrielle":
                    record.loyer = record.propriete_id.loyer_mensuel * 6
                elif record.frequence == "annuelle":
                    record.loyer = record.propriete_id.loyer_mensuel * 12
                else:
                    record.loyer = 0
            else:
                record.loyer = 0