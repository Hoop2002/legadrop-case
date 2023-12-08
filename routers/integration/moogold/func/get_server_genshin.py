SERVERS = {"6": "America", "7": "Europe", "8": "Asia", "9": "TW, HK, MO"}


async def get_server(user):
    id = user[0]
    for i in SERVERS.items():
        if i[0] == id:
            return i[1]

    return False
