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
- Log collector deamons

For best results also deploy the operators

- Pulsar
- OTel
-
