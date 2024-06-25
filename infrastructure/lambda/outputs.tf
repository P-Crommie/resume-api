output "lambaFunctionInvokeArn" {
  value = aws_lambda_function.this.invoke_arn
}

output "lambdaFunctionName" {
  value = aws_lambda_function.this.function_name
}
