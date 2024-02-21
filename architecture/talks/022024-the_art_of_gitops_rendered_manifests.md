https://www.youtube.com/watch?v=_WvOlo8t7fs

Importance of maintaining the distinction between the GitOps repo's source of truth and the Kubernetes cluster state. 

Problem
- GitOps Controller (e.g. ArgoCD) renders manifests before applying
- Change to a HelmChart or Kustomization Base changes the abstraction (impact unnknown)
- The desired state is actually the rendered manifest
- e.g. when you update the dependent chart version, you don't know the impact
  
YOU SHOULDN'T MUTATE YOUR SOURCE OF TRUTH RIGHT BEFORE IT GETS APPLIED

The rendered manifest pattern is proposed as a solution, where rendered manifests are stored in Git instead of config management tool artifacts, resulting in
- improved visibility into desired state
- issues will happen in CI and not at runtime
- reducing immutable state risks
- improving performance of the gitops controller

The use of rendered manifests, however, also introduces complexity to CI systems and may result in the loss of functionality with certain tools. New tools like Cargo Rendera are emerging to address the challenges of manifest management and notionally, the future of storing and securing manifests lies with Open Container Initiative (OCI).

While config management tools can be helpful, they abstract the configuration in a way that can lead to unintended consequences. Specifically, when using tools like Helm or Kustomize, the true desired state for a Kubernetes cluster is the manifest that is rendered by these tools, not the original chart or configuration.

These renderings happen at deploy time (ArgoCD), leading to potential issues if outdated or deprecated features are used. Hernandez encourages organizations to adopt a clear understanding of the renders and their implications in their GitOps workflow.

Solution =  "rendered manifest pattern"

Tmain branch of the GitOps repo will result in the Manifest getting rendered by the CI workflow and stored as is in Git. Environment-specific branches are then used to deploy onto the Kubernetes cluster, providing a direct mapping between the desired state in the Git repo and the state of the cluster. The speaker clarifies that this doesn't mean abandoning branches altogether for environments but rather avoiding the use of Git flow for promotion between environments. Instead, the content of these branches is maintained by an automated workflow, making it akin to a release bundle containing plainly rendered manifests for a desired state of an environment.


Advantages
By storing rendered manifests instead of artifacts,
-  users gain improved visibility into the desired state
-  eliminate authentication risks introduced by config management tooling
-  reduce risks with immutable desired state
-  improve performance by eliminating the need for manifest rendering by the controller.

Particularly with tools like Argo CD, there is a significant performance boost. The example given illustrates the difference between observing a change in an umbrella chart without rendered manifests versus with them - in the latter case, users have a clear understanding of the impact of the change on their environment and can make informed decisions.

Disadvantage
- added complexity to CI systems
- loss of functionality with certain tools like sealed secrets
- and the need to work around limitations with Argo CD.

Overall, the decision to use rendered manifests should be weighed against the specific use case and required functionality.


Benefits and challenges of using rendered manifests. Rendered manifests involve injecting the application name into the configuration to differentiate it between environments. However, this approach comes with the drawback of losing that differentiation if the manifests are not properly managed. To mitigate this issue, new tools like Cargo Rendera, a part of the Cargo ecosystem, have emerged. Cargo Rendera can be used standalone without adopting Cargo and is still in alpha. There's also a GitHub action available that can be used to render manifests without having to complicate CI. The speaker encourages the audience to try out Cargo Rendera and learn more about this tool and the ACU community, which is working on open-source projects related to manifests and OCI (Open Container Initiative). The speaker expresses his opinion that GitOps has outgrown Git and that OCI is the future for storing and securing manifests, treating them as artifacts rather than using Git for version control.