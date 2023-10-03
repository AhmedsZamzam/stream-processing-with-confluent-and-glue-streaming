import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from awsglue.job import Job
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StringType, StructField, StructType

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


# Write the data back to Kafka
query: StreamingQuery = kafka_source_df \
    .writeStream \
    .format("kafka") \
    .outputMode("append") \
    .option("topic", args['cc_target_topic']) \
    .options(**kafka_params) \
    .trigger(processingTime="10 seconds")  # Adjust the trigger interval as needed

query.start().awaitTermination()

