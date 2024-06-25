resource "aws_iam_role" "this" {
  name = "${var.project}-${var.environment}-lambdaRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = merge(
    var.tags,
    {
      Name = "${var.project}-${var.environment}-lambdaRole"
    }
  )
}


resource "aws_iam_policy" "this" {
  name = "${var.project}-${var.environment}-lambdaPolicy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "dynamodb:GetItem"
        ],
        Effect   = "Allow",
        Resource = var.dynamodbTableArn
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })

  tags = merge(
    var.tags,
    {
      Name = "${var.project}-${var.environment}-lambdaPolicy"
    }
  )
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}
