# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'    
    
    @api.one    
    def action_account_invoice_not_create_partner_without_vat(self):
        res = super(SaleOrder, self).action_account_invoice_not_create_partner_without_vat()
        
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                                                        
        attachments = [
            {                    
                "title": 'No se ha podido crear la factura del pedido '+str(self.name)+' porque no hay CIF definido para el cliente',
                "text": self.name,                        
                "color": "#ff0000",                                             
                "fallback": "Ver pedido de venta "+str(self.name)+' '+str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=sale.order",                                    
                "actions": [
                    {
                        "type": "button",
                        "text": "Ver pedido de venta "+str(self.name),
                        "url": str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=sale.order"
                    }
                ],
                "fields": [                    
                    {
                        "title": "Comercial",
                        "value": self.partner_invoice_id.name,
                        'short': True,
                    },
                    {
                        "title": "Direccion de facturacion",
                        "value": self.partner_invoice_id.name,
                        'short': True,
                    }
                ],                    
            }
        ]            
        
        slack_message_vals = {
            'attachments': attachments,
            'model': 'sale.order',
            'res_id': self.id,
            'channel': self.env['ir.config_parameter'].sudo().get_param('slack_arelux_log_contabilidad_channel'),                                                         
        }                        
        slack_message_obj = self.env['slack.message'].sudo().create(slack_message_vals)
        
        return res
    
    @api.one    
    def action_confirm_create_message_slack(self):        
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        options = {
            'display_currency': self.currency_id
        }
        amount_untaxed_monetary = self.env['ir.qweb.field.monetary'].value_to_html(self.amount_untaxed, options)        
        amount_untaxed_monetary = amount_untaxed_monetary.replace('<span class="oe_currency_value">', '')
        amount_untaxed_monetary = amount_untaxed_monetary.replace('</span>', '')                                                                
                                                                
        attachments = [
            {                    
                "title": 'Venta confirmada',
                "text": self.name,                        
                "color": "#36a64f",                                             
                "fallback": "Ver pedido de venta "+str(self.name)+' '+str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=sale.order",                                    
                "actions": [
                    {
                        "type": "button",
                        "text": "Ver pedido de venta "+str(self.name),
                        "url": str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=sale.order"
                    }
                ],
                "fields": [                    
                    {
                        "title": "Comercial",
                        "value": self.user_id.partner_id.name,
                        'short': True,
                    },
                    {
                        "title": "Cliente",
                        "value": self.partner_id.name,
                        'short': True,
                    },
                    {
                        "title": "Base imponible",
                        "value": amount_untaxed_monetary,
                        'short': True,
                    }
                ],                    
            }
        ]            
        
        slack_message_vals = {
            'attachments': attachments,
            'model': 'sale.order',
            'res_id': self.id,
            'channel': self.env['ir.config_parameter'].sudo().get_param('slack_arelux_channel_data'),                                                         
        }                        
        slack_message_obj = self.env['slack.message'].sudo().create(slack_message_vals)

    @api.one    
    def action_custom_send_sms_info_slack(self):
        res = super(SaleOrder, self).action_custom_send_sms_info_slack()
        
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        options = {
            'display_currency': self.currency_id
        }
        amount_untaxed_monetary = self.env['ir.qweb.field.monetary'].value_to_html(self.amount_untaxed, options)        
        amount_untaxed_monetary = amount_untaxed_monetary.replace('<span class="oe_currency_value">', '')
        amount_untaxed_monetary = amount_untaxed_monetary.replace('</span>', '')
        
        attachments = [
            {                    
                "title": 'Se ha enviado por SMS la info del presupuesto',
                "text": self.name,                        
                "color": "#36a64f",                                             
                "fallback": "Ver presupuesto "+str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=sale.order",                                    
                "actions": [
                    {
                        "type": "button",
                        "text": "Ver presupuesto",
                        "url": str(web_base_url)+"/web?#id="+str(self.id)+"&view_type=form&model=sale.order"
                    }
                ],
                "fields": [                    
                    {
                        "title": "Comercial",
                        "value": self.user_id.partner_id.name,
                        'short': True,
                    },
                    {
                        "title": "Cliente",
                        "value": self.partner_id.name,
                        'short': True,
                    },
                    {
                        "title": "Base imponible",
                        "value": amount_untaxed_monetary,
                        'short': True,
                    }
                ],                    
            }
        ]        
        
        slack_message_vals = {
            'attachments': attachments,
            'model': self._inherit,
            'res_id': self.id,
            'channel': self.env['ir.config_parameter'].sudo().get_param('slack_arelux_log_channel'),                                                         
        }                        
        slack_message_obj = self.env['slack.message'].sudo().create(slack_message_vals)
        
        return res
        
    @api.multi
    def action_confirm(self):
        return_action_confirm = super(SaleOrder, self).action_confirm()
        if return_action_confirm==True:
            if self.amount_total>0 and self.claim==False:
                self.action_confirm_create_message_slack()
            
        return return_action_confirm