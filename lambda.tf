data "aws_iam_role" "existing_lambda_role" {
  name = "lambda_write_s3_role"
}

# 5. The Lambda Layer for 'requests' library
# Note: You must have a folder 'python/requests' zipped as 'requests_layer.zip'
resource "aws_lambda_layer_version" "requests_layer" {
  filename   = "requests_layer.zip"
  layer_name = "requests_library"

  compatible_runtimes = ["python3.9"]
}


resource "aws_lambda_function" "lambda_extract" {
  filename      = "lambda_function_payload.zip" # This is your zipped python code
  function_name = "on_prem_sql_to_s3"
  role          = data.aws_iam_role.existing_lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  
  # Upgraded settings for 50,000 rows
  timeout      = 300  # 5 minutes
  memory_size  = 512  # Half a GB to handle JSON parsing safely

  environment {
    variables = {
      BASE_API_URL = "https://names-betty-tea-newcastle.trycloudflare.com"
      BUCKET_NAME  = aws_s3_bucket.my_bucket.id
    }
  }

  # Link the 'requests' library layer
  layers = [aws_lambda_layer_version.requests_layer.arn]
}

