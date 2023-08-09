# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from requests import get
from . import (
    ParseMode,
    _try_purged,
    eor,
    get_text,
    is_ipv4,
    is_url,
    plugins_helper,
    px,
    pytel,
    suppress,
    fetch_ipinfo,
    fetch_dns,
    random_prefixies,
    screenshots,)


@pytel.instruction(
    ["webss"],
    outgoing=True,
    privileges=[
        "can_send_media_messages"
    ],
)
async def _screenshots(client, message):
    url = get_text(
        message, save_link=True
    )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid link!",
        )
        return

    x = await eor(
        message,
        text="Take a screenshot...",
    )
    try:
        file = await screenshots(
            url=url,
            download=False,
        )
    except BaseException as excp:
        await eor(
            x,
            text=f"{excp}",
        )
        return

    if file:
        with suppress(Exception):
            z = await eor(
                x,
                text="Uploading...",
            )
            await client.send_document(
                z.chat.id,
                document=file,
                caption=(
                    "{} [PYTEL](https://github.com/kastaid/pytel)".format(
                        "Made using",
                    )
                    + "\n{} [KASTA ID 🇮🇩](t.me/kastaid)".format(
                        "a Project by",
                    )
                ),
                parse_mode=ParseMode.MARKDOWN,
                force_document=True,
                disable_notification=True,
            )
            await _try_purged(z, 2.5)
            return
    else:
        await eor(
            x,
            text="Sorry, couldn't capture the screen.",
        )
        return


@pytel.instruction(
    [
        "shorten_isgd",
        "shorten_tiny",
        "shorten_clck",
    ],
    outgoing=True,
)
async def _shorten_url(client, message):
    url = get_text(
        message, save_link=True
    )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid link!",
        )
        return

    x = await eor(
        message,
        text="Shorten...",
    )
    if (
        message.command[0]
        == "shorten_isgd"
    ):
        rsp = get(
            "https://is.gd/create.php",
            params={
                "format": "simple",
                "url": url,
            },
        )
    elif (
        message.command[0]
        == "shorten_tiny"
    ):
        rsp = get(
            "http://tinyurl.com/api-create.php",
            params={"url": url},
        )
    elif (
        message.command[0]
        == "shorten_clck"
    ):
        rsp = get(
            "https://clck.ru/--",
            params={"url": url},
        )

    with suppress(BaseException):
        if not rsp.ok:
            response = rsp.text.strip()
            await eor(x, text=response)
            return
        else:
            response = rsp.text.strip()
            text = "<b><u>SHORT URL</b></u>\n"
            text += f" ├ <b>Input:</b> <code>{url}</code>\n"
            text += f" └ <b>Output:</b> <code>{response}</code>"
            await eor(x, text=text)
            return


@pytel.instruction(
    ["ipinfo"],
    outgoing=True,
)
async def _ip_info(client, message):
    ipv = get_text(
        message, save_link=True
    )
    if not ipv or not (
        is_ipv4(ipv) is True
    ):
        await eor(
            message,
            text="Provide a valid IP Address!",
        )
        return
    x = await eor(
        message,
        text="Fetches IP Address...",
    )
    str_ip = await fetch_ipinfo(ipv)
    if str_ip:
        await eor(x, text=str_ip)


@pytel.instruction(
    ["dns", "domain"],
    outgoing=True,
)
async def _domain_ns(client, message):
    url = get_text(
        message, save_link=True
    )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid domain url!",
        )
        return
    x = await eor(
        message,
        text="Fetches DNS...",
    )
    dn_server = await fetch_dns(url)
    if dn_server:
        await eor(x, text=dn_server)


plugins_helper["webtools"] = {
    f"{random_prefixies(px)}webss [url]/[reply link]": "To capture the screen on the link.",
    f"{random_prefixies(px)}shorten_[isgd/tiny/clck] [url]/[reply link]": "To shorten your link/url.",
    f"{random_prefixies(px)}dns / {random_prefixies(px)}domain [url]/[reply link]": "To get DNS ( Domain Name Server )",
    f"{random_prefixies(px)}ipinfo [ip address]": "To get information IP Address.",
}
