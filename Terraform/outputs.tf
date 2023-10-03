output "resource-ids" {
  value = <<-EOT
  Environment ID:   ${confluent_environment.staging.id}
  Kafka Cluster ID: ${confluent_kafka_cluster.cluster.id}

  Service Accounts and their Kafka API Keys (API Keys inherit the permissions granted to the owner):
  ${confluent_service_account.connectors.display_name}:                     ${confluent_service_account.connectors.id}
  ${confluent_service_account.connectors.display_name}'s Kafka API Key:     "${confluent_api_key.connector_keys.id}"
  ${confluent_service_account.connectors.display_name}'s Kafka API Secret:  "${confluent_api_key.connector_keys.secret}"
  EOT

  sensitive = true
}
