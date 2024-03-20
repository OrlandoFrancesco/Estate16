from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate.property.offer"
    _order = "price asc"

    price = fields.Float()
    status = fields.Selection([
        ("accepted","Accepted"),("refused","Refused")],
         copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_calculate_deadline", inverse="_calculate_validity")
    create_date = fields.Date(default=fields.Datetime.today())
    property_offer_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends("validity", "date_deadline")
    def _calculate_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _calculate_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days      

    def accept(self):
        for record in self:
            if record.price < ((record.property_id.expected_price * 90)/100):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
            
            domain = [('status', '=', 'accepted')]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError("Only one offer can be accepted for a given property!")
            else:
                record.status = "accepted"
                record.property_id.state = "offer_accepted"
                record.property_id.selling_price = self.price
                record.property_id.partner_id = self.partner_id

    def refuse(self):
        self.status = "refused"

    @api.constrains("price")
    def _check_price_positivity(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("The price must be strictly positive.")
            
    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        property.state = "offer_received"

        for record in property.offer_ids:
            if vals["price"] < record.price:
                raise UserError("You cannot create an offer with a lower amount than an existing offer.")                
        
        return super(EstatePropertyOffer, self).create(vals)