from urllib import response
from fastapi import HTTPException, APIRouter, status
from aiohttp import ClientSession
from models.request_models import (
    MoogoldOutputOfTheItem,
    MoogoldOutputOfTheItems,
    PurchaseMoogoldOutputOfTheItems,
)

import time
import hmac
import hashlib
import base64
import json
import os


from .func import (
    get_server,
    get_item,
    get_items_key_moogold,
    get_itemfs,
    change_status_output_moogold,
    write_order_id_in_itemfs,
    get_orders_list,
)


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
                                body
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
                        body
                    ),
                    "Status": response.status,
                    "Content-type": response.headers["content-type"],
                }
        except:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="BAD REQUEST"
            )


@router.post("/api/v1/moogold/purchase/outputs/item")
async def purchase_items(data: PurchaseMoogoldOutputOfTheItems):
    data_dict = data.model_dump()
    itemfs = await get_itemfs(data_dict.get("itemfs_id"))
    server_name = await get_server(user=itemfs.genshin_user_id)

    if not itemfs:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="itemfs not found"
        )

    moogold_items = await get_items_key_moogold(itemfs.item_id)

    response_data = {"data": []}

    async with ClientSession() as session:
        for i in moogold_items:
            for j in i:
                order = {
                    "path": "order/create_order",
                    "data": {
                        "category": GENSHIN_CATEGORY,
                        "product-id": j,
                        "quantity": "1",
                        "User ID": itemfs.genshin_user_id,
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
                    try:
                        body = await response.text()
                        body_json = json.loads(body)
                        try:
                            await write_order_id_in_itemfs(
                                itemfs=data_dict.get("itemfs_id"),
                                order_id=body_json.get("order_id"),
                            )
                        except Exception as err:
                            print(err)
                        response_data["data"].append(
                            {
                                "Body": body_json,
                                "Status": response.status,
                                "Content-type": response.headers["content-type"],
                            }
                        )
                    except Exception as err:
                        response_data["data"].append({"err": err, "moogold_item": j})

    await change_status_output_moogold(itemfs_id=itemfs.itemfs_id)

    return response_data


@router.get("/api/v1/moogoald/{moogoald_order_id}/order")
async def get_order(moogoald_order_id: str):
    async with ClientSession() as session:
        try:
            data = {"path": "order/order_detail", "order_id": moogoald_order_id}

            data_json = json.dumps(data)
            timestamp = str(int(time.time()))
            path = "order/order_detail"
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
                "https://moogold.com/wp-json/v1/api/order/order_detail",
                data=data_json,
                headers=headers,
            ) as response:
                body = await response.text()
                return {
                    "Body": json.loads(body),
                    "Status": response.status,
                    "Content-type": response.headers["content-type"],
                }
        except:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="BAD REQUEST"
            )


@router.get("/api/v1/moogoald/{itemfs_id}/order/list")
async def get_orders_itemfs_list(itemfs_id: str):
    result = await get_orders_list(itemfs_id=itemfs_id)
    return result
