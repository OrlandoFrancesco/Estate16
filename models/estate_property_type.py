from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description = "estate.property.type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_offer_type_id")
    offer_count = fields.Integer(compute="_number_of_offers")

    @api.constrains("name")
    def _check_name_is_already_used(self):
        for record in self:
            domain = [('name', '=', record.name)]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError(_("The name must be unique."))
            
    @api.depends("offer_ids")
    def _number_of_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)