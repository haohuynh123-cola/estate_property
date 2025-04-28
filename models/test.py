from odoo import models, fields, api

class TestModel(models.Model):
    _name = 'test.model'
    _description = 'Test Model'

    name = fields.Char(string="Name")
    description = fields.Text(string='Description',nullable=True)
    postal_code = fields.Char(string='Postal Code',nullable=True)
    date_availability = fields.Date(string='Date Availability',nullable=True)
    expected_price = fields.Float(string='Expected Price',nullable=True)
    selling_price = fields.Float(string='Selling Price',nullable=True)
    bedrooms = fields.Integer(string='Bedrooms',nullable=True)
    living_area = fields.Integer(string='Living Area',nullable=True)
    facades = fields.Integer(string='Facades',nullable=True)
    garage = fields.Boolean(string='Garage',nullable=True)
    garden = fields.Boolean(string='Garden',nullable=True)
    garden_area = fields.Integer(string='Garden Area',nullable=True)
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], string='Garden Orientation')

    def action_create(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Test Model',
            'res_model': 'test.model',
            'view_mode': 'form',
            'target': 'new',  # To open in a new form view
            'context': {'default_name': '', 'default_description': '', 'default_postal_code': '', 'default_date_availability': '', 'default_expected_price': 0.0},  # optional default values
        }
