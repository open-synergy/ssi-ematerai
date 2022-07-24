# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import tempfile
from datetime import datetime

import ghostscript

from odoo import api, fields, models


class CreateEmaterai(models.TransientModel):
    _name = "create.ematerai"
    _description = "Create E-Materai Document"

    @api.model
    def _compute_allowed_ematerai_type_ids(self):
        model_name = self.env.context.get("active_model", False)
        obj_ematerai_type = self.env["ematerai.type"]
        obj_model = self.env["ir.model"]

        model_id = False
        result = []

        if model_name:
            obj_model = self.env["ir.model"]
            criteria = [
                ("model", "=", model_name),
            ]
            models = obj_model.search(criteria)
            if len(models) > 0:
                model_id = models[0]
        if model_id:
            criteria = [("model_id", "=", model_id.id)]
            result = obj_ematerai_type.search(criteria).ids
        return result

    allowed_ematerai_type_ids = fields.Many2many(
        string="Allowed Ematerai Type",
        comodel_name="ematerai.type",
        default=lambda self: self._compute_allowed_ematerai_type_ids(),
        relation="rel_create_ematerai_2_type",
        column1="wizard_id",
        column2="ematerai_type_id",
    )
    ematerai_type_id = fields.Many2one(
        string="E-Materai Type",
        comodel_name="ematerai.type",
        required=True,
    )
    provider_id = fields.Many2one(
        string="Provider",
        comodel_name="ematerai.provider",
        required=True,
    )

    def action_create(self):
        for record in self:
            record._action_create()

    @api.multi
    def _prepare_ematerai_data(self):
        self.ensure_one()
        model_name = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", False)
        original_attachment_id = self._get_report_attachment()
        return {
            "model": model_name,
            "res_id": active_id,
            "type_id": self.ematerai_type_id.id,
            "value_id": self.ematerai_type_id.value_id.id,
            "provider_model_name": self.provider_id.model_name,
            "original_attachment_id": original_attachment_id.id,
        }

    @api.multi
    def _prepare_attachment_data(self, report_id):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", False)
        active_model = self.env.context.get("active_model", "")
        if report_id.report_type == "aeroo":
            pdf = report_id.render_aeroo(active_ids, {})
        else:
            pdf = report_id.render_qweb_pdf(active_ids)

        b64_pdf = base64.b64encode(pdf[0])  # Bytes
        input_pdf = tempfile.NamedTemporaryFile()
        output_pdf = tempfile.NamedTemporaryFile()

        try:
            input_pdf.write(base64.b64decode(b64_pdf))
            args = [
                "downgradePDF",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.6",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                "-sOutputFile=" + output_pdf.name,
                input_pdf.name,
            ]
            ghostscript.Ghostscript(*args)
            output_pdf.seek(0)
            b64_pdf_new = base64.b64encode(output_pdf.read())
        finally:
            input_pdf.close()
            output_pdf.close()

        datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "report_" + datetime_now
        return {
            "name": filename,
            "type": "binary",
            "datas": b64_pdf_new,
            "datas_fname": filename + ".pdf",
            "store_fname": filename,
            "res_model": active_model,
            "res_id": active_ids[0],
            "mimetype": "application/x-pdf",
        }

    @api.multi
    def _action_create(self):
        self.ensure_one()
        obj_ematerai_document = self.env[self.provider_id.model_name]
        data = self._prepare_ematerai_data()
        if data:
            document_id = obj_ematerai_document.create(data)
            document_id.write(
                {
                    "provider_res_id": document_id.id,
                }
            )

    @api.multi
    def _get_object(self):
        active_id = self.env.context.get("active_id", False)
        active_model = self.env.context.get("active_model", "")
        object = self.env[active_model].browse([active_id])[0]
        return object

    @api.multi
    def _get_report_attachment(self):
        self.ensure_one()
        obj_ir_attachment = self.env["ir.attachment"]
        report_id = self.ematerai_type_id.report_id

        result = obj_ir_attachment.create(self._prepare_attachment_data(report_id))
        return result
