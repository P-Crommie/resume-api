output "dynamodbTableArn" {
  value = aws_dynamodb_table.this.arn
}

output "dynamodbTableName" {
  value = aws_dynamodb_table.this.name
}

output "dynamodbTableID" {
  value = aws_dynamodb_table.this.id
}
