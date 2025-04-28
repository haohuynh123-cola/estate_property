from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute="_compute_date_deadline", store=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')


    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = fields.Date.context_today(self) + timedelta(days=record.validity)
            else:
                record.date_deadline = False


    # ==================== Action ====================
    def action_accept(self):
        for record in self:
            if record.status == 'refused':
                raise ValueError("You cannot change the state of a refused offer.")
            else:
                record.status = 'accepted'

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise ValueError("You cannot change the state of an accepted offer.")
            else:
                record.status = 'refused'






