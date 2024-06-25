variable "project" {
  type = string
}

variable "environment" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "lambaFunctionInvokeArn" {
  type = string
}

variable "lambdaFunctionName" {
  type = string
}
