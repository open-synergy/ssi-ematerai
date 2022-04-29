# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

import base64
import hashlib
import os
import re
import tempfile
from datetime import datetime

import pytz
import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class EmateraiRedphoenix(models.Model):
    _name = "ematerai.redphoenix"
    _inherits = {"ematerai.document": "ematerai_document_id"}
    _description = "E-Materai Document for Redphoenix"

    ematerai_document_id = fields.Many2one(
        string="E-Materai Document",
        comodel_name="ematerai.document",
        required=True,
        ondelete="cascade",
    )
    redphoenix_document_id = fields.Char(
        string="Document ID",
    )

    @api.multi
    def _generate_stamping_order(self, url):
        self.ensure_one()
        return re.sub(r"{stamping_order_id}", self.stamping_order, url)

    @api.multi
    def _get_redphoenix_credentials(self):
        self.ensure_one()
        static_jwt_token = False
        rp_add_document = False
        rp_create_order = False
        rp_update_param = False
        rp_submit_document = False
        rp_generate_sn = False
        rp_complete_terra = False
        rp_download_doc = False

        self._check_expiry_token()
        static_jwt_token = self._get_static_jwt_token()
        rp_add_document = self._get_add_doc_api()
        rp_create_order = self._get_create_order_api()
        if self.stamping_order:
            rp_update_param = self._get_update_param_api()
            rp_submit_document = self._get_submit_doc_api()
            rp_generate_sn = self._get_generate_sn_api()
            rp_complete_terra = self._get_complete_terra_api()
            rp_download_doc = self._get_download_doc_api()

        return {
            "static_jwt_token": static_jwt_token,
            "rp_add_document": rp_add_document,
            "rp_create_order": rp_create_order,
            "rp_update_param": rp_update_param,
            "rp_submit_document": rp_submit_document,
            "rp_generate_sn": rp_generate_sn,
            "rp_complete_terra": rp_complete_terra,
            "rp_download_doc": rp_download_doc,
        }

    @api.multi
    def _get_credentials_param(self, param):
        self.ensure_one()
        obj_ir_config_parameter = self.env["ir.config_parameter"].sudo()
        result = obj_ir_config_parameter.get_param(
            param,
            default=False,
        )
        return result

    @api.multi
    def _get_client_id(self):
        self.ensure_one()
        client_id = self._get_credentials_param("redphoenix.client_id")
        if not client_id:
            msg_err = _("Client ID Not Found")
            raise UserError(msg_err)
        return client_id

    @api.multi
    def _get_client_secret(self):
        self.ensure_one()
        client_secret = self._get_credentials_param("redphoenix.client_secret")
        if not client_secret:
            msg_err = _("Client Secret Not Found")
            raise UserError(msg_err)
        return client_secret

    @api.multi
    def _check_expiry_token(self):
        self.ensure_one()
        access_token_expiry = self._get_credentials_param(
            "redphoenix.access_token_expiry"
        )
        now = datetime.now()
        str_now = now.strftime("%Y-%m-%d %H:%M:%S")
        if str_now >= access_token_expiry:
            self._login()

    @api.multi
    def _get_static_jwt_token(self):
        self.ensure_one()
        static_jwt_token = self._get_credentials_param("redphoenix.static_jwt_token")
        if not static_jwt_token:
            msg_err = _("Token Not Found")
            raise UserError(msg_err)
        return static_jwt_token

    @api.multi
    def _get_api_login(self):
        self.ensure_one()
        rp_login = self._get_credentials_param("redphoenix.rp_login")
        if not rp_login:
            msg_err = _("Login API Not Found")
            raise UserError(msg_err)
        return rp_login

    @api.multi
    def _get_add_doc_api(self):
        self.ensure_one()
        rp_add_document = self._get_credentials_param("redphoenix.rp_add_document")
        if not rp_add_document:
            msg_err = _("Add Doc. API Not Found")
            raise UserError(msg_err)
        return rp_add_document

    @api.multi
    def _get_create_order_api(self):
        self.ensure_one()
        rp_create_order = self._get_credentials_param("redphoenix.rp_create_order")
        if not rp_create_order:
            msg_err = _("Create Order API Not Found")
            raise UserError(msg_err)
        return rp_create_order

    @api.multi
    def _get_update_param_api(self):
        self.ensure_one()
        rp_update_param = self._get_credentials_param("redphoenix.rp_update_param")
        if not rp_update_param:
            msg_err = _("Update Param API Not Found")
            raise UserError(msg_err)
        else:
            rp_update_param = self._generate_stamping_order(rp_update_param)
        return rp_update_param

    @api.multi
    def _get_submit_doc_api(self):
        self.ensure_one()
        rp_submit_document = self._get_credentials_param(
            "redphoenix.rp_submit_document"
        )
        if not rp_submit_document:
            msg_err = _("Submit Document API Not Found")
            raise UserError(msg_err)
        else:
            rp_submit_document = self._generate_stamping_order(rp_submit_document)
        return rp_submit_document

    @api.multi
    def _get_generate_sn_api(self):
        self.ensure_one()
        rp_generate_sn = self._get_credentials_param("redphoenix.rp_generate_sn")
        if not rp_generate_sn:
            msg_err = _("Generate SN. API Not Found")
            raise UserError(msg_err)
        else:
            rp_generate_sn = self._generate_stamping_order(rp_generate_sn)
        return rp_generate_sn

    @api.multi
    def _get_download_doc_api(self):
        self.ensure_one()
        rp_download_doc = self._get_credentials_param("redphoenix.rp_download_doc")
        if not rp_download_doc:
            msg_err = _("Download Doc. API Not Found")
            raise UserError(msg_err)
        else:
            rp_download_doc = self._generate_stamping_order(rp_download_doc)
        return rp_download_doc

    @api.multi
    def _get_complete_terra_api(self):
        self.ensure_one()
        rp_complete_terra = self._get_credentials_param("redphoenix.rp_complete_terra")
        if not rp_complete_terra:
            msg_err = _("Complete Terra API Not Found")
            raise UserError(msg_err)
        else:
            rp_complete_terra = self._generate_stamping_order(rp_complete_terra)
        return rp_complete_terra

    @api.multi
    def _prepare_access_token(self, data):
        self.ensure_one()
        access_token = data["access_token"]
        access_token_expiry = data["access_token_expiry"]
        obj_ir_config_parameter = self.env["ir.config_parameter"].sudo()
        obj_ir_config_parameter.set_param("redphoenix.static_jwt_token", access_token)
        tz_found = access_token_expiry.find(".")
        dt_token_expiry = access_token_expiry[:tz_found].replace("T", " ")
        obj_ir_config_parameter.set_param(
            "redphoenix.access_token_expiry", dt_token_expiry
        )

    @api.multi
    def _prepare_param_data(self):
        param = self._prepare_extra_param_data()
        if "document_date" in param:
            conv_dt = datetime.strptime(param["document_date"], "%Y-%m-%d")
            param["document_date"] = conv_dt.strftime("%Y/%m/%d")
        user = self.env.user
        location = "Asia/Jakarta"
        if user.tz:
            location = user.tz
        val = {
            "certificate_level": self.type_id.certificate_level,
            "document_type": self.type_id.api_name,
            "document_value": self.type_id.value_id.ematerai_value,
            "visual_sign_page": self.type_id.visual_sign_page,
            "location": location,
            "visual_llx": self.type_id.visual_iix,
            "visual_lly": self.type_id.visual_iiy,
            "visual_urx": self.type_id.visual_urx,
            "visual_ury": self.type_id.visual_ury,
        }
        param.update(val)
        return param

    @api.multi
    def check_redphoenix_meta(self, data, str):
        result = False
        err = str
        data_json = data.json()
        if data_json:
            if "meta" in data_json:
                meta = data_json["meta"]
                if meta.get("success"):
                    result = True
                if "error" in data_json["meta"]:
                    err += ": " + data_json["meta"]["error"]
            if "error" in data_json:
                err += ": " + data_json["error"]
        return result, err

    @api.multi
    def get_redphoenix_data(self, data):
        result = {}
        data_json = data.json()
        if "data" in data_json:
            result = data_json["data"]
        return result

    @api.multi
    def _get_timestamp(self):
        user = self.env.user
        if user.tz:
            local_tz = pytz.timezone(user.tz)
        else:
            local_tz = pytz.utc
        now = datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
        conv_dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        conv_dt = conv_dt.replace(tzinfo=pytz.utc)
        timestamp = conv_dt.astimezone(local_tz)
        return timestamp.isoformat("T")

    @api.multi
    def bytes_utf_8(self, data_str):
        return data_str.encode("utf-8")

    @api.multi
    def sha_512(self, data_bytes):
        hasher = hashlib.sha512()
        hasher.update(data_bytes)
        return hasher

    @api.multi
    def _get_secret_hash(self, client_id, client_secret, timestamp):
        id_secret = client_id + client_secret
        b_id_secret = self.bytes_utf_8(id_secret)
        s_id_secret = self.sha_512(b_id_secret).digest()
        b_timestamp = self.bytes_utf_8(timestamp)
        secret = s_id_secret + b_timestamp
        secret_hash = self.sha_512(secret).hexdigest()
        return secret_hash

    @api.multi
    def _login(self):
        self.ensure_one()
        client_id = self._get_client_id()
        client_secret = self._get_client_secret()
        timestamp = self._get_timestamp()
        secret_hash = self._get_secret_hash(client_id, client_secret, timestamp)
        rp_login = self._get_api_login()

        headers = {
            "Content-Type": "application/json",
        }

        json_data = {
            "grant_type": "client_id",
            "client_id": client_id,
            "timestamp": timestamp,
            "secret_hash": secret_hash,
        }
        try:
            response = requests.post(rp_login, headers=headers, json=json_data)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            raise UserError(msg_err)

        check, err_resp = self.check_redphoenix_meta(response, "login")
        if check:
            data = self.get_redphoenix_data(response)
            if "access_token" in data:
                self._prepare_access_token(data)
        else:
            msg_err = _(err_resp)
            raise UserError(msg_err)

    def _get_localdict(self):
        self.ensure_one()
        criteria = [("id", "=", self.res_id)]
        document = self.env[self.model].search(criteria)
        return {
            "env": self.env,
            "document": document,
        }

    def _evaluate_param_use_python(self, param):
        self.ensure_one()
        res = False
        if param:
            localdict = self._get_localdict()
            try:
                safe_eval(param.python_code, localdict, mode="exec", nocopy=True)
                res = localdict["result"]
            except Exception as error:
                raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    @api.multi
    def _prepare_add_document_data(self):
        return {
            "state": "added",
        }

    @api.multi
    def _prepare_update_param_data(self):
        return {
            "state": "updated",
        }

    @api.multi
    def _prepare_create_order_data(self):
        return {
            "state": "preparing",
        }

    @api.multi
    def _prepare_submit_document_data(self):
        return {
            "state": "submitted",
        }

    @api.multi
    def _prepare_generate_sn_data(self):
        return {
            "state": "sn_generated",
        }

    @api.multi
    def _prepare_complete_tera_data(self):
        return {
            "state": "terra_completed",
        }

    @api.multi
    def _prepare_download_document_data(self, data):
        self.ensure_one()
        attachment_id = self._get_document(data)
        return {"ematerai_attachment_id": attachment_id, "state": "success"}

    @api.multi
    def _get_document(self, data):
        self.ensure_one()
        obj_ir_attachment = self.env["ir.attachment"]
        b64_pdf = base64.b64encode(data)
        datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "ematerai_" + datetime_now
        ir_values = {
            "name": filename,
            "type": "binary",
            "datas": b64_pdf,
            "datas_fname": filename + ".pdf",
            "store_fname": filename,
            "res_model": self._name,
            "res_id": self.id,
            "mimetype": "application/x-pdf",
        }
        attachment_id = obj_ir_attachment.create(ir_values)
        return attachment_id.id

    @api.multi
    def _prepare_extra_param_data(self):
        val = {}
        if self.type_id.param_id:
            for param_detail in self.type_id.param_id.ematerai_param_ids:
                val[param_detail.name] = self._evaluate_param_use_python(param_detail)
        return val

    @api.multi
    def _add_document(self):
        self.ensure_one()
        if not self.redphoenix_document_id:
            credentials = self._get_redphoenix_credentials()
            headers = {"Authorization": "Bearer " + credentials["static_jwt_token"]}

            data = base64.decodestring(self.original_attachment_data)

            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()

            files = {
                "description": (None, "Document Letter PageSize"),
                "file": open(fname, "rb"),
            }
            try:
                response = requests.post(
                    credentials["rp_add_document"], headers=headers, files=files
                )
            except requests.exceptions.Timeout:
                msg_err = _("Timeout: the server did not reply within 30s")
                raise UserError(msg_err)
            finally:
                os.unlink(fname)
            check, err_resp = self.check_redphoenix_meta(response, "Add Document")
            if check:
                data = self.get_redphoenix_data(response)
                if "document_id" in data:
                    self.redphoenix_document_id = data["document_id"]
                    self.write(self._prepare_add_document_data())
            else:
                msg_err = _(err_resp)
                raise UserError(msg_err)
            self.env.cr.commit()

    @api.multi
    def _create_order(self):
        self.ensure_one()
        credentials = self._get_redphoenix_credentials()
        headers = {"Authorization": "Bearer " + credentials["static_jwt_token"]}
        json_data = {
            "document_id": self.redphoenix_document_id,
        }

        try:
            response = requests.post(
                credentials["rp_create_order"], headers=headers, json=json_data
            )
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            raise UserError(msg_err)

        check, err_resp = self.check_redphoenix_meta(response, "Create Order")
        if check:
            data = self.get_redphoenix_data(response)
            if "stamping_order_id" in data:
                self.stamping_order = data["stamping_order_id"]
                self.write(self._prepare_create_order_data())
        else:
            msg_err = _(err_resp)
            raise UserError(msg_err)
        self.env.cr.commit()

    @api.multi
    def _update_param(self):
        self.ensure_one()
        credentials = self._get_redphoenix_credentials()
        headers = {"Authorization": "Bearer " + credentials["static_jwt_token"]}
        json_data = self._prepare_param_data()
        try:
            response = requests.put(
                credentials["rp_update_param"], headers=headers, json=json_data
            )
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            raise UserError(msg_err)

        check, err_resp = self.check_redphoenix_meta(response, "Update Param")

        if not check:
            msg_err = _(err_resp)
            raise UserError(msg_err)
        self.write(self._prepare_update_param_data())
        self.env.cr.commit()

    @api.multi
    def _submit_document(self):
        self.ensure_one()
        credentials = self._get_redphoenix_credentials()
        headers = {"Authorization": "Bearer " + credentials["static_jwt_token"]}

        try:
            response = requests.put(credentials["rp_submit_document"], headers=headers)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            raise UserError(msg_err)

        check, err_resp = self.check_redphoenix_meta(response, "Submit Document")
        if check:
            self.write(self._prepare_submit_document_data())
        else:
            msg_err = _(err_resp)
            raise UserError(msg_err)
        self.env.cr.commit()

    @api.multi
    def _generate_sn(self):
        self.ensure_one()
        credentials = self._get_redphoenix_credentials()
        headers = {"Authorization": "Bearer " + credentials["static_jwt_token"]}
        data = {}

        try:
            response = requests.put(
                credentials["rp_generate_sn"], headers=headers, data=data
            )
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            raise UserError(msg_err)

        check, err_resp = self.check_redphoenix_meta(response, "Generate SN")
        if check:
            self.write(self._prepare_generate_sn_data())
        else:
            msg_err = _(err_resp)
            raise UserError(msg_err)
        self.env.cr.commit()

    @api.multi
    def _complete_tera(self):
        self.ensure_one()
        credentials = self._get_redphoenix_credentials()
        headers = {
            "Authorization": "Bearer " + credentials["static_jwt_token"],
        }

        try:
            response = requests.put(credentials["rp_complete_terra"], headers=headers)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            raise UserError(msg_err)

        check, err_resp = self.check_redphoenix_meta(response, "Complete Terra")
        if check:
            self.write(self._prepare_complete_tera_data())
        else:
            msg_err = _(err_resp)
            raise UserError(msg_err)
        self.env.cr.commit()

    @api.multi
    def _download_document(self):
        self.ensure_one()
        credentials = self._get_redphoenix_credentials()
        headers = {
            "Authorization": "Bearer " + credentials["static_jwt_token"],
        }

        try:
            response = requests.get(credentials["rp_download_doc"], headers=headers)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            raise UserError(msg_err)
        if response:
            self.write(self._prepare_download_document_data(response.content))
        else:
            msg_err = _("Response Error")
            raise UserError(msg_err)
        self.env.cr.commit()

    # @api.multi
    # def _action_add_document(self):
    #     self.ensure_one()
    #     self._add_document()
    #     if self.redphoenix_document_id:
    #         self.ematerai_document_id.action_create_order()
    #
    # @api.multi
    # def _action_create_order(self):
    #     self.ensure_one()
    #     if self.stamping_order:
    #         self._create_order()
    #         self.ematerai_document_id.action_update_param()
    #
    # @api.multi
    # def _action_update_param(self):
    #     self.ensure_one()
    #     raise UserError(_("Update Param Masuk"))
    #     if self.stamping_order:
    #         self._update_param()
    #         self.ematerai_document_id.action_submit_document()
    #
    # @api.multi
    # def _action_submit_document(self):
    #     self.ensure_one()
    #     if self.stamping_order:
    #         self._submit_document()
    #         self.ematerai_document_id.action_generate_sn()
    #
    # @api.multi
    # def _action_generate_sn(self):
    #     self.ensure_one()
    #     if self.stamping_order:
    #         self._generate_sn()
    #         self.ematerai_document_id.action_complete_tera()
    #
    # @api.multi
    # def _action_complete_tera(self):
    #     self.ensure_one()
    #     if self.stamping_order:
    #         self._complete_tera()
    #         self._download_document()

    @api.multi
    def _action_generate_ematerai(self):
        self.ensure_one()
        self._add_document()
        if self.redphoenix_document_id:
            self._create_order()
        if self.stamping_order:
            self._update_param()
            self._submit_document()
            self._generate_sn()
            self._complete_tera()
            self._download_document()
        return True
