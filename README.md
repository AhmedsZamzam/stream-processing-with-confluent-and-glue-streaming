#  Stream Processing using Confluent with AWS Glue Streaming

[AWS Glue Streaming](https://docs.aws.amazon.com/glue/latest/dg/add-job-streaming.html) uses [Glue Connections](https://docs.aws.amazon.com/glue/latest/dg/glue-connections.html) to connect to different sources and targets. One of these conections is Kafka. However, this connection does not support SASL/PLAIN, a common authentication mechanism used by vanilla Kafka and Confluent. This limitation means that Glue Streaming does not natively support Confluent out-of-the-box.

An alternative solution would be using native Spark APIs to integrate AWS Glue Streaming with Confluent. This repository provides a simple demo and boilerplate code for Glue Streaming. It reads data from a Confluent Cloud topic and writes that data into another topic, with the only transformation being the removal of a specific column. This code serves as a foundation that you can build upon by adding your own custom transformations as needed.

We use Terraform to deploy all the necessary resources. The script deploys the following:

The template deploys:
1. Confluent Cloud environment
2. Confluent Cloud Cluster
3. Confluent Cloud source and target topics
4. API Keys with read/write permissions on the source and target topics
5. [Datagen Connector](https://docs.confluent.io/cloud/current/connectors/cc-datagen-source.html) to generate mock data for the demo
6. Glue Steaming Python code
7. S3 Bucket to upload the code 


```bash
├── assets                                <-- Directory that will hold demo assests
│   ├── architecture.png                  <-- Demo architecture diagram
└── Terraform                             <-- Demo terraform script and artifacts
│   ├── aws.tf                            <-- Terraform for AWS resources
│   ├── main.tf                           <-- Terraform for Confluent resources
│   ├── outputs.tf                        <-- Terraform output file
│   ├── providors.tf                      <-- Terraform providors file
│   ├── streaming.py                      <-- Glue Streaming code
│   ├── variables.tf                      <-- Terraform variables file
└── README.md
```
## Architecture

## General Requirements

* **Confluent Cloud API Keys** - (Cloud API Keys)[https://docs.confluent.io/cloud/current/access-management/authenticate/api-keys/api-keys.html#cloud-cloud-api-keys] with Organisation Admin permissions are needed to deploy the necessary Confluent resources.
* **Terraform (0.14+)** - The application is automatically created using [Terraform](https://www.terraform.io). Besides having Terraform installed locally, will need to provide your cloud provider credentials so Terraform can create and manage the resources for you.
* **AWS account** - This demo runs on AWS
* **AWS CLI** - Terraform script uses AWS CLI to manage AWS resources


## Deploy Demo

1. Clone the repo onto your local development machine using `git clone <repo url>`.
2. Change directory to demo repository and terraform directory.

```
cd stream-processing-with-confluent-and-glue-streaming/Terraform

```
3. Use Terraform CLI to deploy solution

```
terraform plan

terraform apply

```

## Post deployment

1. Go to [Confluent Cloud Topics UI](https://confluent.cloud/go/topics), then choose the newly created environment and cluster.
2. Browse to *source-topic* and view raw messages
3. Navigate to *target-topic* and then view post-processed messages. Notice the output messages are missing one column which was dropped by the Glue Steaming job.
4. Play with the Glue streaming code to add any transformations needed.


## Clean-up
The great thing about Cloud resources is that you can spin the up and down with few commands. Once you are finished with this demo, remember to destroy the resources you created, to avoid incurring in charges. You can always spin it up again anytime you want.

*Note:* When you are done with the demo, you can automatically destroy all the resources created using the command below:


```
terraform destroy
```
