import os

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    CfnOutput,
    aws_iam as iam,
)
from constructs import Construct


class ProductServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        env = {"PRODUCTS_TABLE_NAME": "products", "STOCKS_TABLE_NAME": "stocks"}

        role = iam.Role.from_role_name(
            self, "DynamoDBLambdaAccessRole", "DynamoDBLambdaAccess"
        )

        # Lambda for getProductsList
        get_products_list_lambda = _lambda.Function(
            self,
            "GetProductsListFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="product_list.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "../lambda_functions")
            ),
            environment=env,
            role=role,
        )

        # Lambda for getProductsById
        get_products_by_id_lambda = _lambda.Function(
            self,
            "GetProductsByIdFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="product.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "../lambda_functions")
            ),
            environment=env,
            role=role,
        )

        # Lambda for createProduct
        create_product_lambda = _lambda.Function(
            self,
            "CreateProductFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="create_product.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "../lambda_functions")
            ),
            environment=env,
            role=role,
        )

        # API Gateway
        api = apigateway.RestApi(
            self,
            "ProductsApi",
            rest_api_name="Products Service",
            description="This service serves product information.",
            deploy_options=apigateway.StageOptions(stage_name=""),
        )

        # /products endpoint -> getProductsListLambda, createProductLambda
        products_resource = api.root.add_resource("products")
        products_resource.add_method(
            "GET", apigateway.LambdaIntegration(get_products_list_lambda)
        )
        products_resource.add_method(
            "POST", apigateway.LambdaIntegration(create_product_lambda)
        )

        # /products/{id} endpoint -> getProductsByIdLambda
        product_by_id_resource = products_resource.add_resource("{id}")
        product_by_id_resource.add_method(
            "GET", apigateway.LambdaIntegration(get_products_by_id_lambda)
        )

        # Output the API Gateway URL
        CfnOutput(self, "ApiGatewayUrl", value=api.url)
