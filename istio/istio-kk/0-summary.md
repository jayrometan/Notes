Summary
- Must enable Istio sidecar injection at a namespace level if you would like Istio to inject proxy services as side cars to the applications deployed in a namespace

```
# To do this on a specific namespace
kubectl label namespace plat-default istio-injection=enabled

# If you want to disable, change enabled to disable.
```
- Kiali dashboard is very helpful
```
istioctl dashboard kiali
```

- Gateway / Virtual Service / Destination Rule - TODO: PUT YAML for each

authorizationpolicies.security.istio.io
destinationrules.networking.istio.io
envoyfilters.networking.istio.io
gateways.networking.istio.io
istiooperators.install.istio.io
peerauthentications.security.istio.io
proxyconfigs.networking.istio.io
requestauthentications.security.istio.io
serviceentries.networking.istio.io
sidecars.networking.istio.io
telemetries.telemetry.istio.io
virtualservices.networking.istio.io
wasmplugins.extensions.istio.io
workloadentries.networking.istio.io
workloadgroups.networking.istio.io

**Exam**

**Istio Installation, Upgrade and Configuration (7%)**
- Using the Istio CLI to install a basic cluster
- Customizing the Istio installation with the IstioOperator API
- Using overlays to manage Istio component settings

**Traffic Management (40%)**
- Controlling network traffic flows within a service mesh
- Configuring sidecar injection
- Using the Gateway resource to configure ingress and egress traffic
- Understanding how to use ServiceEntry resources for adding entries to internal service registry
- Define traffic policies using DestinationRule
- Configure traffic mirroring capabilities

**Resilience and Fault Injection (20%)**
- Configuring circuit breakers (with or without outlier detection)
- Using resilience features
- Creating fault injection

**Security Workloads (20%)**
- Understand Istio security features
- Set up Istio authorization for HTTP/TCP traffic in the mesh
- Configure mutual TLS at mesh, namespace, and workload levels

