from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Name',required=True)
    description = fields.Text(string='Description',compute="_compute_description" ,store=True)
    postal_code = fields.Char(string='Postal Code', nullable=True)
    date_availability = fields.Date(string="Date Availability", nullable=True)
    expected_price = fields.Float(string='Expected Price', nullable=True)
    selling_price = fields.Float(string='Selling Price', nullable=True)
    bedrooms = fields.Integer(string='Bedrooms', nullable=True)
    living_area = fields.Integer(string='Living Area', nullable=True)
    facades = fields.Integer(string='Facades', nullable=True)
    garage = fields.Boolean(string='Garage', nullable=True)
    garden = fields.Boolean(string='Garden', nullable=True)
    garden_area = fields.Integer(string='Garden Area', nullable=True)
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], string='Garden Orientation', nullable=True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # i want add seller and buyer
    seller_id = fields.Many2one("res.partner", string="Seller")
    buyer_id = fields.Many2one("res.partner", string="Buyer", compute="_compute_buyer_id", store=True)

    total_area = fields.Integer(string='Total Area', compute="_compute_total_area", store=True)
    best_price = fields.Float(string='Best Price', compute="_compute_best_price", store=True)
    best_price_id = fields.Many2one("estate.property.offer", string="Best Price Offer")

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='Status', default='new', required=True, copy=False)

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.status')
    def _compute_best_price(self):
        for record in self:
            best_price = 0.0
            best_offer = None
            for offer in record.offer_ids:
                if  offer.price > best_price:
                    best_price = offer.price
                    best_offer = offer
            record.best_price = best_price
            record.best_price_id = best_offer


    @api.depends('offer_ids.status')
    def _compute_buyer_id(self):
        for record in self:
           for offer in record.offer_ids:
                if offer.status == 'accepted':
                    record.buyer_id = offer.partner_id
                    record.selling_price = offer.price
                    record.state = 'offer_accepted'
                    break

        # all ofter canceled
        if not record.offer_ids.filtered(lambda x: x.status == 'accepted'):
            record.buyer_id = False
            record.selling_price = 0.0
            record.state = 'offer_received'


    # @api.depends('buyer_id.name')
    # def _compute_description(self):
    #     for record in self:
    #         if record.buyer_id:
    #             record.description = "Test for parner  %s" % record.buyer_id.name
    #         else:
    #             record.description = "No owner assigned"


    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None


    # ====== Action =========
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("You cannot change the state of a canceled property.")
            else:
                record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You cannot change the state of a sold property.")
            else :
                record.state = 'canceled'









