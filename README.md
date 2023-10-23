# app.pinnings

a different take on underpin

app'pinnings builds Kubernetes systems from any mono repo. It can be tested on itself

this is what happens

1. You push to main (any mono repo)
2. The build is packed
3. At the end we call apin service with changes (this service)
4. apin service pulls down the repo (any repo) and checks changes and builds a manifest change set
5. the manifests replaces the app-manifests in the configured branch (not main)
6. argo CD pulls the manifests

For free you get a few things on your stack

- A workflow runner
- Some default templates for apis and event consumers
- Observability stuff
- Log collector daemons

For best results also deploy the operators

- Pulsar
- OTel

## notes

- The service runs on a Docker image with Kustomize and other bits but everything else is packed with packer
-

```bash

```

## Stack

WE have

- init-  we add basic things such as ingress controllers, knative, karpenter and things like that
- we add argo tools as core stack
- application sets - these are flavours of deployments that are treated the same and easy to add from existing templates. the template can be anything. We generate it with LLM
  - services, deployments and workflows are examples
- we add operators via OLM
- we add observability
- we probably will add something like Pulsar

- read and write workflow perms

- sss
