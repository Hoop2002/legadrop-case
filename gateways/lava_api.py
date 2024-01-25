from aiohttp import ClientSession

import requests
import hmac
import json
import hashlib


class LavaApi:
    def __init__(self, secret_key, shop_id):
        self.URL = "https://api.lava.ru"
        self.SECRETKEY = secret_key
        self.SHOP_ID = shop_id

    async def create_order(self, data: dict, router: str = "/business/invoice/create"):
        data = await self.sortDict(data)
        json_str = json.dumps(data).encode()

        auth = hmac.new(
            bytes(self.SECRETKEY, "UTF-8"),
            json_str,
            hashlib.sha256,
        ).hexdigest()

        async with ClientSession() as session:
            async with session.post(
                url=self.URL + router,
                json=data,
                headers={
                    "Signature": auth,
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            ) as response:
                body = await response.text()

                return json.loads(body)

    async def sortDict(self, data: dict):
        sorted_tuple = sorted(data.items(), key=lambda x: x[0])
        return dict(sorted_tuple)

    async def get_order_status(
        self, invoice_id, order_id, router="/buisiness/invoice/status"
    ):
        data = await self.sortDict(
            {"shopId": self.SHOP_ID, "orderId": order_id, "invoiceId": invoice_id},
        )
        json_str = json.dumps(data).encode()

        auth = hmac.new(
            bytes(self.SECRETKEY, "UTF-8"),
            json_str,
            hashlib.sha256,
        ).hexdigest()

        async with ClientSession() as session:
            async with session.post(
                url=self.URL + router,
                json=data,
                headers={
                    "Signature": auth,
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            ) as response:
                body = await response.text()
                return json.loads(body)

    def sync_create_order(self, data: dict, router: str = "/business/invoice/create"):
        data = self.SyncSortDict(data)
        json_str = json.dumps(data).encode()

        auth = hmac.new(
            bytes(self.SECRETKEY, "UTF-8"),
            json_str,
            hashlib.sha256,
        ).hexdigest()

        response = requests.post(
            self.URL + router,
            json=data,
            headers={
                "Signature": auth,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        return json.loads(response.content.decode("utf-8"))

    def sync_get_order_status(
        self,
        invoice_id,
        order_id,
        router="/business/invoice/status",
    ):
        data = self.SyncSortDict(
            {"shopId": self.SHOP_ID, "orderId": order_id, "invoiceId": invoice_id},
        )
        json_str = json.dumps(data).encode()

        auth = hmac.new(
            bytes(self.SECRETKEY, "UTF-8"),
            json_str,
            hashlib.sha256,
        ).hexdigest()

        response = requests.post(
            self.URL + router,
            json=data,
            headers={
                "Signature": auth,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        return json.loads(response.content.decode("utf-8"))

    def SyncSortDict(self, data: dict):
        sorted_tuple = sorted(data.items(), key=lambda x: x[0])
        return dict(sorted_tuple)
