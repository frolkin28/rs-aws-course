import unittest

from lambda_functions.product import lambda_handler


class TestGetProductsById(unittest.TestCase):
    def test_product_found(self):
        event = {"pathParameters": {"id": "1"}}
        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Laptop", response["body"])

    def test_product_not_found(self):
        event = {"pathParameters": {"id": "999"}}
        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 404)
        self.assertIn("Product not found", response["body"])

    def test_no_id_provided(self):
        event = {"pathParameters": None}
        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 404)
        self.assertIn("Product not found", response["body"])

    def test_path_parameters_missing(self):
        event = {}
        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 404)
        self.assertIn("Product not found", response["body"])


if __name__ == "__main__":
    unittest.main()
