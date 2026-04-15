
# resource "aws_glue_connection" "sql_server_on_prem" {
#   name = "on-prem-sql-server-connection"

#   connection_properties = {
#     JDBC_CONNECTION_URL = "jdbc:sqlserver://DESKTOP-NJ4MVFB:1433;databaseName=raw_data"
#     SECRET_ID           = "arn:aws:secretsmanager:us-east-1:824308981579:secret:on-prem-sql-server-m4p5Eu"
#     #JDBC_ENFORCE_SSL    = "false"
#   }

#   physical_connection_requirements {
#     availability_zone      = "us-east-1a"
#     security_group_id_list = [aws_security_group.glue_sg.id]
#     subnet_id              = aws_subnet.private_subnet.id
#   }
# }




##############################################################################
# resource "aws_glue_job" "sql_to_s3_ingestion" {
#   name     = "on-prem-sql-to-s3-staging"
#   role_arn = aws_iam_role.glue_service_role.arn

#   # The location of your PySpark or Python script in S3
#   command {
#     script_location = "s3://${aws_s3_bucket.staging.id}/scripts/ingest_script.py"
#     python_version  = "3"
#   }

#   connections = [aws_glue_connection.sql_server_on_prem.name]

#   default_arguments = {
#     "--job-language"        = "python"
#     "--TempDir"             = "s3://${aws_s3_bucket.staging.id}/temporary/"
#     "--staging_bucket_path" = "s3://${aws_s3_bucket.staging.id}/raw_data/"
#   }

#   glue_version      = "4.0"
#   worker_type       = "G.1X"
#   number_of_workers = 2
# }