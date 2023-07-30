Content of page retrieved from [here](https://www.youtube.com/watch?v=NGLMPz3kAUU.)

## Architecture
![Architecture](images/vault%20-%20architecture.png)


## New CRDs
| CRD | Description |
|---|---|
| VaultConnection | Provides config necessary for the Operator to connect to a single Vault server instance |
| VaultAuth | Provide configuration necessary for the Operator to authenticate to a single Vault server instance as specified in a VaultConnection Custom Resource |
| VaultStaticSecret | Provide config necessary for Operator to sync a single Vault static Secret to a single k8 secret. supported secrets engine - kv-v2, kv-v1 |
| VaultDynamicSecret | Provide config necessray for the operator to sync a single vault dynamic secret to a single k8 secret. supported secrets engine - db, aws, azure, gcpp |
| VaultPkiSecret | sync a single Vault pKI secret to a single k8 secret. supported secret engine - pki |


## Secret creation - Flow
![Flow](images/vault%20-%20secret%20creation%20flow.png)

## Secret update - Flow
![Update Flow](images/vault%20-%20secret%20update%20flow.png)

## Demo

