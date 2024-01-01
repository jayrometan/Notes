
#### CIS Benchmark
best practices for security e.g. open certain ports, limit sudo, only certain services are enabled, enable auditing, logging, etc
  
Download link - https://www.cisecurity.org/cis-benchmarks/#kubernetes

Tools for CIS benchmark for kubernetes
- kube-bench
- kubescape
- trivy (all in one - also by Aqua security who performs CIS benchmark)

Install kube-bench in /root directory
```
curl -L https://github.com/aquasecurity/kube-bench/releases/download/v0.4.0/kube-bench_0.4.0_linux_amd64.tar.gz -o kube-bench_0.4.0_linux_amd64.tar.gz
tar -xvf kube-bench_0.4.0_linux_amd64.tar.gz
 ./kube-bench --config-dir `pwd`/cfg --config `pwd`/cfg/config.yaml 
```

#### Kubernetes Security Primitives

First line of defence - controlling access to the API server itself

2 questions
- who can access the api server?
  - who can authenticate to the server? 
  - ldap/tokens/certs/svc account
- what can they do?
  - rbac authorization
  - ABAC uathorization
  - node authorization
  - webhook mode

All communication between the cluster is encrypted via TLS
- kube controller manager
- kube scheduler
- kubeproxy
- kubelet

Pods by default can access other pods within the same cluster
- can be restricted by NetworkPolicy

#### Authentication
This part is securing access to k8 cluster with authentication mechanisms for administrative reasons

Users
- no way to create users like "e.g. kubectl create user user1"
- how does kube-apiserver authenticate the user?
  - user/password in a static password file
  ```
  # user-details.csv
  password123,users123,u0001,g001
  password123,users124,u0002,g002

  # kube-apiserver.service need to add 
  --basic-auth-file=user-details.csv

  curl -v -k "endpoint" -u "users123:password123"
  ```
  - static token in a static token file
  ```
  xxxxtokenxxx,user123,u001,xxx
  ```
  - certificates
  - ldap/kerberoes


#### Service Accounts
- user account used by users
- service accounts used for machines

```
# Get service account
$ kubectl describe sa serivceaccount 

# Get secret of the service account
$ kubectl describe secret secret-sa

You can get the token and utilize it with CURL to get a rest call to the kubernetes API

```

**TokenRequestAPI**
- tokens that are issued by TokenRequestAPI are audience bound, time bound and object bound, hence are more secure

**v1.24 Kubernetes**
- service account creation does not automatically create a secret due to security concerns
  
```yaml
# if you need a token, can perform the following but token will expire
$ kubectl create token <name of service account> # token name must be name as serice account

# if don't want expiry
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
meteadata:
    name: mysecret
    annotations:
        kubernetes.io/service-account.name: dashboard-sa
```

#### TLS

How does browser know that the cert was signed by Digicert and not by someone who says that they are Digicert?

Public keys of all CAs are all built into the browser which uses the public key of the CA to ensure legitimacy of certificate that the CA signed them

The CA make use of proper ways to ensure that they sign certificates for valid people e.g. TXT record, call, etc

Some people have an internal CA server. Can install the public key of the CA server installed on all employees' desktop and browsers for security.

Kubernetes requires at least one CA for the cluster

![Alt text](images/2-certificate-overview.png)

```
# Generating certificate
## Generate key
openssl genrsa -out cak.ey 2048

## CSR
openssl req -new -key cak.key -sub"/CN-kUBERNETES-CA" -out ca.csr

## Sign certificate
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
```

Need to read up more?

#### Certificate Details / API

Registering a new user's cert and key to get her access into the cluster but with more users, this becomes hard to scale. We need to use the built in Certificate API

1. User can register their own key and sends out CSR to administrator
```yaml
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
name: jane
spec:
groups:
- system:authenticated
usages:
- digital signature
- key encipherment
- server auth
request: LS0tLS1CRUdJTiBDRVJUUyZQV0FURSBSRVFVVJNV0xHT1RVVFJ3d01lb3ZYTlhwZW
1D0V6R3JNOTTFTVRVRU0Q0T0libVYzTFhWelp
PYXSDnZ0PVtUEWRONTdUdWTSWZRFFQ9pB
UVB0RTY0FUKU01yanBob0ZVWU1KClCGXeuemcr
NnhjOSTVndrS2xwc0t4ckxneG0zZ1dxc3ZUVT0
41TXV0T1oZXZtTVVPRnBi # Base64 encoded of CSR
```
2. Administrator can review and approve request
3. Administrator share cert with user

