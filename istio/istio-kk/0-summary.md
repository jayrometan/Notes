## Summary
---

## What is a service mesh?

In the world of microservices architecture, a service mesh is a dedicated infrastructure layer responsible for managing communication between services.
It acts like a virtual network that sits on top of the existing infrastructure and provides various functionalities, including:


#### Service discovery: Makes services aware of each other and enables dynamic routing.
- Traffic routing: Directs traffic between services based on defined rules and policies.
- Load balancing: Distributes traffic across multiple instances of a service for improved scalability and resilience.
- Security: Enforces encryption and authentication for secure communication between services.
- Monitoring and observability: Provides insights into service behavior and network traffic for troubleshooting and performance optimization.

#### Benefits of a Service Mesh:

- Simplified service communication: Abstracting communication logic from individual services, making them easier to develop and maintain.
- Enhanced resilience: Provides built-in features like retries, circuit breakers, and timeouts to handle failures gracefully.
- Improved security: Enforces security policies across the entire service mesh, reducing the risk of unauthorized access and data breaches.
- Increased scalability: Enables services to scale independently and efficiently.
- Improved observability: Provides comprehensive insights into service and network behavior for improved troubleshooting and performance optimization.

#### Solutions Provided by Service Mesh:

- Complexity of service communication: Service meshes handle communication details, freeing developers to focus on business logic.
- Network visibility and control: They provide a centralized view of all service interactions, allowing for better traffic management and security.
- Decoupling services and infrastructure: Services are no longer tightly coupled to the underlying network infrastructure, leading to greater flexibility and portability.
- Dynamic service configuration: Enables dynamic routing and policy enforcement based on real-time conditions.

#### Popular Service Mesh Solutions:

- Istio: An open-source service mesh offering a comprehensive set of features and functionalities.
- Linkerd: A lightweight and easy-to-use service mesh focused on simplicity and performance.
- Consul Connect: A service mesh solution built on top of the Consul service discovery platform.

---
### Key notes

#### Enabling Istio at a namespace level
- Must enable Istio sidecar injection at a namespace level if you would like Istio to inject proxy services as side cars to the applications deployed in a namespace
- each pod in that namespace will have one more container running inside

```
# To do this on a specific namespace
kubectl label namespace plat-default istio-injection=enabled

# If you want to disable, change enabled to disable.

```

#### Visualization
- Kiali dashboard is very helpful
- Prometheus/Grafana
- Jaeger
```
# Run kiali dashboard
istioctl dashboard kiali
```

#### CRDs

| CRD Name                              | Description                                                                                              | CRD Type    |
|---------------------------------------|----------------------------------------------------------------------------------------------------------|-------------|
| authorizationpolicies.security.istio.io | Manages access control policies to control traffic authorization within the mesh.                         | Security    |
| destinationrules.networking.istio.io  | Specifies traffic policies applied to specific destination services in the mesh.                           | Networking  |
| envoyfilters.networking.istio.io      | Allows users to customize Envoy proxy configuration and behavior in the mesh.                               | Networking  |
| gateways.networking.istio.io          | Defines a set of rules for allowing inbound or outbound traffic to enter or exit the mesh.                 | Networking  |
| istiooperators.install.istio.io       | Represents Istio control plane components and their configurations in a cluster.                            | Installation|
| peerauthentications.security.istio.io | Configures mutual TLS settings for service-to-service communication authentication and encryption.         | Security    |
| proxyconfigs.networking.istio.io     | Manages Envoy proxy configuration settings within the Istio service mesh.                                   | Networking  |
| requestauthentications.security.istio.io | Configures authentication policies for HTTP requests entering the mesh.                                   | Security    |
| serviceentries.networking.istio.io   | Defines how services can access external services outside the mesh and handles their traffic configurations.| Networking  |
| sidecars.networking.istio.io         | Configures settings for Envoy sidecar proxies handling network traffic within the Istio mesh.              | Networking  |
| telemetries.telemetry.istio.io       | Manages telemetry configurations and settings for monitoring and observability within Istio.               | Telemetry   |
| virtualservices.networking.istio.io | Defines rules for routing traffic to different versions of services in the Istio service mesh.             | Networking  |
| wasmplugins.extensions.istio.io      | Enables the use of WebAssembly (Wasm) plugins for extending Envoy's functionality in the Istio mesh.      | Extensions  |
| workloadentries.networking.istio.io | Specifies how workloads in the mesh can access external resources outside the mesh boundaries.             | Networking  |
| workloadgroups.networking.istio.io | Manages groups of workloads in the Istio service mesh, enabling applying policies to workload sets.       | Networking  |


