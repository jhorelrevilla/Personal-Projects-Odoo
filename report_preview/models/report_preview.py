import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ReportPreview(models.Model):
    _name="report.preview"
    _inherit = ['mail.thread']
    _description="Report preview"
    
    name=fields.Char(
        string="Name",
        required=True
    )
    report_content=fields.Text(
        string="Report Content",
        default=lambda self:self.get_default_template()
    )
    paperformat_id=fields.Many2one(
        'report.paperformat',
        string='Paperformat',
        default=lambda self:self.env.ref('report_preview.paperformat_report_preview').id
    )
    attachment_id = fields.Many2one('ir.attachment', string='attachment')
    
    
    @api.model
    def create(self, vals):
        res=super().create(vals)
        self.update_view()
        return res
    
    def update_view(self):
        arch_content=f"""<?xml version="1.0"?>
        <t t-name="report_preview.{self.id}">
            <t t-call="web.html_container">
                <t t-foreach="docs" t-as="o">
                    {self.report_content}
                </t>
            </t>
        </t>
        """
        self.env.ref('report_preview.template_report_preview').write(
            {
                'arch': arch_content
            }
        )
        
    
    def get_report(self):
        self.update_view()
        attach_list=self.env['ir.attachment'].search([('res_id','=',self.id)])
        for attach in attach_list:
            attach.unlink()
        
        
        
        pdf=self.env.ref('report_preview.action_report_report_preview')._render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        self.attachment_id=self.env['ir.attachment'].create({
            'name': f"{self.name}.pdf",
            'type': 'binary',
            'datas': b64_pdf,
            'store_fname': f"report_preview_{self.id}",
            'res_model': 'report.preview',
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        }).id
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    
    def get_default_template(self):
        return"""<!-- contenido del reporte   -->
<div class="header">
</div>
<div class="footer">
</div>
<t t-call="web.external_layout">
    <style>
    </style>
    <div class="page">
      
    </div>
</t>
        """