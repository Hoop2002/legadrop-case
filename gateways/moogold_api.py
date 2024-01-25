from aiohttp import ClientSession

import time
import hmac
import hashlib
import base64
import json
import requests


class ApiMoogold:
    def __init__(self, secret_key: str, parner_id: str, category: str):
        self.SECRET_KEY = secret_key
        self.PARTNER_ID = parner_id
        self.CATEGORY = category

    def buy_moogold_item(self, product_id, quantity, server, uid):
        order = {
            "path": "order/create_order",
            "data": {
                "category": self.CATEGORY,
                "product-id": product_id,
                "quantity": quantity,
                "User ID": uid,
                "Server": server,
            },
        }
        order_json = json.dumps(order)

        timestamp = str(int(time.time()))

        path = "order/create_order"
        string_to_sign = order_json + timestamp + path

        auth = hmac.new(
            bytes(self.SECRET_KEY, "utf-8"),
            msg=string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        auth_basic = base64.b64encode(
            f"{self.PARTNER_ID}:{self.SECRET_KEY}".encode()
        ).decode()

        headers = {
            "timestamp": timestamp,
            "auth": auth,
            "Authorization": "Basic " + auth_basic,
            "Content-Type": "application/json",
        }

        response = requests.post(
            url="https://moogold.com/wp-json/v1/api/order/create_order",
            data=order_json,
            headers=headers,
        )

        return json.loads(response.content.decode("utf-8"))

    def get_moogold_order_detail(self, order_id):
        order = {"path": "order/order_detail", "order_id": order_id}
        order_json = json.dumps(order)

        timestamp = str(int(time.time()))

        path = "order/order_detail"
        string_to_sign = order_json + timestamp + path

        auth = hmac.new(
            bytes(self.SECRET_KEY, "utf-8"),
            msg=string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        auth_basic = base64.b64encode(
            f"{self.PARTNER_ID}:{self.SECRET_KEY}".encode()
        ).decode()

        headers = {
            "timestamp": timestamp,
            "auth": auth,
            "Authorization": "Basic " + auth_basic,
            "Content-Type": "application/json",
        }

        response = requests.post(
            url="https://moogold.com/wp-json/v1/api/order/order_detail",
            data=order_json,
            headers=headers,
        )

        return json.loads(response.content.decode("utf-8"))

    def get_moogold_balance(self):
        order = {"path": "user/balance"}
        order_json = json.dumps(order)

        timestamp = str(int(time.time()))

        path = "user/balance"
        string_to_sign = order_json + timestamp + path

        auth = hmac.new(
            bytes(self.SECRET_KEY, "utf-8"),
            msg=string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        auth_basic = base64.b64encode(
            f"{self.PARTNER_ID}:{self.SECRET_KEY}".encode()
        ).decode()

        headers = {
            "timestamp": timestamp,
            "auth": auth,
            "Authorization": "Basic " + auth_basic,
            "Content-Type": "application/json",
        }

        response = requests.post(
            url="https://moogold.com/wp-json/v1/api/user/balance",
            data=order_json,
            headers=headers,
        )

        return json.loads(response.content.decode("utf-8"))
