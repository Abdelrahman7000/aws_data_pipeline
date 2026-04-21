
# IAM Role for Lambda to write to S3 
resource "aws_iam_role" "lambda_s3_role" {
  name = "lambda_write_to_s3_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}
# Attach the AmazonS3FullAccess policy to the Lambda role
resource "aws_iam_role_policy_attachment" "s3_full_access" {
  role       = aws_iam_role.lambda_s3_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

 
#####################################################
# EMR Service Role with necessary permissions
resource "aws_iam_role" "emr_service_role" {
  name = "emr-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "elasticmapreduce.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}
 
resource "aws_iam_role_policy_attachment" "emr_service_ec2_full" {
  role       = aws_iam_role.emr_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_role_policy_attachment" "emr_service_emr_policy" {
  role       = aws_iam_role.emr_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEMRServicePolicy_v2"
}

resource "aws_iam_role_policy_attachment" "emr_service_s3_full" {
  role       = aws_iam_role.emr_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# resource "aws_iam_role_policy" "emr_passrole" {
#   name = "emr-masterclass-temp-passrole"
#   role = aws_iam_role.emr_service_role.id

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Sid    = "Statement1",
#         Effect = "Allow",
#         Action = "iam:PassRole",
#         Resource = "arn:aws:iam::824308981579:role/service-role/AmazonEMR-*"
#       }
#     ]
#   })
# }
resource "aws_iam_role_policy" "emr_passrole" {
  name = "emr-passrole"
  role = aws_iam_role.emr_service_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "iam:PassRole",
        Resource = aws_iam_role.emr_ec2_role.arn
      }
    ]
  })
}

#######################################################################
# EC2 Instance Profile Role for EMR Cluster
resource "aws_iam_role" "emr_ec2_role" {
  name = "emr-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# resource "aws_iam_role_policy_attachment" "emr_ec2_s3_full" {
#   role       = aws_iam_role.emr_ec2_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
# }

# resource "aws_iam_role_policy" "emr_ec2_custom_policy" {
#   name = "AmazonEMR-InstanceProfile-Policy"
#   role = aws_iam_role.emr_ec2_role.id

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Action = [
#           "s3:AbortMultipartUpload",
#           "s3:CreateBucket",
#           "s3:DeleteObject",
#           "s3:ListBucket",
#           "s3:ListBucketMultipartUploads",
#           "s3:ListBucketVersions",
#           "s3:ListMultipartUploadParts",
#           "s3:PutBucketVersioning",
#           "s3:PutObject",
#           "s3:PutObjectTagging"
#         ],
#         Resource = [
#           "arn:aws:s3:::aws-logs-824308981579-us-east-1/elasticmapreduce",
#           "arn:aws:s3:::aws-logs-824308981579-us-east-1/elasticmapreduce/*"
#         ]
#       },
#       {
#         Effect = "Allow",
#         Action = [
#           "s3:GetBucketVersioning",
#           "s3:GetObject",
#           "s3:GetObjectTagging",
#           "s3:GetObjectVersion",
#           "s3:ListBucket",
#           "s3:ListBucketMultipartUploads",
#           "s3:ListBucketVersions",
#           "s3:ListMultipartUploadParts"
#         ],
#         Resource = [
#           "arn:aws:s3:::aws-logs-824308981579-us-east-1/elasticmapreduce",
#           "arn:aws:s3:::elasticmapreduce",
#           "arn:aws:s3:::aws-logs-824308981579-us-east-1/elasticmapreduce/*",
#           "arn:aws:s3:::elasticmapreduce/*",
#           "arn:aws:s3:::*.elasticmapreduce/*"
#         ]
#       }
#     ]
#   })
# }
resource "aws_iam_role_policy_attachment" "emr_ec2_policy" {
  role       = aws_iam_role.emr_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
}

resource "aws_iam_instance_profile" "emr_instance_profile" {
  name = "emr-instance-profile"
  role = aws_iam_role.emr_ec2_role.name
}
