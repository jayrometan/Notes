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

### Gateway vs Virtual Service
Gateway:
- Purpose: It defines an entry point for traffic into or out of the mesh. It specifies the ports on which the gateway listens and the backend services to which it can forward traffic.
- Scope: It applies to a specific set of ports and can be defined at the global or namespace level.
- Configuration: It defines the properties of the load balancer, such as the type of load balancing algorithm and the port where the service is running.

VirtualService:
- Purpose: It defines how traffic is routed within the mesh. It can be used to route traffic to different versions of a service, perform load balancing, or implement traffic shaping and security policies.
- Scope: It applies to a specific set of hostnames and can be targeted at specific gateways or sidecars.
- Configuration: It defines the routing rules, including the destination services, weight distribution, and any additional transformations or modifications to be applied to the traffic.

Relationship Summary:
- Gateways act as the doors to the mesh, providing entry and exit points for traffic.
- VirtualServices act as the traffic controllers, directing traffic to the appropriate destinations within the mesh.
- Multiple VirtualServices can be bound to a single Gateway, enabling fine-grained control over traffic routing


Jerome
- Gateway will tell Istio to look out for a special hostname at a special port. Also, if you wanna handle TLS offloading.

```yaml
# The following example shows a possible gateway configuration for external HTTPS ingress traffic:

apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: ext-host-gwy
spec:
  selector:
    app: my-gateway-controller
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - ext-host.example.com
    tls:
      mode: SIMPLE
      credentialName: ext-host-cert

# This gateway configuration lets HTTPS traffic from ext-host.example.com into the mesh on port 443, but doesn’t specify any routing for the traffic.

# To specify routing and for the gateway to work as intended, you must also bind the gateway to a virtual service.
# You do this using the virtual service’s gateways field, as shown in the following example:

apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: virtual-svc
spec:
  hosts:
  - ext-host.example.com
  gateways:
  - ext-host-gwy

# You can then configure the virtual service with routing rules for the external traffic.

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

**Exam Simplifed**

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

**Links**
- https://learncloudnative.com/blog/2023-10-10-meshweek



### To update with YAMLs and stuff

**Istio Installation, Upgrade and Configuration (7%)**
  
1. Using the Istio CLI to install a basic cluster
```
$ istioctl install --set profile=demo -y
$ kubectl label namespace default istio-injection=enabled
namespace/default labeled
```
2. Customizing the Istio installation with the IstioOperator API
```
Installing via IstioOperator CLI (which is an API)
The istioctl command can be used to automatically deploy the Istio operator:

$ istioctl operator init

This command runs the operator by creating the following resources in the istio-operator namespace:

- The operator custom resource definition
- The operator controller deployment
- A service to access operator metrics
- Necessary Istio operator RBAC rules

You can configure which namespace the operator controller is installed in, the namespace(s) the operator watches, the installed Istio image sources and versions, and more.
For example, you can pass one or more namespaces to watch using the --watchedNamespaces flag:


$ istioctl operator init --watchedNamespaces=istio-namespace1,istio-namespace2

```

Installing it via helm
```


$ kubectl create namespace istio-operator
$ helm install istio-operator manifests/charts/istio-operator \
 --set watchedNamespaces="istio-namespace1\,istio-namespace2" \
 -n istio-operator

kubectl apply -f - <<EOF
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
  name: example-istiocontrolplane
spec:
  profile: demo
EOF

You can confirm the Istio control plane services have been deployed with the following commands:

$ kubectl get services -n istio-system
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)   AGE
istio-egressgateway    ClusterIP      10.96.65.145    <none>           ...       30s
istio-ingressgateway   LoadBalancer   10.96.189.244   192.168.11.156   ...       30s
istiod                 ClusterIP      10.96.189.20    <none>           ...       37s

$ kubectl get pods -n istio-system
NAME                                    READY   STATUS    RESTARTS   AGE
istio-egressgateway-696cccb5-m8ndk      1/1     Running   0          68s
istio-ingressgateway-86cb4b6795-9jlrk   1/1     Running   0          68s
istiod-b47586647-sf6sw                  1/1     Running   0          74s

Basically, this topic is just updating the IstioOperator helm chart e.g. to add a new user gateway 

apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  components:
    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
      - namespace: user-ingressgateway-ns
        name: ilb-gateway
        enabled: true
        k8s:
          resources:
            requests:
              cpu: 200m
          serviceAnnotations:
            cloud.google.com/load-balancer-type: "internal"
          service:
            ports:
            - port: 8060
              targetPort: 8060
              name: tcp-citadel-grpc-tls
            - port: 5353
              name: tcp-dns
