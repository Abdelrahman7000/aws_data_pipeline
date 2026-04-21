resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-etl-bucket-4312345"
  tags = {
    Name        = "etl-bucket"
  }
}

# Upload your PySpark script
resource "aws_s3_object" "my_bucket_script" {
  bucket = aws_s3_bucket.my_bucket.id
  key    = "scripts/run_pipeline.py"
  source = "${path.module}/../../emr-job/run_pipeline.py" #"./emr-job/run_pipeline.py"
  etag   = filemd5("${path.module}/../../emr-job/run_pipeline.py") #filemd5("./emr-job/run_pipeline.py") 
}

# Upload your Zip file (e.g., dependencies or extra modules)
resource "aws_s3_object" "my_bucket_zip_file" {
  bucket = aws_s3_bucket.my_bucket.id
  key    = "scripts/emr-job.zip"
  source = "${path.module}/../../emr-job.zip" #"./emr-job.zip"
  etag   = filemd5("${path.module}/../../emr-job.zip") #filemd5("./emr-job.zip")
}