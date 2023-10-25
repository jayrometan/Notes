Content of page retrieved from [here](https://www.youtube.com/watch?v=NGLMPz3kAUU.)

# Authentication Method

### App role
AppRole in HashiCorp Vault is an authentication method for machine and service accounts. It allows applications to obtain tokens to access Vault secrets without requiring human intervention. AppRole is a good choice for applications that need to access Vault secrets on a regular basis, such as web servers, database servers, and CI/CD pipelines.

To use AppRole, an administrator must first create a role and assign it policies that determine which secrets the application can access. The administrator then provides the application with the role ID and secret ID. The application can then use these credentials to authenticate with Vault and obtain a token.

AppRole is a flexible authentication method that can be used to support a variety of workflows. For example, AppRole can be used to:

- Authenticate applications that are running on different machines.
- Authenticate applications that are dynamically scaled up or down.
- Authenticate applications that are running in a containerized environment.


AppRole is also a secure authentication method. The role ID and secret ID can be rotated regularly to reduce the risk of compromise. Additionally, AppRole can be used with other security features, such as IP address restrictions and client certificates, to further protect Vault secrets.

Here are some of the benefits of using AppRole in HashiCorp Vault:

- Security: AppRole provides a secure way for applications to authenticate with Vault and obtain tokens. The role ID and secret ID can be rotated regularly to reduce the risk of compromise. Additionally, AppRole can be used with other security features, such as IP address restrictions and client certificates, to further protect Vault secrets.
- Flexibility: AppRole is a flexible authentication method that can be used to support a variety of workflows. For example, AppRole can be used to authenticate applications that are running on different machines, dynamically scaled up or down, or running in a containerized environment.
- Ease of use: AppRole is easy to use for both administrators and application developers. Administrators can create roles and assign policies using the Vault CLI or UI. Application developers can use the role ID and secret ID to authenticate with Vault and obtain a token from their application code.


Basically
- enable AppRole auth method
` vault auth enable approle`
`Success! Enabled app role auth method at: approle/`
- create new role
` vault write auth/approle/role/bryan policies=bryan token_ttl=60m`
`Success! Data written to: auth/approle/role/bryan`
- get roleid for that role
` vault list auth/approle/role`
` vault read auth/approle/role/bryan/role-id`
` role_id 2d7xxx42`
- generate secret id for that role (like generate a key) - will be different every time you generate this
` vault write -force auth/approle/role/bryan/secret-id`
` secret_id fe323f09-xxx-6c`
- pass roleid + secretid to vault and get the token to authenticate to activities permitted by that role
` vault write auth/approle/login role_id=2d7xxx42 secret_id=fe323f09-xxxx-6c`