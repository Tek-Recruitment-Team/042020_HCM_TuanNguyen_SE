# -*- coding: utf-8 -*-

import hashlib
import werkzeug
import logging
import urllib
from odoo import http
from odoo.http import request, content_disposition
from controller import settings

_logger = logging.getLogger()

class MainController(http.Controller):

    @http.route(['/payment_vnpay'], type='json', auth='user', website=True)
    def payment_vnpay(self, data):
        try:
            payment = request.env['payment.payment']
            url = payment.build_payment_vnpay_url('vnpay', data) # Return URL with param
            if not url:
                result = {"msg": "Thiếu params thanh toán !!!"}
                return request.render('web.payment_fail', result)
            return werkzeug.utils.redirect(url, 302) # redirect qua trang thanh toan
        except Exception as e:
            _logger.error(e)
            return {'error_msg': 'Error: {0}'.format(e)}
        finally:
            _logger.info("UPDATE VÀO TRANSACTION TRẠNG THÁI: CHỜ THANH TOÁN")

    @http.route(['/payment_vnpay_return'], type='GET', auth='user', website=True)
    def payment_vnpay_return(self, **kw):
        try:
            code = 'vnpay'
            input_data = request.GET
            if not input_data:
                return request.render('web.payment_fail', {"msg": "Thiếu params return !!!"})
            input_data = input_data.dict()
            config_value = settings.get(code)
            if self.validate_response(input_data, config_value.VNPAY_HASH_SECRET_KEY):
                vnp_ResponseCode = input_data.get('vnp_ResponseCode')
                # rebuild value return
                result = {
                    "order_id": input_data['vnp_TxnRef'],
                    "amount": int(input_data['vnp_Amount']) / 100,
                    "order_desc": input_data['vnp_OrderInfo'],
                    "vnp_TransactionNo": input_data['vnp_TransactionNo'],
                    "vnp_ResponseCode": input_data['vnp_ResponseCode']
                }
                if vnp_ResponseCode == "00":
                    # CODE UPDATE TRANSACTION THÀNH CÔNG
                    result.update({"msg": "Thành công"})
                    return request.render('web.payment_success', result)
                else:
                    # CODE UPDATE TRANSACTION THẤT BẠI
                    result.update({"msg": "Thiếu params return !!!"})
                    return request.render('web.payment_fail', result)
            else:
                result = {"msg": "Sai checksum !!!"}
                return request.render('web.payment_fail', result)
        except Exception as e:
            _logger.error(e)
            result = {"msg": "Lỗi phát sinh trong quá trình lấy thông tin thanh toán !!!"}
            return request.render('web.payment_fail', result)

    def validate_params(self, data):
        require_param = ['vnp_Amount','vnp_Command','vnp_CreateDate','vnp_CurrCode',
                         'vnp_Merchant','vnp_OrderInfo','vnp_TmnCode','vnp_TxnRef']
        for item in require_param:
            if not data.has_key(item):
                return False
        return True

    def map_config_data(self, data, config_value):
        res = {}
        except_key = ('vnp_RETURN_URL', 'vnp_PAYMENT_URL', 'vnp_API_URL', 'vnp_TMN_CODE', 'vnp_HASH_SECRET_KEY')
        for key, value in config_value:
            if key in except_key:
                continue
            if data.get(key):
                res.update({key: data.get(key)})
            else:
                res.update({key: value})
        return res

    def build_payment_vnpay_url(self, code, form_value):
        headers = {"Content-type": "application/json"}
        # Build param
        config_value = settings.get(code)
        if self.validate_params(form_value):
            return False
        res = self.map_config_data(form_value, config_value)
        # Update some value
        res.update({'vnp_Amount': res.get('vnp_Amount', 0) * 100})
        # Get config
        secret_key = config_value.get('VNPAY_HASH_SECRET_KEY')
        payment_url = config_value.get('vnp_PAYMENT_URL')
        res = self.get_hash(res, secret_key)
        param_string = urllib.parse.urlencode(res)
        payment_url = "?".join((payment_url, param_string))
        return self.request_url(headers, res, payment_url)

    def get_hash(self, data, secret_key):
        hash_data = ''
        seq = 0
        for key, val in data:
            if seq == 1:
                hash_data = hash_data + "&" + str(key) + '=' + str(val)
            else:
                seq = 1
                hash_data = str(key) + '=' + str(val)
        hash_value = self.__md5(secret_key + hash_data)
        data.update({'vnp_SecureHash': hash_value, 'vnp_SecureHashType': 'MD5'})
        return data

    def __md5(self, input):
        byteInput = input.encode('utf-8')
        return hashlib.md5(byteInput).hexdigest()

    def validate_response(self, input_data, secret_key):
        vnp_SecureHash = input_data.get('vnp_SecureHash')
        hasData = ''
        seq = 0
        for key, val in input_data:
            if str(key).startswith('vnp_'):
                if seq == 1:
                    hasData = hasData + "&" + str(key) + '=' + str(val)
                else:
                    seq = 1
                    hasData = str(key) + '=' + str(val)
        hashValue = self.__md5(secret_key + hasData)
        _logger.debug("Validate input hash {0}, hashValue {1}".format(vnp_SecureHash, hashValue))
        return vnp_SecureHash == hashValue