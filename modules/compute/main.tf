# create the lambda function and its dependencies

# # create a new IAM role for Lambda with S3 access
# resource "aws_iam_role" "lambda_s3_role" {
#   name = "lambda_write_to_s3_role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect = "Allow"
#         Principal = {
#           Service = "lambda.amazonaws.com"
#         }
#         Action = "sts:AssumeRole"
#       }
#     ]
#   })
# }
# # Attach the AmazonS3FullAccess policy to the Lambda role
# resource "aws_iam_role_policy_attachment" "s3_full_access" {
#   role       = aws_iam_role.lambda_s3_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
# }

# 5. The Lambda Layer for 'requests' library
# Note: You must have a folder 'python/requests' zipped as 'requests_layer.zip'
resource "aws_lambda_layer_version" "requests_layer" {
  filename   = "${path.module}/requests_layer.zip" #"requests_layer.zip"
  layer_name = "requests_library"

  compatible_runtimes = ["python3.9"]
}

  
resource "aws_lambda_function" "lambda_extract" {
  filename      = "${path.module}/lambda_function_payload.zip" #"lambda_function_payload.zip" # This is your zipped python code
  function_name = "on_prem_sql_to_s3"
  role          = var.lambda_role_arn #aws_iam_role.lambda_s3_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  
  
  timeout      = 300  
  memory_size  = 512  

  environment {
    variables = {
      BASE_API_URL = "https://crystal-begins-casey-manga.trycloudflare.com"
      BUCKET_NAME  = var.bucket_name #aws_s3_bucket.my_bucket.id
    }
  }

  # Link the 'requests' library layer
  layers = [aws_lambda_layer_version.requests_layer.arn]
}

 

################################################################
# create an EMR cluster to run Spark jobs for transformation and loading to Redshift

resource "aws_emr_cluster" "emr_cluster" {
  name          = "emr-cluster"
  release_label = "emr-7.13.0"
  applications  = ["Spark", "Hadoop", "Hive", "Livy", "JupyterEnterpriseGateway"]

  service_role = var.service_role_arn #aws_iam_role.emr_service_role.arn

  ec2_attributes {
    instance_profile = var.instance_profile_arn #aws_iam_instance_profile.emr_instance_profile.arn

    subnet_id                         = var.subnet_id #aws_subnet.public_subnet.id
    emr_managed_master_security_group = var.master_sg #aws_security_group.public_sg.id
    emr_managed_slave_security_group  = var.core_sg #aws_security_group.public_sg_2.id

    # key_name = "your-keypair"
  }

  log_uri = "s3://aws-logs-824308981579-us-east-1/elasticmapreduce"

  master_instance_group {
    instance_type  = "m4.large"
    instance_count = 1
  }

  core_instance_group {
    instance_type  = "m4.large"
    instance_count = 1
  }

  ebs_root_volume_size = 15

  configurations_json = jsonencode([
    {
      Classification = "spark-hive-site"
      Properties = {
        "hive.metastore.client.factory.class" = "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
      }
    },
    {
      Classification = "hive-site"
      Properties = {
        "hive.metastore.client.factory.class" = "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
      }
    }
  ])

  keep_job_flow_alive_when_no_steps = true
}

# Add a task instance group to the EMR cluster
resource "aws_emr_instance_group" "task" {
  cluster_id     = aws_emr_cluster.emr_cluster.id
  instance_count = 1
  instance_type  = "m4.large"
  name           = "my little instance group"
}