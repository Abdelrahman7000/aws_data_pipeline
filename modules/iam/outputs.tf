 output "emr_service_role_arn" {
  value = aws_iam_role.emr_service_role.arn
}

output "emr_instance_profile_arn" {
  value = aws_iam_instance_profile.emr_instance_profile.arn
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_s3_role.arn
}