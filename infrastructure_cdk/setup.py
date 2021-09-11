import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="infrastructure_cdk",
    version="0.0.1",

    description="A sample CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "infrastructure_cdk"},
    packages=setuptools.find_packages(where="infrastructure_cdk"),

    install_requires=[
        "aws-cdk.core==1.121.0",
        "aws-cdk.aws_apigateway==1.121.0",
        "aws-cdk.aws_lambda==1.121.0",
        "aws-cdk.aws_ecs==1.121.0",
        "aws-cdk.aws_ecr==1.121.0",
        "aws-cdk.aws_ecs_patterns==1.121.0",
        "aws-cdk.aws_ec2==1.121.0",
        "aws-cdk.aws_elasticloadbalancingv2==1.121.0",
        "aws-cdk.aws_autoscaling==1.121.0",
        "aws-cdk.aws_iam==1.121.0",
        "jsii",
        
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
