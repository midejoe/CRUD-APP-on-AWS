resource "aws_api_gateway_rest_api" "serveless-api" {
    api_key_source               = "HEADER"
    disable_execute_api_endpoint = false
    minimum_compression_size     = -1
    name                         = "serveless-api"
    put_rest_api_mode            = "overwrite"

    endpoint_configuration {
        types            = [
            "REGIONAL",
        ]
        vpc_endpoint_ids = []
    }
}

