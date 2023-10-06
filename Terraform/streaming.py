import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from awsglue.job import Job
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType
from pyspark.sql.functions import col, from_json, to_json

## @params: [JOB_NAME]


args = getResolvedOptions(sys.argv, ['JOB_NAME','s3_bucket','cc_target_topic','cc_source_topic','cc_bootstrap','cc_secret','cc_key'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("KafkaToKafka") \
    .getOrCreate()
    
spark.conf.set("spark.sql.streaming.checkpointLocation","s3://"+args['s3_bucket']+"/scripts/")

# Kafka parameters for reading
kafka_params = {
    "kafka.bootstrap.servers": args['cc_bootstrap'],
    "kafka.security.protocol": "SASL_SSL",
    "kafka.sasl.jaas.config": 'org.apache.kafka.common.security.plain.PlainLoginModule required ' \
                            'username="'+args['cc_key']+'" ' \
                            'password="'+args['cc_secret']+'";',
    "kafka.sasl.mechanism": "PLAIN"
}

# Read data from Kafka
kafka_source_df = spark \
    .readStream \
    .format("kafka") \
    .option("subscribe", args['cc_source_topic']) \
    .options(**kafka_params) \
    .load()


# Define the updated JSON schema with the correct data types
json_schema = StructType([
    StructField("ordertime", TimestampType(), True),
    StructField("orderid", IntegerType(), True),
    StructField("itemid", StringType(), True),
    StructField("orderunits", DoubleType(), True),
    StructField("address", StructType([
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("zipcode", IntegerType(), True)
    ]), True)
])


# Parse the JSON data and create a DataFrame and Drop the "orderid"
parsed_df = kafka_source_df.selectExpr("CAST(value AS STRING)").\
    select(from_json(col("value"), json_schema).alias("data"))


# Select specific columns from the "data" struct, excluding "itemid"
parsed_df = parsed_df.select(
    col("data.ordertime").cast("timestamp").alias("ordertime"),
    col("data.orderid").cast("integer").alias("orderid"),
    col("data.orderunits").cast("double").alias("orderunits"),
    col("data.address").alias("address")
)


# Write the data back to Kafka
query: StreamingQuery = parsed_df.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .outputMode("append") \
    .option("topic", args['cc_target_topic']) \
    .options(**kafka_params) \
    .trigger(processingTime="10 seconds")  # Adjust the trigger interval as needed

query.start().awaitTermination()

