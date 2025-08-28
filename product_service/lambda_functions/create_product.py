import json
import uuid
import os
from dataclasses import dataclass
from typing import Any

import boto3
from botocore.exceptions import ClientError


MIN_STRING_LEN = 2
MIN_INT_VALUE = 0


def _str_validator(field: str, value: Any, lenght: int):
    if not isinstance(value, str):
        raise TypeError(f"{field} must be str, got {type(value).__name__}")
    if len(value) < lenght:
        raise ValueError(f"Minimum lenght of {field} = {lenght}")


def _int_validator(field: str, value: Any, min_value: int):
    if not isinstance(value, int):
        raise TypeError(f"price must be int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{field} must be >= {min_value}")


@dataclass
class CreateProductPayload:
    title: str
    description: str
    price: int
    stock: int
    _product_id: str

    def __post_init__(self):
        _str_validator("title", self.title, MIN_STRING_LEN)
        _str_validator("description", self.description, MIN_STRING_LEN)

        _int_validator("price", self.price, MIN_INT_VALUE)
        _int_validator("stock", self.stock, MIN_INT_VALUE)

        self._product_id = str(uuid.uuid4())

    @property
    def product_id(self) -> str:
        return self._product_id


def lambda_handler(event, context):
    products_table_name = os.getenv("PRODUCTS_TABLE_NAME")
    stocks_table_name = os.getenv("STOCKS_TABLE_NAME")
    assert products_table_name and stocks_table_name, "Table names os vars is missing"

    try:
        data = json.loads(event["body"])
    except json.JSONDecodeError as e:
        return {"statusCode": 422}

    try:
        payload = CreateProductPayload(**data)
    except (TypeError, ValueError) as e:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": str(e)}),
        }

    dynamodb = boto3.resource("dynamodb")
    try:
        dynamodb.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": products_table_name,
                        "Item": {
                            "id": {"S": payload.product_id},
                            "title": {"S": payload.title},
                            "description": {"S": payload.description},
                            "price": {"N": str(payload.price)},
                        },
                    }
                },
                {
                    "Put": {
                        "TableName": stocks_table_name,
                        "Item": {
                            "product_id": {"S": payload.product_id},
                            "count": {"N": str(payload.count)},
                        },
                    }
                },
            ]
        )
    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": f"Unexpected error: {e}"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"product_id": payload.product_id}),
    }