```
$ kubectl get csr
$ kubectl certificate approve jane
$ kubectl get csr jane -o yaml # decode signed CSR and pass to user
```

Controller Manager = component that signs the certificates for us. It has CSR-APPROVING/CSR-SIGNING internal components
- you can see the controller manager yaml got the ca.crt 
```
spec:
containers:
- command:
- kube-controller-manager
- --address=127.0.0.1
- --cluster-signing-key-file=/etc/kubernetes/pki/ca.crt
- --controllers=*,bootstrapsigner,tokencleaner
- --kubeconfig=/etc/kubernetes/controller-manager.conf
- --leader-elect=true
- --root-ca-file=/etc/kubernetes/pki/ca.crt
- --service-account-private-key-file=/etc/kubernetes/pki/sa.key
- --use-service-account-credentials=true
```

#### Kubeconfig

Without kubeconfig, if we want to call the kube api server, we need to perform the following which is a pain. We use kubeconfig to replace this as it'll contain the certificates/tokens

```
# kubectl get pods
    --server xxx:6443
    --client-key admin.key
    --client-certificate admin.crt
    --certificate-authority ca.crt
```
Hey bud, gather 'round! Let's talk about the kubeconfig file, a crucial key in your Kubernetes kingdom. Think of it like a passport that grants you access to your cluster and lets you talk to all the cool stuff inside.

What does it do?

Imagine a bunch of castle gates guarding your Kubernetes cluster. Each gate leads to different resources, like pods, services, and deployments. Now, the kubeconfig file is like a master key that opens all these gates. It stores all the authentication and authorization information you need to interact with your cluster – things like usernames, passwords, tokens, and even the location of the API server.

Why is it awesome?

- Single source of truth: No more juggling multiple logins or scattered credentials. This file becomes your one-stop shop for cluster access.
- Flexibility: You can have different kubeconfig files for different contexts, like staging and production environments. This keeps things organized and secure.
- Version control: Treat your kubeconfig file like code! Version control it to track changes and roll back if something goes wrong.

ntegrating kubeconfig and DEX in Kubernetes opens up a whole new world of flexibility and security for managing authentication and authorization within your cluster. Here's how it all works:

Imagine the scenario:

You have Kubernetes, the bustling kingdom, secured by DEX, your trusty gatekeeper.

To access the kingdom's resources (pods, deployments, etc.), users need a passport – the kubeconfig file.

But how does DEX, the gatekeeper, verify these passports and grant access? That's where integration comes in.
Two main integration approaches:

1. OpenID Connect (OIDC):

DEX acts as an OpenID Connect provider, issuing tokens to users after successful authentication (e.g., via LDAP, GitHub, or social login).
- These tokens are then embedded in the kubeconfig file using tools like dex-k8s-authenticator.
- When users run kubectl commands, the kubeconfig file presents the token to the Kubernetes API server.
- DEX verifies the token and grants access based on the user's role and permissions defined in Kubernetes RBAC (Role-Based Access Control).

Benefits:

- Centralized authentication: Manage user identities and access from a single point in DEX.
- Secure authentication: Use multi-factor authentication (MFA) and other security features offered by DEX.
- Fine-grained access control: Define granular permissions for users within Kubernetes based on their roles and DEX attributes.
- Seamless user experience: Users log in once to DEX and gain access to the Kubernetes cluster without additional configuration.

##### Integration with KeyCloak

Integrating Keycloak with kubeconfig for Kubernetes cluster access can be another fantastic option, offering similar benefits to DEX but with its own unique twists. Here's how it works:

The Keycloak Setup:

- Keycloak acts as your central identity and access management (IAM) system, managing user identities, authentication (via social login, LDAP, etc.), and authorization policies.

- You can define fine-grained roles and permissions within Keycloak for users accessing your Kubernetes cluster.
Integration Methods:

1. OpenID Connect (OIDC):

- Similar to DEX, Keycloak acts as an OIDC provider, issuing tokens to authenticated users.
- These tokens are embedded in the kubeconfig file using tools like keycloak-operator or manually configured with the Keycloak provider configuration.
- The Kubernetes API server verifies the token with Keycloak and grants access based on the user's roles and permissions within Keycloak.