#### Example CRD YAML Files

```yaml
# Defines an AuthorizationPolicy to allow traffic from a specific source service.
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: example-auth-policy
spec:
  selector:
    matchLabels:
      app: example-app
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/default"]

# Specifies traffic policies for routing to subsets of a destination service.
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: example-destination-rule
spec:
  host: example-service.default.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2

# Configures an EnvoyFilter to add custom headers to inbound requests for a specific app.
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: example-envoy-filter
spec:
  workloadSelector:
    labels:
      app: example-app
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_INBOUND
      listener:
        filterChain:
          filter:
            name: envoy.http_connection_manager
            subFilter:
              name: envoy.router
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.lua
        typed_config:
          "@type": "type.googleapis.com/envoy.config.filter.http.lua.v2.Lua"
          inlineCode: |
            function envoy_on_request(request_handle)
              request_handle:headers():add("example-header", "example-value")
            end

# Defines a Gateway to allow inbound traffic on port 80 for all hosts.
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: example-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"

# Represents Istio control plane components and their configurations in a cluster.
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: example-istio-operator
spec:
  profile: default
  components:
    base:
      enabled: true

# Configures mutual TLS settings for service-to-service communication authentication and encryption.
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: example-peer-authentication
spec:
  mtls:
    mode: STRICT

# Manages Envoy proxy configuration settings within the Istio service mesh.
apiVersion: networking.istio.io/v1alpha3
kind: ProxyConfig
metadata:
  name: example-proxy-config
spec:
  binaryPath: /usr/local/bin/envoy
  concurrency: 2
  configPath: /etc/envoy/envoy.yaml

# Configures authentication policies for HTTP requests entering the mesh.
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: example-request-authentication
spec:
  jwtRules:
  - issuer: "https://example-issuer.com"
    jwksUri: "https://example-issuer.com/.well-known/jwks.json"

# Defines how services access external services outside the mesh and handles their traffic configurations.
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: example-service-entry
spec:
  hosts:
  - example.com
  ports:
  - number: 80
    name: http
    protocol: HTTP
  resolution: DNS

# Configures settings for Envoy sidecar proxies handling network traffic within the Istio mesh.
apiVersion: networking.istio.io/v1alpha3
kind: Sidecar
metadata:
  name: example-sidecar
spec:
  egress:
  - hosts:
    - "*"
  ingress:
  - ignoredPorts:
    - 8080

# Manages telemetry configurations for monitoring and observability within Istio.
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: example-telemetry
spec:
  enabled: true
  resolution: 1s

# Defines rules for routing traffic to different versions of services in the Istio service mesh.
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: example-virtual-service
spec:
  hosts:
  - example-service.default.svc.cluster.local
  http:
  - route:
    - destination:
        host: example-v1
        subset: v1
      weight: 80
    - destination:
        host: example-v2
        subset: v2
      weight: 20

# Enables the use of WebAssembly (Wasm) plugins for extending Envoy's functionality in the Istio mesh.
apiVersion: extensions.istio.io/v1beta1
kind: WasmPlugin
metadata:
  name: example-wasm-plugin
spec:
  config: |-
    {}

# Specifies how workloads in the mesh access external resources outside the mesh boundaries.
apiVersion: networking.istio.io/v1alpha3
kind: WorkloadEntry
metadata:
  name: example-workload-entry
spec:
  address: 192.168.1.100
  labels:
    app: example-app

# Manages groups of workloads in the Istio service mesh, enabling applying policies to workload sets.
apiVersion: networking.istio.io/v1alpha3
kind: WorkloadGroup
metadata:
  name: example-workload-group
spec:
  metadata:
    app: example-app
  targets:
  - name: example-service
    ports:
    - number: 80
      protocol: HTTP

```

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