```
3. Using overlays to manage Istio component settings

In Istio, overlaying refers to a specific mechanism for customizing the configuration of your Istio installation without directly modifying the generated manifests.

It allows you to add, modify, or delete resources while leveraging the base configuration provided by Istio itself.

Types of overlays:

- IstioOperator overlays: These are provided by the IstioOperator and allow you to modify components like Pilot, Citadel, and Envoy configurations.
- Custom overlays: You can create your own overlay files to customize any Istio resource based on your specific needs.

The following example overlay file adjusts the resources and horizontal pod autoscaling settings for Pilot
```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 1000m # override from default 500m
            memory: 4096Mi # ... default 2048Mi
        hpaSpec:
          maxReplicas: 10 # ... default 5
          minReplicas: 2  # ... default 1

$ istioctl install -f samples/operator/pilot-k8s.yaml
```

**Traffic Management (40%)**
- Controlling network traffic flows within a service mesh
- Configuring sidecar injection
- Using the Gateway resource to configure ingress and egress traffic
- Understanding how to use ServiceEntry resources for adding entries to internal service registry
- Define traffic policies using DestinationRule
- Configure traffic mirroring capabilities
  ```yaml
  Traffic mirroring, also called shadowing, is a powerful concept that allows feature teams to bring changes to production with as little risk as possible.
  Mirroring sends a copy of live traffic to a mirrored service. The mirrored traffic happens out of band of the critical request path for the primary service.

  apiVersion: networking.istio.io/v1alpha3
  kind: VirtualService
  metadata:
    name: httpbin
  spec:
    hosts:
      - httpbin
    http:
    - route:
      - destination:
          host: httpbin
          subset: v1
        weight: 100
      mirror:
        host: httpbin
        subset: v2
      mirrorPercentage:
        value: 100.0
  EOF

  This route rule sends 100% of the traffic to v1. The last stanza specifies that you want to mirror (i.e., also send) 100% of the same traffic to the httpbin:v2 service.
  
  When traffic gets mirrored, the requests are sent to the mirrored service with their Host/Authority headers appended with -shadow. For example, cluster-1 becomes cluster-1-shadow.
  ```

**Resilience and Fault Injection (20%)**
- Configuring circuit breakers (with or without outlier detection)
  ```
  Circuit breaking is an important pattern for creating resilient microservice applications.
  
  Circuit breaking allows you to write applications that limit the impact of failures, latency spikes, and other undesirable effects of network peculiarities.
  ```
- Using resilience features
  - Timeout
  - Retries + perTryTimeout
  - Circuit Breakers
    - ```yaml
      Circuit breakers are another useful mechanism Istio provides for creating resilient microservice-based applications.
      In a circuit breaker, you set limits for calls to individual hosts within a service, such as the number of concurrent connections or how many times calls to this host have failed.
      Once that limit has been reached the circuit breaker “trips” and stops further connections to that host. Using a circuit breaker pattern enables fast failure rather than clients trying to connect to an overloaded or failing host.

      As circuit breaking applies to “real” mesh destinations in a load balancing pool, you configure circuit breaker thresholds in destination rules, with the settings applying to each individual host in the service.
      The following example limits the number of concurrent connections for the reviews service workloads of the v1 subset to 100:

      apiVersion: networking.istio.io/v1alpha3
      kind: DestinationRule
      metadata:
        name: reviews
      spec:
        host: reviews
        subsets:
        - name: v1
          labels:
            version: v1
          trafficPolicy:
            connectionPool:
              tcp:
                maxConnections: 100
      ```
- Creating fault injection
  ```yaml
  After you’ve configured your network, including failure recovery policies, you can use Istio’s fault injection mechanisms to test the failure recovery capacity of your application as a whole.

  Fault injection is a testing method that introduces errors into a system to ensure that it can withstand and recover from error conditions.

  Using fault injection can be particularly useful to ensure that your failure recovery policies aren’t incompatible or too restrictive, potentially resulting in critical services being unavailable.

  You can inject two types of faults, both configured using a virtual service:

  1. Delays: Delays are timing failures.
  They mimic increased network latency or an overloaded upstream service.

  2. Aborts: Aborts are crash failures.
  They mimic failures in upstream services.
  Aborts usually manifest in the form of HTTP error codes or TCP connection failures.

  For example, this virtual service introduces a 5 second delay for 1 out of every 1000 requests to the ratings service.

  apiVersion: networking.istio.io/v1alpha3
  kind: VirtualService
  metadata:
    name: ratings
  spec:
    hosts:
    - ratings
    http:
    - fault:
        delay:
          percentage:
            value: 0.1
          fixedDelay: 5s
      route:
      - destination:
          host: ratings
          subset: v1

  ```

**Security Workloads (20%)**
- Understand Istio security features
- Set up Istio authorization for HTTP/TCP traffic in the mesh
- Configure mutual TLS at mesh, namespace, and workload levels
