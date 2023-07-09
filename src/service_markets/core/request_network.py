import aiohttp
import requests
import json

from .model import Payment


async def fetch_payment(tx_hash: str) -> Payment:
    url = (
        "https://api.thegraph.com/subgraphs/name/requestnetwork/request-payments-goerli"
    )

    headers = {"Content-Type": "application/json"}
    request_json = json.dumps({"query": payment_query.format(tx_hash)})

    # Initiate the session
    async with aiohttp.ClientSession() as session:
        # Post the query
        async with session.post(url, headers=headers, data=request_json) as response:
            # Raise an exception in case of status error
            response.raise_for_status()

            # Fetch the json response
            json_response = await response.json()

    return Payment(**(await response.json())["data"]["payments"][0])


def fetch_payment_sync(tx_hash: str) -> Payment:
    # The endpoint URL for the Request Payments Subgraph
    url = (
        "https://api.thegraph.com/subgraphs/name/requestnetwork/request-payments-goerli"
    )

    headers = {"Content-Type": "application/json"}

    request_json = json.dumps({"query": payment_query.format(tx_hash)})

    # Post the query
    response = requests.post(url, headers=headers, data=request_json)

    # Raise an exception in case of status error
    response.raise_for_status()

    return Payment(**response.json()["data"]["payments"][0])


payment_query = """
{{
  payments(where: {{txHash: "{0}"}}, first: 1) {{
    amount
    txHash
    from
    to
    contractAddress
    tokenAddress
    reference
  }}
}}
"""
