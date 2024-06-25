module "dynamodbTable" {
  source            = "./dynamodb"
  dynamodbTableName = var.dynamodbTableName
  project           = var.project
  environment       = var.environment
  tags              = var.tags
}

module "lambdaFunction" {
  source            = "./lambda"
  lambdaVars        = var.lambdaVars
  project           = var.project
  environment       = var.environment
  tags              = var.tags
  dynamodbTableArn  = module.dynamodbTable.dynamodbTableArn
  dynamodbTableName = module.dynamodbTable.dynamodbTableName
}

module "apiGateway" {
  source                 = "./api-gateway"
  project                = var.project
  environment            = var.environment
  tags                   = var.tags
  lambdaFunctionName     = module.lambdaFunction.lambdaFunctionName
  lambaFunctionInvokeArn = module.lambdaFunction.lambaFunctionInvokeArn
}
