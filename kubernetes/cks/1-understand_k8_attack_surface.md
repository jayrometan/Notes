### The Attack
Demo of how an individual hack into a container, escape container to get access to the underlying host as root. Access the database etc to tune the results

### The 4C's of Cloud Native Security

- Cloud
  - firewalls
  - security of the infrastructure hosting the servers (cloud/colo)
- Cluster
  - able to go into Docker container with privileged perms
  - dashboard no need for authorization
  - network policies / security + ingress
  - authentication
  - authorization
  - admission
- Container
  - restrict images
  - supply chain
  - sandboxing
  - privileged
- Code
  - hardcoding credentials
  - no mTLS
  - secrets/vault