### Platform Engineering
Delivering values fast - why don't we create VMs that are standby since resources already exist (on Vsphere level)

### Panic-ing when CVE drops
SBOM - software bill of material

Need to have an inventory of software so that when CVE drops, we know where to patch? -> Tenable can do this?

1. Know what you have
2. xxxx

GUAC - graphical xxx for security supply chain attacks


### GreenOps + Kelper + KDEDA
For sustainable use of Kubernetes,
- Kepler can calculate ur kubernetes resource usage - deployed as daemonset, count CPU cycle - ownself input the coal/oil/electricty coefficient
- KEDA carbon waste operator - to scale the applications based on the cardon intensity??? input x factor value (for instance, electricy * 0.8) = output

xx

### Distributed Tracing Integration with OpenTelemetry and Knative

Observability Pillars
- metrics
- logs
- traces (which line of code is failing, etc)

Open source for all parts of the monitoring chain
- Visualization
- Data Proecssing
- Data Collection
- Instrument

Besides open source software, have open standards for doing telemetry.

Old tracing projects combined to form OpenTelemtry
- OpenTracing 
- OpenCensus

OpenTelemtry Components
- Specification
  - Describes cross language requirements for all applications
- Instrumentation
  - make every library and application observable out of the box
- Collector

Tracing serverless applications
- example of serverless --> knative


### Kubernetees Security (to watch on youtube)

### Handling billions of metrics with prometheus and grafana

ArgoCD Live Metrics
- new extension in ArgoCD --> enable it? what release did this come out?

Prometheus Kafka Adapter?

### Arsenal Tools

image security: trivy. - light weight

falco, OPA, notary (signing of artifacts), kubebench

nova - notifies about updates for helm charts and container releases
pluto - notify about deprecation of apiversion? same as kubent

kubescape instead of kubebench?
- kubescape can integrate into CICD?

sealed secrets
kata containers

backstage


### ArgoCD Talk
- 10k+ ArgoCD Apps, 6000 repo, 60 proj

IDP

Service lifecycle
- 1 service contains 3-5 ArgoCD apps with diff lifecycle
- Istio Sidecar / Istio Gateway


Appset & App of apps pattern - monorepo

challenges of cetranlized argocd
- tunnels/peering
- mTLS
- slow recon & sync
  - workqueue_depth
  - argocd_app_reconcile_bucket metrics
- slow uI loading 
- repo server


Performance Tuning
- xxx


They are thinking of 

Decentralized ArgoCD
- one argocd for each cluster
- pros
  - xx
- cons
  - maintenance and upgrade headache e.g.
  - xx

agent based argocd (hybrid model) - popularized by Akuity platform


# multi cluster service mesh

# multi cloud self service

challenge
- would be great if user can do this in a self-service way
- good to have consolidated for multiple cloud providers
- fully secure and compliant

architecture
- landing zone
  - 
- pattern
- platform
- app deploy

self-service 

deliver cluster with csi drivers/cis benchmark/cert-manager/OPA gatekeeper

chain of custody
- how controls are being met during each stage of the pipeline
- e.g. before handover of the cluster, the cluster is CIS benchmark-ed