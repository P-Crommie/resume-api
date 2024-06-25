resource "aws_lambda_function" "this" {
  function_name = var.lambdaVars.function_name
  package_type  = "Image"
  image_uri     = var.lambdaVars.image_uri
  timeout       = var.lambdaVars.timeout
  memory_size   = var.lambdaVars.memory_size
  role          = aws_iam_role.this.arn

  environment {
    variables = {
      TABLE_NAME = var.dynamodbTableName
    }
  }
}