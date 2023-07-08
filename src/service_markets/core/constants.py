SERVICE_MARKETS_MESSAGE_CHANNEL = "SERVICE_MARKETS_TEST_V0.4"
SERVICE_MARKETS_MANAGER_PUBKEYS = [
    "Bxa95pz5SkcKQE5Qji893inhxeXsnhVK8uALoF993fVv",  # Mike
    "6ZSRBF5tPYZg99mqp99w11tiePaaUn6HSZH1GKCn2w23",  # Mike Docker
    "82AocbGgNL8uHeVqMiyL1phUdeyxW6ktTpfQk6syCcgF",  # Leonardo
    "7TTtzzYqWXtTcAqrsRzHPWa6T3fnkW6GjdkNe58TLYGJ",  # Leonardo Docker
    "6Bf4i3vGhjtz69y2bw1tpYPmCGR4PmgwW8JLTF2qy4Z2",  # Leonardo Extra
    "BExGtmNQP4eQjSNNuhWiGnUGW6aucZeJB7d3uAaATcc5",  # Ricardo
]

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
