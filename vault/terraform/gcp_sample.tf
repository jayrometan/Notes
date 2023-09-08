# https://cloud.google.com/kms/docs/key-import#key_import_flow
# https://discuss.hashicorp.com/t/switching-to-different-aws-kms-key-id-with-the-same-key-material/19116/5
#https://github.com/hashicorp/vault/issues/6046


# Configure the Google Cloud provider
provider "google" {
  credentials = file(var.account_file_path)
  project     = var.gcloud-project
  region      = var.gcloud-region
}

# Create a service account for Vault
resource "google_service_account" "vault" {
  account_id   = "vault"
  display_name = "Vault Service Account"
}

# Grant the service account the Cloud KMS IAM role
resource "google_project_iam_member" "vault_kms" {
  role   = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member = "serviceAccount:${google_service_account.vault.email}"
}

# Create a key ring for Vault
resource "google_kms_key_ring" "vault" {
  name     = "vault"
  location = var.gcloud-region
}

# Create a crypto key for Vault
resource "google_kms_crypto_key" "vault_init" {
  name            = "vault-init"
  key_ring        = google_kms_key_ring.vault.self_link
  rotation_period = "7776000s" # 90 days
}

# Create a compute instance for Vault
resource "google_compute_instance" "vault" {
  name         = "vault"
  machine_type = var.machine_type
  zone         = var.gcloud-zone

  boot_disk {
    initialize_params {
      image = var.image
    }
  }

  network_interface {
    network = var.network
    access_config {
      # Ephemeral IP
    }
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash

    # Download and install Vault
    curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
    sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
    sudo apt-get update && sudo apt-get install vault

    # Create Vault config file with GCP auto unseal settings
    cat <<EOF > /etc/vault.d/vault.hcl
    storage "file" {
      path = "/opt/vault/data"
    }

    listener "tcp" {
      address     = "0.0.0.0:8200"
      tls_disable = true
    }

    seal "gcpckms" {
      project     = "${var.gcloud-project}"
      region      = "${var.gcloud-region}"
      key_ring    = "${google_kms_key_ring.vault.name}"
      crypto_key  = "${google_kms_crypto_key.vault_init.name}"
    }
    EOF

    # Start Vault service
    sudo systemctl enable vault
    sudo systemctl start vault

    # Export Vault address and token environment variables
    export VAULT_ADDR=http://127.0.0.1:8200
    export VAULT_TOKEN=$(sudo vault operator init -key-shares=1 -key-threshold=1 -format=json | jq -r '.root_token')

    # Enable userpass auth method and create a user with policy to manage secrets
    sudo vault auth enable userpass
    sudo vault policy write my-policy -<<EOF
    path "*" {
      capabilities = ["create", "read", "update", "delete", "list"]
    }
    EOF

    sudo vault write auth/userpass/users/my-user password=my-password policies=my-policy

    # Enable kv-v2 secrets engine and write some secrets
    sudo vault secrets enable -version=2 kv-v2
    sudo vault kv put kv-v2/my-secret foo=bar baz=qux

  EOF

  service_account {
    email  = google_service_account.vault.email
    scopes = ["cloud-platform"]
  }

}

