variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "dynamodbTableName" {
  type = string
}
