"""
The builder reads metadata from a target repo and generates app manifests which are posted back to a branch on the target
the source is configured to have Argo what for apps
in this case we use APIN as the source and target

application-sets folders is auto generated by creating Argo Applications with the correct settings and values
you can test this app in isolation 
someone needs to bootstrap the application set

"""


def process(path, config, sha, **kwargs):
    """
    take the options and generate the manifest files
    run kustomize to tag the thing

    """
    pass
