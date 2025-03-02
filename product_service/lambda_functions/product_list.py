import json


def lambda_handler(event, context):
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Mouse", "price": 19.99},
        {"id": 3, "name": "Keyboard", "price": 49.99},
        {"id": 4, "name": "Monitor", "price": 199.99},
        {"id": 5, "name": "Headphones", "price": 89.99},
    ]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(products),
    }
