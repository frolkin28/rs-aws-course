import json



def lambda_handler(event, context):
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Mouse", "price": 19.99},
        {"id": 3, "name": "Keyboard", "price": 49.99},
        {"id": 4, "name": "Monitor", "price": 199.99},
        {"id": 5, "name": "Headphones", "price": 89.99},
    ]

    try:
        raw_product_id = event.get("pathParameters", {}).get("id")
        product_id = int(raw_product_id)
    except (TypeError, ValueError):
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Invalid product ID"}),
        }

    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Product not found"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(product),
    }
