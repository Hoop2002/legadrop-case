from urllib import response
from fastapi import HTTPException, APIRouter, status
from aiohttp import ClientSession
from models.request_models import MoogoldOutputOfTheItem, MoogoldOutputOfTheItems

import time
import hmac
import hashlib
import base64
import json
import os


from .func import get_server, get_item, get_items_key_moogold


SECRET_KEY = os.getenv("MOOGOLD_SECRET_KEY")
PARTNER_ID = os.getenv("MOOGOLD_PARTNER_ID")
GENSHIN_CATEGORY = "428075"

router = APIRouter()


@router.post("/api/v1/moogold/purchase/item")
async def purchase(data: MoogoldOutputOfTheItem):
    data_dict = data.model_dump()

    server_name = await get_server(user=data_dict.get("genshin_user_id", False))

    if not server_name:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid genshin user id, server not found",
        )

    item = await get_item(item_id=data_dict.get("item_id", False))

    if not item:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid item id"
        )

    moogold_items = await get_items_key_moogold(item.item_id)

    async with ClientSession() as session:
        try:
            for i in moogold_items:
                for j in i:
                    order = {
                        "path": "order/create_order",
                        "data": {
                            "category": GENSHIN_CATEGORY,
                            "product-id": j,
                            "quantity": "1",
                            "User ID": data_dict.get("genshin_user_id", False),
                            "Server": server_name,
                        },
                    }
                    order_json = json.dumps(order)
                    timestamp = str(int(time.time()))
                    path = "order/create_order"
                    string_to_sign = order_json + timestamp + path
                    auth = hmac.new(
                        bytes(SECRET_KEY, "utf-8"),
                        msg=string_to_sign.encode("utf-8"),
                        digestmod=hashlib.sha256,
                    ).hexdigest()
                    auth_basic = base64.b64encode(
                        f"{PARTNER_ID}:{SECRET_KEY}".encode()
                    ).decode()

                    headers = {
                        "timestamp": timestamp,
                        "auth": auth,
                        "Authorization": "Basic " + auth_basic,
                        "Content-Type": "application/json",
                    }

                    async with session.post(
                        "https://moogold.com/wp-json/v1/api/order/create_order",
                        data=order_json,
                        headers=headers,
                    ) as response:
                        body = await response.text()
                        return {
                            "Body": json.loads(
                                body.replace("\n", "").replace("\r", "").strip()
                            ),
                            "Status": response.status,
                            "Content-type": response.headers["content-type"],
                        }

        except:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="BAD REQUEST"
            )


@router.get("/api/v1/moogold/balance")
async def moogold_balance():
    async with ClientSession() as session:
        try:
            data = {"path": "user/balance"}

            data_json = json.dumps(data)
            timestamp = str(int(time.time()))
            path = "user/balance"
            string_to_sign = data_json + timestamp + path
            auth = hmac.new(
                bytes(SECRET_KEY, "utf-8"),
                msg=string_to_sign.encode("utf-8"),
                digestmod=hashlib.sha256,
            ).hexdigest()

            auth_basic = base64.b64encode(
                f"{PARTNER_ID}:{SECRET_KEY}".encode()
            ).decode()
            headers = {
                "timestamp": timestamp,
                "auth": auth,
                "Authorization": "Basic " + auth_basic,
                "Content-Type": "application/json",
            }
            async with session.post(
                "https://moogold.com/wp-json/v1/api/user/balance",
                data=data_json,
                headers=headers,
            ) as response:
                body = await response.text()
                return {
                    "Body": json.loads(
                        body.replace("\n", "").replace("\r", "").strip()
                    ),
                    "Status": response.status,
                    "Content-type": response.headers["content-type"],
                }
        except:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="BAD REQUEST"
            )


@router.post("/api/v1/moogoald/purchase/items")
async def purchase_items(data: MoogoldOutputOfTheItems):
    pass
