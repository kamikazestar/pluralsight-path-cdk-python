from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    core
)


class LambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        hello_function = _lambda.Function(
            self, 'WelcomeHandler',
            runtime = _lambda.Runtime.PYTHON_3_8,
            code = _lambda.Code.asset('lambda-api'),
            handler = 'welcome.handler',
        )
        
        api_gw = apigw.LambdaRestApi(
           self, 'ApiEndpoint',
           handler = hello_function,
        )

        