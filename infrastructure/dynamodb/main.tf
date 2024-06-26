resource "aws_dynamodb_table" "this" {
  name         = var.dynamodbTableName
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.project}-${var.environment}-dynamodbTable"
    }
  )
}

resource "aws_dynamodb_table_item" "this" {
  table_name = aws_dynamodb_table.this.name
  hash_key   = "id"
  item       = file("${path.module}/resume.json")
}
