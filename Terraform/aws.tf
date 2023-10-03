
# ------------------------------------------------------
# IAM Roles
# ------------------------------------------------------

resource "aws_iam_role" "glue_role" {
  name = "glue-demo-${random_id.env_display_id.hex}"
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"]  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "glue.amazonaws.com"
        }
      },
    ]
  })
}

# ------------------------------------------------------
# Glue  Job
# ------------------------------------------------------


resource "aws_glue_job" "glue_streaming" {
  name     = "glue-demo-gluestreaming"
  role_arn = aws_iam_role.glue_role.arn
  worker_type  = "G.1X"
  number_of_workers = "2"
  glue_version = "4.0"
  command {
    python_version = "3"
    script_location = "s3://${aws_s3_bucket.code_bucket.bucket}/glue_code/streaming.py"
  }
    default_arguments = {
    "--s3_bucket"  = aws_s3_bucket.code_bucket.bucket
    "--cc_target_topic" = confluent_kafka_topic.output_topic.topic_name
    "--cc_source_topic" = confluent_kafka_topic.input_topic.topic_name
    "--cc_bootstrap" = confluent_kafka_cluster.cluster.bootstrap_endpoint
    "--cc_secret"     = confluent_api_key.connector_keys.secret
    "--cc_key" = confluent_api_key.connector_keys.id
    "--enable-metrics"                   = "true"
  }
  provisioner "local-exec" {
    command = "aws glue start-job-run --job-name glue-demo-gluestreaming"
}
}


# ------------------------------------------------------
# Glue Code
# ------------------------------------------------------


resource "aws_s3_bucket" "code_bucket" {
  bucket = "aws-glue-${var.s3_bucket}"
  force_destroy = true
}

# Upload your code/script to the S3 bucket
resource "aws_s3_object" "code_object" {
  bucket       = aws_s3_bucket.code_bucket.id
  key          = "glue_code/streaming.py"
  source       = "streaming.py"
  etag         = filemd5("streaming.py")
  content_type = "text/plain"
}
