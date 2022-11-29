resource "aws_dynamodb_table" "student-records" {
  name           = "student-records"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "studentId"

  attribute {
    name = "studentId"
    type = "S"
  }
  
  ttl {
    enabled        = false
  }
}