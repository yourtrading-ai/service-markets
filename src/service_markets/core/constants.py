SERVICE_MARKETS_MESSAGE_CHANNEL = "SERVICE_MARKETS_TEST_V0.3"
SERVICE_MARKETS_MANAGER_PUBKEYS = [
    "Bxa95pz5SkcKQE5Qji893inhxeXsnhVK8uALoF993fVv",  # Mike
    "6ZSRBF5tPYZg99mqp99w11tiePaaUn6HSZH1GKCn2w23", # Mike Docker
    "82AocbGgNL8uHeVqMiyL1phUdeyxW6ktTpfQk6syCcgF",  # Leonardo
    "7TTtzzYqWXtTcAqrsRzHPWa6T3fnkW6GjdkNe58TLYGJ"  # Leonardo Docker
]

API_PATH = "../api"
API_MESSAGE_FILTER = [
    {
        "channel": SERVICE_MARKETS_MESSAGE_CHANNEL,
        "type": "POST",
        "post_type": [
            "Service",
            "UserInfo",
            "Vote",
            "Comment",
            "Permission",
            "amend",
        ],
    }
]

VM_URL_PATH = "https://aleph.sh/vm/{hash}"
VM_URL_HOST = "https://{hash_base32}.aleph.sh"
