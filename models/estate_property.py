from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate.property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Datetime.today() + relativedelta(months=3), 
        copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ("north", "North"), ("south", "South"),
        ("east", "East"), ("west", "West")])
    active = fields.Boolean(default=False)
    state = fields.Selection([
        ("new", "New"),("offer_received", "Offer Received"),
        ("offer_accepted","Offer Accepted"), 
        ("sold","Sold"), ("cancelled","Cancelled")])
    user_id = fields.Many2one('res.users', string='Salesperson',
                              default=lambda self: self.env.user,)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(default=0, compute="_compute_best_price")
    sequence = fields.Integer()
    
    @api.depends("garden_area","living_area")
    def _compute_total(self):
        self.total_area = self.garden_area + self.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            old_price = 0
            for r in record.offer_ids:
                actual_price = r.price
                if  actual_price > old_price:
                    old_price = actual_price
            record.best_price = old_price
    
    @api.onchange("garden")
    def _garden_change(self):
        for record in self:
            if record.garden == True:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = ""

    def button_cancel(self):
        self.state = "cancelled"

    def button_sold(self):
        if self.state == "cancelled":
            raise UserError("Cancelled properties cannot be sold.")
        else:
            self.state = "sold"       

    @api.constrains("expected_price")
    def _check_expected_price_positivity(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("The expected price must be strictly positive.")
            
    @api.constrains("selling_price")
    def _check_selling_price_positivity(self):
        for record in self:
            if record.selling_price <= 0:
                raise ValidationError("The selling price must be positive.")
            
    @api.ondelete(at_uninstall=False)
    def _property_delete(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError("You can delete a property with a 'new' or 'deleted' status")