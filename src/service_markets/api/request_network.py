import requests
from enum import Enum
from typing import List, Optional, Any

import aiohttp
from pydantic import BaseModel

example_invoice = {
    "creationDate": "2022-12-22T14:38:16.916Z",
    "invoiceItems": [
        {
            "currency": "USD",
            "name": "Television",
            "quantity": 2,
            "tax": {
                "type": "percentage",
                "amount": "20"
            },
            "unitPrice": "9999"
        }
    ],
    "invoiceNumber": "13",
    "buyerInfo": {
        "businessName": "Acme Wholesaler Ltd.",
        "address": {
            "streetAddress": "4933 Oakwood Avenue",
            "extendedAddress": "",
            "city": "New York",
            "postalCode": "10038",
            "region": "New York",
            "country": "US"
        },
        "email": "justin.walton@acme-wholesaler.com",
        "firstName": "Justin",
        "lastName": "Walton",
        "taxRegistration": "985-80-3313"
    },
    "paymentTerms": {
        "dueDate": "2023-01-21T23:59:59.999Z"
    },
    "paymentAddress": "0x4886E85E192cdBC81d42D89256a81dAb990CDD74",
    "paymentCurrency": "USDC-matic",
    "tags": [
        "my_tag"
    ],
    "status": "paid"
}

"""
You can check the status field of the JSON response. The different statuses of an invoice are the following:
open – The request associated with the invoice has been created on-chain. The buyer has not yet paid the invoice.
accepted – The invoice has been approved by the buyer.
declaredPaid – The buyer declared the invoice as paid. The seller has to confirm before the invoice can move into the paid status. This is necessary for currencies, where the Request Network does not yet support payment detection.
paid – Final state. The buyer paid the invoice.
canceled – Final state. The seller canceled the invoice.
rejected – Final state. The buyer rejected the invoice.
scheduled – Status for recurring invoices. Indicates that an invoice will be created on a specific date in the future.
draft – The invoice is in draft status. It can still be edited and was not yet converted into an on-chain request. This status is currently only supported when creating an invoice in the Request Finance UI.
"""


class InvoiceStatus(str, Enum):
    open = "open"
    accepted = "accepted"
    declaredPaid = "declaredPaid"
    paid = "paid"
    canceled = "canceled"
    rejected = "rejected"
    scheduled = "scheduled"
    draft = "draft"


class InvoiceItem(BaseModel):
    currency: str
    name: str
    quantity: int
    tax: dict
    unitPrice: str


class BuyerInfo(BaseModel):
    businessName: str
    address: dict
    email: str
    firstName: str
    lastName: str
    taxRegistration: str


class PaymentTerms(BaseModel):
    dueDate: str


class Invoice(BaseModel):
    creationDate: str
    invoiceItems: List[InvoiceItem]
    invoiceNumber: str
    buyerInfo: BuyerInfo
    paymentTerms: PaymentTerms
    paymentAddress: str
    paymentCurrency: str
    tags: List[str]
    status: Optional[InvoiceStatus] = None


request_network_api_key = "4B8VN2G-56Q4K77-P8BY5MS-6123CD7"


async def fetch_invoice(
        invoice_id: str,
) -> Any:
    """
    Fetch an invoice from the request network API.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.request.finance/invoices/{invoice_id}", headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": request_network_api_key,
        }) as response:
            return await response.json()


def fetch_invoice_sync(
        invoice_id: str,
) -> Any:
    """
    Fetch an invoice from the request network API.
    """
    import requests
    response = requests.get(f"https://api.request.finance/invoices/{invoice_id}", headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": request_network_api_key,
    })
    return response.json()


async def fetch_invoices() -> Any:
    """
    Fetch invoices from the request network API.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.request.finance/invoices", headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": request_network_api_key,
        }) as response:
            return await response.json()


def fetch_invoices_sync() -> Any:
    """
    Fetch invoices from the request network API.
    """
    import requests
    response = requests.get(f"https://api.request.finance/invoices", headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": request_network_api_key,
    })
    return response.json()


async def create_invoice(
    invoice: Invoice,
) -> Any:
    """
    Create an invoice on the request network API.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://api.request.finance/invoices", headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": request_network_api_key,
        }, params=invoice.dict()) as response:
            return await response.json()


def create_invoice_sync(
    invoice: Invoice,
) -> Any:
    """
    Create an invoice on the request network API.
    """
    response = requests.post(f"https://api.request.finance/invoices", headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": request_network_api_key,
    }, params=invoice.dict())
    return response.json()
