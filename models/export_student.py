from odoo import models, fields, api
from datetime import date, datetime, timedelta
from odoo.tools.misc import xlwt
import io
import base64


class ExportStudent(models.Model):

    # Nom de la base de donnée à créer
    _name = 'export.student'

    # Fonction qui permet de récupérer les élèves actifs de la liste (cochés)
    def get_default_students(self):
        return self.env['ecole.partner.school'].browse(self.env.context.get('active_ids'))

    # Champs de relation avec la table ecole.partner.school afin de récupérer la liste des enfants
    # Défaut = par défaut, appel la fonction qui récupère les enfants actifs
    student_ids = fields.Many2many('ecole.partner.school', String="Students", default=get_default_students)
    # Création d'un champ binaire dans la base pour stocker le fichier généré
    excel_file = fields.Binary(string="excel file")
    # Création d'un champ de type char avec une tailel de 64 caractères pour le nom du fichier
    file_name = fields.Char(string="File name", size=64)

    # Même principe pour les autres champs
    # Informations détaillées sur l'enfant
    student_contact_information = fields.Boolean(string="Student contact information")

    # Inscription scolaire
    student_school_information = fields.Boolean(string="Student school information")
    student_school_information_details = fields.Boolean(string="Student school information details")
    responsible_school_contact_information = fields.Boolean(string="Responsible school contact information")

    # Inscription restauration scolaire
    student_school_catering_information = fields.Boolean(string="Student school catering contact information")
    student_school_catering_information_details = fields.Boolean(string="Student school catering contact information details")
    responsible_school_catering_contact_information = fields.Boolean(string="Responsible school catering contact information")

    # Inscription garderie
    student_nursery_information = fields.Boolean(string="Student nursery information")
    student_nursery_information_details = fields.Boolean(string="Student nursery information details")
    responsible_nursery_contact_information = fields.Boolean(string="Responsible nursery contact information")

    @api.model
    def get_active_records(self):
        # records = self.student_ids
        # active_ids = self.ids
        # active_ids_two = self.env.context.get('active_ids', [])
        # print(records)
        # print(active_ids)
        # print(active_ids_two)
        return [['ecole.partner.school'], [8569, 8567, 8574, 8523]]

    # Fonction qui permet d'exporter les données dans un fichier excel
    @api.multi
    def set_export_student(self):
        # Nom du fichier de sortie
        filename = str(self.file_name) + '.xls'

        # Style du tableau Excel
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Export élèves')
        font = xlwt.Font()
        font.bold = True
        for_left = xlwt.easyxf("font: bold 1, color black; borders: top double, bottom double, left double, right double; align: horiz left")
        for_left_not_bold = xlwt.easyxf("font: color black; align: horiz left")
        for_center_bold = xlwt.easyxf("font: bold 1, color black; align: horiz center")
        style = xlwt.easyxf('font:height 400, bold True, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')

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
        for student in self.student_ids.sorted(key=lambda x: x.partner_id.name):
            column = 0
            # Nom et prénom de ou des enfants selectionnés obligatoire à la génération du fichier
            if row == 0:
                worksheet.write(row, column, 'Enfant - Nom et prénom', for_left)
            worksheet.write(row+1, column, student.partner_id.name, for_left_not_bold)
            column += 1
            # Informations des élèves selectionnés
            if self.student_contact_information:
                school_birthdate = datetime.strptime(student.school_birthdate, "%Y-%m-%d").strftime("%d/%m/%Y")
                if row == 0:
                    column_libelle = column
                    libelles = ('Enfant - Adresse', 'Enfant - Ville', 'Enfant - Date de naissance',
                                'Enfant - Lieu de naissance')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (student.partner_id.street, student.partner_id.city_id.name,
                               school_birthdate, student.school_place_of_birth.name)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            # Informations sur les inscriptions scolaires des élèves selectionnés
            if self.student_school_information:
                school_registration = datetime.strptime(student.school_registration, "%Y-%m-%d").strftime("%d/%m/%Y")
                school_end_date = datetime.strptime(student.school_end_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                if row == 0:
                    column_libelle = column
                    libelles = ('École - Début', 'École - Fin', 'Établissement', 'Niveau', 'Onde',
                                'Resp. - Nom et prénom', 'Resp. - Tél. 1', 'Resp. - Tél. 2')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (school_registration, school_end_date, student.school_name_id.name,
                               student.school_level_id.name, student.school_send_onde,
                               student.school_responsible_partner.name, student.school_responsible_partner.phone,
                               student.school_responsible_partner.mobile)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            # Informations détaillées sur les inscriptions scolaires des élèves selectionnés
            if self.student_school_information_details:
                if row == 0:
                    column_libelle = column
                    libelles = ('École - Commentaire', 'École - Dérogation',
                                'Dérogation - Motif', 'Dérogation - Statut')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (student.school_text, student.school_derogation,
                               student.school_derogation_reason, student.school_derogation_state)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            # Informations sur le responsable - inscription scolaire
            if self.responsible_school_contact_information:
                if row == 0:
                    column_libelle = column
                    libelles = ('Resp. - Adresse', 'Resp. - Ville', 'Resp. - Email')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (student.school_responsible_partner.street,
                               student.school_responsible_partner.city_id.name,
                               student.school_responsible_partner.email)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            # Informations sur les inscriptions restauration scolaire des élèves selectionnés
            if self.student_school_catering_information:
                if student.half_pension:
                    half_pension_begin_date = datetime.strptime(student.half_pension_begin_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                    half_pension_end_date = datetime.strptime(student.half_pension_end_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                else:
                    half_pension_begin_date = ""
                    half_pension_end_date = ""
                if row == 0:
                    column_libelle = column
                    libelles = ('Rest. - Inscrit', 'Rest. - Lieu', 'Rest.- Début',
                                'Rest. - Fin', 'Spécifications',
                                'Resp. - Nom et prénom', 'Resp. - Tél. 1', 'Resp. - Tél. 2')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (student.half_pension, student.half_pension_id.name, half_pension_begin_date,
                               half_pension_end_date, student.half_pension_specification,
                               student.half_pension_responsible_partner.name,
                               student.half_pension_responsible_partner.phone,
                               student.half_pension_responsible_partner.mobile)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            # Informations détaillées sur les inscriptions restauration scolaires des élèves selectionnés
            if self.student_school_catering_information_details:
                if row == 0:
                    column_libelle = column
                    libelles = ('Lundi', 'Mardi', 'Jeudi', 'Vendredi', 'Occasionnelle', 'Rest. - Commentaires')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (student.half_pension_monday, student.half_pension_tuesday, student.half_pension_thursday,
                               student.half_pension_friday, student.half_pension_occasional, student.half_pension_text)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            # Informations sur le responsable - restauration scolaire
            if self.responsible_school_catering_contact_information:
                if row == 0:
                    column_libelle = column
                    libelles = ('Resp. Rest. - Adresse', 'Resp. Rest. - Ville', 'Resp. Rest. - Email')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (student.half_pension_responsible_partner.street,
                               student.half_pension_responsible_partner.city_id.name,
                               student.half_pension_responsible_partner.email)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            # Informations sur les inscriptions garderie des élèves selectionnés
            if self.student_nursery_information:
                if student.nursery_morning or student.nursery_evening:
                    nursery_begin_date = datetime.strptime(student.nursery_begin_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                    nursery_end_date = datetime.strptime(student.nursery_end_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                else:
                    nursery_begin_date = ""
                    nursery_end_date = ""
                if row == 0:
                    column_libelle = column
                    libelles = ('Gard. - Lieu', 'Gard. - Début', 'Gard. - Fin',
                                'Resp. - Nom et prénom', 'Resp. - Tél. 1', 'Resp. - Tél. 2')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (student.nursery_name_id.name, nursery_begin_date, nursery_end_date,
                               student.nursery_responsible_partner.name, student.nursery_responsible_partner.phone,
                               student.nursery_responsible_partner.mobile)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            # Informations détaillées sur les inscriptions garderie des élèves selectionnés
            if self.student_nursery_information_details:
                if row == 0:
                    column_libelle = column
                    worksheet.write(row, column_libelle, 'Gard. - Commentaires', for_left)
                    column_libelle += 1
                nursery_text = student.nursery_text
                if not nursery_text:
                    nursery_text = ""
                worksheet.write(row+1, column, nursery_text, for_left_not_bold)
                column += 1

            # Informations sur le responsable - garderie
            if self.responsible_nursery_contact_information:
                if row == 0:
                    column_libelle = column
                    libelles = ('Resp. Gard. - Adresse', 'Resp. Gard. - Ville', 'Resp. Gard. - Email')
                    for libelle in libelles:
                        worksheet.write(row, column_libelle, libelle, for_left)
                        column_libelle += 1
                values_list = (student.nursery_responsible_partner.street,
                               student.nursery_responsible_partner.city_id.name,
                               student.nursery_responsible_partner.email)
                for value_list in values_list:
                    if not value_list:
                        value_list = ""
                    worksheet.write(row+1, column, value_list, for_left_not_bold)
                    column += 1

            row += 1

        fp = io.BytesIO()
        # Sauvegarde des fichiers apres écriture (write)
        workbook.save(fp)
        # Stockage sous forme binaire du fichier dans la base Odoo (table export.student)
        export_student_id = self.env['export.student'].create({'excel_file': base64.encodestring(fp.getvalue()),
                                                               'file_name': filename})
        fp.close()


        # Retourne le même formulaire avec le fichier Excel récupéré
        return {
            'view_mode': 'form',
            'res_id': export_student_id.id,
            'res_model': 'export.student',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',
        }

