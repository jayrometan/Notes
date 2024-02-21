link - https://www.youtube.com/watch?v=kUXexTc9kHU


Why multiple clusters?
- Geographical separation
  - Front faced by GEO LB
- Logical seperation driven by security reasons
  - Cluster per project
- Logical separation driven by functionality reasons
  - Cluster per team -> good, another team prefer nginx as lb, service mesh, etc
  - Different teams = different best practices

If we use different cloud providers e.g. GKE/EKS, ECS. The challenges are
- different hosted kubernets provider = different authenticaiton
- authentication strategy on a hosted provider can't be changed
- configuring RBAC for the same user across clusters

We need a sysetm to manage multiple kubernetes clusters across different cloud
- goal to build an authentication/authorization management system, that is
  - open source
  - extend kubernetes api via CRD
  - logic implemented as custom controller

Cross Cluster Authentication with Rancher
- configure authentication only once, not with every cluster
- All requests to the clusters will go through RMC which will verify with the auth provider (e.g. ldap)

Global role -> Cluster role -> Project Role -> Namespace Role