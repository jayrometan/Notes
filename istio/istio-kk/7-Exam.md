### Mock Exam

#### Istio installation, upgrade and configuration
---
1. Create an IstioOperator resource you can use to deploy Istio with the following configuration:

Two ingress gateways: 
- "payments-ingress", deployed to the “payments” namespace
- “frontend-ingress”, deployed to the “frontend” namespace

Single egress gateway:

- “cluster-egress”, deployed  to the “egress” namespace

Also update the Pilot component and set the CPU requests to 750m and memory to 4096Mi 

```yaml
$ kubectl create namespace istio-operator
$ helm install istio-operator manifests/charts/istio-operator\
 -n istio-operator

$ kubectl apply -f - <<EOF
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
  name: istio-controlplane
spec:
  components:
    pilot:
      k8s:
        resources:
          requests:
            memory: 4096Mi
            cpu: 750m
    egressGateways:
    - name: cluster-egress
      enabled: true
      namespace: egress
    ingressGateways:
    - name: payments-ingress
      enabled: true
      namespace: payments
    - name: frontend-ingress
      enabled: true
      namespace: frontend
EOF
```

---

#### Traffic Management

You’re given access to the Kubernetes cluster with Istio installed. Two workloads are running in the default namespace: payments and frontend. Both workloads have corresponding Kubernetes services wit the same name. 

You want to expose both services through the ingress gateway in the following way:

“payments” should be accessible on: “mycompany.com/payments”

“frontend” should be accessible on: “mycompany.com”

Create a Gateway and VirtualService resource to expose the services.

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: default-gateway
spec:
  selector:
    app: istio-ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "mycompany.com"

apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: default-virtualservice
spec:
  hosts:
  - "mycompany.com"
  gateways:
  - "default-gateway"
  http:
  - match:
    - uri:
        exact: /
    route:
    - destination:
        host: frontend
        port: 
          number: 80
  - match:
    - uri:
        prefix: /payments
    route:
    - destination:
        host: payment
        port:
          number: 80

```

---

Two versions of a workload are running inside the cluster - “orders-v1” and “orders-v2”. A Kubernetes Service resource also uses “app: orders” in its label selector; both deployments use the version label either set to v1 or v2.


You’ve been asked to configure a 30-70 traffic split where 30% of the traffic goes to “orders-v1” and 70% goes to “orders-v2”.

Create the VirtualService and DestinationRule resources.

---

Create a VirtualService that injects delays and faults for the “backend” for these cases:

A 5-second delay whenever a request is made to “backend.default.svc.cluster.local/delay”

An HTTP 403 response whenever a request is made to “backend.default.svc.cluster.local/fault”  

---

#### Securing Workloads

You want to configure a strict mTLS policy for all workloads in the default namespace with the label “mtls: strict” set. Additionally, you want to disable mTLS for port 9000 (on the same set of workloads). Create a resource that configures these settings.

--- 

Write an authorization policy that does the following:

The policy applies to workloads with the label “app: customers” in the “default” namespace

The policy allows access either from a principal called “cluster.local/ns/default/sa/payments” OR “cluster.local/ns/default/sa/orders”.

Access is only allow for the GET operations to “/api” path.

---

Write an authorization policy that denies access between all workloads in the namespace called “payments”

---