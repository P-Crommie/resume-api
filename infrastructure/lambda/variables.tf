variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "lambdaVars" {
  type = object({
    function_name = string
    image_uri     = string
    timeout       = number
    memory_size   = number
  })
}

variable "dynamodbTableArn" {
  type = string
}

variable "dynamodbTableName" {
  type = string
}
