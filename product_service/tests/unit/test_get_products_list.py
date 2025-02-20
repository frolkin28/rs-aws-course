import unittest
from lambda_functions.product_list import lambda_handler


class TestGetProductsList(unittest.TestCase):
    def test_lambda_handler(self):
        event = {}
        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("application/json", response["headers"]["Content-Type"])
        self.assertIn("Laptop", response["body"])
        self.assertIn("Mouse", response["body"])


if __name__ == "__main__":
    unittest.main()