Benefits:

- Centralized IAM: Manage user identities, authentication, and authorization from a single source in Keycloak.
- Fine-grained access control: Define granular roles and permissions for Kubernetes access based on Keycloak user attributes.
- Seamless user experience: Single sign-on (SSO) allows users to log in once to Keycloak and access the Kubernetes cluster without further authentication.
- Multi-factor authentication (MFA): Enhance security by enforcing MFA for cluster access through Keycloak.
 
2. Client certificates:

- Keycloak can issue client certificates to service accounts used by applications within the cluster.
- These certificates are stored in Secrets within Kubernetes and referenced in the kubeconfig file of the application pod.
- The API server verifies the certificate against the Secret object to grant access to the application.

Benefits:

- Stronger security: Client certificates offer robust authentication compared to simple static tokens.
- Automatic certificate renewal: Keycloak can automatically renew certificates before they expire, simplifying maintenance.

3. JWT token exchange:

- This involves converting Keycloak JWT tokens (obtained via authentication) into Kubernetes authentication tokens using a dedicated bridge or proxy.
- The converted tokens are then used in the kubeconfig file for API server authorization.

Benefits:

- Leverages existing Keycloak authentication workflow and token issuance.
- Can be more lightweight compared to the full OIDC integration.

Choosing the best approach:

- Consider your security requirements: OIDC and client certificates offer stronger authentication than static tokens.
- Assess your userbase and complexity: OIDC and JWT token exchange are ideal for centralized user management and fine-grained access control.
- Evaluate existing infrastructure: Leverage your existing Keycloak setup and choose the integration method that best aligns with it.

Keycloak offers a powerful and flexible option for integrating IAM with your Kubernetes cluster through kubeconfig. Weigh the options and choose the approach that best meets your specific needs and security considerations.

##### Structure of KubeConfig File
1. Clusters
   - Development
   - Production
   - Google
2. Contexts
   - Marries Clusters/Users together, which user account access which cluster?
3. Users
    - Admin
    - Dev User
    - Prod User
```
$ kubectl config view
$ kubectl config view --kubeconfig=xxx=config
$ kubectl config current-context
$ kubectl config use-context nyz-core-prod
```
```yaml
apiVersion: v1
kind: Config
clusters:
- name: my-kube-playground
cluster:
certificate-authority: ca.crt
server: https://my-kube-playground:6443
contexts:
- name: my-kube-admin@my-kube-playground
context:
cluster: my-kube-playground
user: my-kube-admin
users:
- name: my-kube-admin
user:
client-certificate: admin.crt
client-key: admin.key
```

```yaml
apiVersion: v1
kind: Config
current-context: dev-user@google # We can change this via cLI
clusters:
- name: my-kube-playground
(values hidden...)
- name: development
- name: production
- name: google
contexts:
- name: my-kube-admin@my-kube-playground
- name: dev-user@google
- name: prod-user@production
users:
- name: my-kube-admin
- name: admin
- name: dev-user
- name: prod-user
```


```yaml
# What about namespaces?
# can specify namespace in the contexts part in the kubeconfig file
apiVersion: v1
kind: Config
clusters:
- name: production
cluster-authority: /etc/kubernetes/pki/ca.crt #Specify certificate
server: https://172.17.0.51:6443
contexts:
- name: admin@production
context:
cluster: production
user: admin
namespace: finance # Specify namespace
users:
- name: admin
client-certificate: /etc/kubernetes/pki/users/admin.crt
client-key: /etc/kubernetes/pki/users/admin.key
```

#### API Groups

#### AuthorizatioN

#### RBAC

#### CLUSTER ROLES AND ROLE BINDINGS

#### KUBELET SECURITY

#### KUBECTL PROXY + PORT FORWARD

#### KUBERNETES DASHBOARD

#### SECURING KUBERNETES DASHBOARD

#### VERIFY PLATFORM BINARIES

#### KUBERNETES SOFTWARE VERSIONS

#### CLUSTER UPGRADE

#### NETWORK POLICIES

#### DEVELOPING NETWORK POLICIES

#### INGRESS

#### DOCKER

#### SECURING CONTROL PLANE