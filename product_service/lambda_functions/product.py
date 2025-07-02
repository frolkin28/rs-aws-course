import json
import os

import boto3


def lambda_handler(event, _):
    products_table_name = os.getenv("PRODUCTS_TABLE_NAME")
    stocks_table_name = os.getenv("STOCKS_TABLE_NAME")
    assert products_table_name and stocks_table_name, "Table names os vars is missing"

    product_id = event.get("pathParameters", {}).get("id")
    if not product_id:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Invalid product ID"}),
        }

    dynamodb = boto3.resource("dynamodb")
    products_table = dynamodb.Table("products")

    response = products_table.get_item(Key={"id": product_id})
    product = response.get("Item")
    if not product:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
        }

    stock_table = dynamodb.Table(stocks_table_name)
    response = stock_table.get_item(Key={"product_id": product_id})
    stock = response.get("Item")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "id": product["id"],
                "count": int(stock["count"]) if stock else None,
                "price": int(product["price"]),
                "title": product["title"],
                "description": product["description"],
            }
        ),
    }
