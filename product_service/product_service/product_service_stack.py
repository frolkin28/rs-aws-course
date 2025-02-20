import os

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    CfnOutput,
)
from constructs import Construct


class ProductServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda for getProductsList
        get_products_list_lambda = _lambda.Function(
            self,
            "GetProductsListFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="product_list.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "../lambda_functions")
            ),
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
        )

        # API Gateway
        api = apigateway.RestApi(
            self,
            "ProductsApi",
            rest_api_name="Products Service",
            description="This service serves product information.",
            deploy_options=apigateway.StageOptions(stage_name="")
        )

        # /products endpoint -> getProductsListLambda
        products_resource = api.root.add_resource("products")
        products_resource.add_method(
            "GET", apigateway.LambdaIntegration(get_products_list_lambda)
        )

        # /products/{id} endpoint -> getProductsByIdLambda
        product_by_id_resource = products_resource.add_resource("{id}")
        product_by_id_resource.add_method(
            "GET", apigateway.LambdaIntegration(get_products_by_id_lambda)
        )

        # Output the API Gateway URL
        CfnOutput(self, "ApiGatewayUrl", value=api.url)
