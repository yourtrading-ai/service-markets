from datetime import datetime
from os import getenv

from aars import AARS
from aleph.sdk.client import AuthenticatedAlephClient
from aleph.sdk.chains.sol import get_fallback_account
from aleph.sdk.conf import settings
from aleph.sdk.vm.cache import TestVmCache, VmCache

from .constants import SERVICE_MARKETS_MESSAGE_CHANNEL, SERVICE_MARKETS_MANAGER_PUBKEYS


async def initialize_aars():
    test_cache_flag = getenv("TEST_CACHE")
    if test_cache_flag is not None and test_cache_flag.lower() == "false":
        cache = VmCache()
    else:
        cache = TestVmCache()

    aleph_account = get_fallback_account()
    aleph_session = AuthenticatedAlephClient(aleph_account, settings.API_HOST)

    test_channel_flag = getenv("TEST_CHANNEL")
    custom_channel = getenv("CUSTOM_CHANNEL")
    if custom_channel:
        channel = custom_channel
    elif test_channel_flag is not None and test_channel_flag.lower() == "true":
        channel = "SERVICE_MARKETS_TEST_" + str(datetime.now())
    else:
        channel = SERVICE_MARKETS_MESSAGE_CHANNEL

    print("Using channel: " + channel)

    aars = AARS(
        account=aleph_account, channel=channel, cache=cache, session=aleph_session
    )

    if aleph_account.get_address() in SERVICE_MARKETS_MANAGER_PUBKEYS:
        try:
            resp, status = await aleph_session.fetch_aggregate(
                "security", aleph_account.get_address()
            )
            existing_authorizations = resp.json().get("authorizations", [])
        except:
            existing_authorizations = []
        needed_authorizations = [
            {
                "address": address,
                "channels": [SERVICE_MARKETS_MESSAGE_CHANNEL],
            }
            for address in SERVICE_MARKETS_MANAGER_PUBKEYS
        ]
        if not all(auth in existing_authorizations for auth in needed_authorizations):
            aggregate = {
                "authorizations": needed_authorizations,
            }
            await aleph_session.create_aggregate(
                "security", aggregate, aleph_account.get_address(), channel="security"
            )

    return aars
