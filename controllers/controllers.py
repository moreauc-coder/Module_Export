from odoo import http, fields, api
from odoo.http import request
from odoo.tools.misc import xlwt
import io
import base64
import werkzeug

import logging
_logger = logging.getLogger(__name__)


class ExportList(http.Controller):

    @http.route('/export_fichier/', auth='user', website=True, type='http',csrf=True, method=['POST'])
    def indexExport(self, **post):

        # retourne des choses au template export est un id
        fields_model = http.request.env['ir.model.fields'].search([('model', '=', 'ecole.partner.school')])  # A rendre dynamique

        return http.request.render('export_view_parthenay.export', {
            'fields_model': fields_model,
        })

    @http.route('/tableau_export_fichier/<fields_checked>', auth='user', website=True, type='http', csrf=False, method=['POST'])
    def tableauExport(self, fields_checked, **post):

        return http.request.render('export_view_parthenay.modal', {
            'fields_checked': fields_checked.split(","),
        })

    @http.route('/telechargement_fichier/', auth='user', website=True, type='http', method=['POST'])
    def download_file(self, **post):
        if request.httprequest.method == 'POST':
            if post.get('input_download_file', False):
                if post.get('fields_checked', False):

                    fields_checked = post.get('fields_checked', False)
                    fields_checked = fields_checked.replace('[', '')
                    fields_checked = fields_checked.replace(']', '')
                    fields_checked = fields_checked.replace("'", '')
                    fields_checked = fields_checked.replace('"', '')
                    # fields_checked = fields_checked.replace(' ', '')
                    fields_checked = fields_checked.split(", ")

                    # Nom du fichier de sortie
                    name_file = post.get('name_file', False)
                    filename = str(name_file)+'.xls'

                    # Style du tableau Excel
                    workbook = xlwt.Workbook()
                    worksheet = workbook.add_sheet('Export élèves')
                    font = xlwt.Font()
                    font.bold = True
                    for_left = xlwt.easyxf(
                        "font: bold 1, color black; borders: top double, bottom double, left double, right double; align: horiz left")
                    for_left_not_bold = xlwt.easyxf("font: color black; align: horiz left")
                    for_center_bold = xlwt.easyxf("font: bold 1, color black; align: horiz center")
                    style = xlwt.easyxf(
                        'font:height 400, bold True, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')

                    alignment = xlwt.Alignment()  # Create Alignment
                    alignment.horz = xlwt.Alignment.HORZ_RIGHT
                    style = xlwt.easyxf('align: wrap yes')
                    style.num_format_str = '0.00'

                    worksheet.row(0).height = 500
                    worksheet.col(0).width = 4000
                    worksheet.col(1).width = 4000
                    borders = xlwt.Borders()
                    borders.bottom = xlwt.Borders.MEDIUM
                    border_style = xlwt.XFStyle()  # Create Style
                    border_style.borders = borders

                    # Traitement des données pour export
                    row = 0
                    column = 0
                    if row == 0:
                        for field_checked in fields_checked:
                            worksheet.write(row, column, field_checked, for_left)
                            column += 1

                    fp = io.BytesIO()
                    # Sauvegarde des fichiers apres écriture (write)
                    workbook.save(fp)
                    # Stockage sous forme binaire du fichier dans la base Odoo (table export.student)
                    export_id = http.request.env['export.student'].create({'excel_file': base64.encodestring(fp.getvalue()),
                                                                           'file_name': filename})
                    fp.close()

                    url_file = '/web/binary/download_document_partner?model=export.student&field=excel_file&id=' + str(
                        export_id.id) + '&filename=' + filename

                    return werkzeug.utils.redirect(url_file)








