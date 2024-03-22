from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate.property.tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    @api.constrains("name")
    def _check_name_is_already_used(self):
        for record in self:
            domain = [('name', '=', record.name)]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError(_("The name must be unique."))