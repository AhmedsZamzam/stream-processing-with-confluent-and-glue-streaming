variable "confluent_cloud_api_key" {
  description = "Confluent Cloud API Key (also referred as Cloud API ID)."
  type        = string
}

variable "confluent_cloud_api_secret" {
  description = "Confluent Cloud API Secret."
  type        = string
  sensitive   = true
}

variable "region" {
  description = "The region of Confluent Cloud Network."
  type        = string
}

variable "s3_bucket" {
  description = "S3 Bucket name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC Cidr to be created"
  type        = string
}

variable "confluent_source_topic_name" {
  description = "Topic name for demo"
  type        = string
}


variable "confluent_output_topic_name" {
  description = "Topic name for demo"
  type        = string
}




