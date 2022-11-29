resource "aws_iam_role" "serverless-api-role" {
    assume_role_policy    = jsonencode(
        {
            Statement = [
                {
                    Action    = "sts:AssumeRole"
                    Effect    = "Allow"
                    Principal = {
                        Service = "lambda.amazonaws.com"
                    }
                },
            ]
            Version   = "2012-10-17"
        }
    )
    description           = "Allows Lambda functions to call AWS services on your behalf."
    force_detach_policies = false
    id                    = "serveless-api-role"
    managed_policy_arns   = [
        "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
        "arn:aws:iam::aws:policy/CloudWatchFullAccess",
    ]
    max_session_duration  = 3600
    name                  = "serveless-api-role"
    path                  = "/"
}