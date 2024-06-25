variable "project" {
  type    = string
  default = "cloud-resume-api"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "tags" {
  type = map(string)
  default = {
    CreatedBy = "crommie"
  }
}

variable "dynamodbTableName" {
  type    = string
  default = "Resume"
}

variable "lambdaVars" {
  type = object({
    function_name = string
    image_uri     = string
    timeout       = optional(number)
    memory_size   = optional(number)
  })
  default = {
    function_name = "cloud-resume-api"
    image_uri     = "522986700920.dkr.ecr.eu-west-1.amazonaws.com/cloud-resume-api:latest"
    timeout       = 30
    memory_size   = 128
  }
}
