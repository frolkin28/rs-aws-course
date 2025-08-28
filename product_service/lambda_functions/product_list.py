import json
import os

import boto3


def lambda_handler(event, context):
    products_table_name = os.getenv("PRODUCTS_TABLE_NAME")
    stocks_table_name = os.getenv("STOCKS_TABLE_NAME")
    assert products_table_name and stocks_table_name, "Table names os vars is missing"

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(products_table_name)
    response = table.scan(Limit=10)
    products = response.get("Items", [])
    if not products:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(products),
        }

    keys = [
        {
            "product_id": {"S": str(p["id"])},
        }
        for p in products
    ]
    request_items = {}
    request_items[stocks_table_name] = {"Keys": keys}
    response = dynamodb.batch_get_item(
        RequestItems=request_items,
    )

    stocks_map = {s["product_id"]: s for s in response["Responses"].get("stocks", [])}
    products_response = [
        {
            "id": product["id"],
            "count": stock_count,
            "price": product["price"],
            "title": product["title"],
            "description": product["description"],
        }
        for product in products
        if (stock_count := stocks_map.get(product["id"], 0))
    ]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(products_response),
    }
