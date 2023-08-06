# pykubeks
This is a fork of [pykube](https://github.com/kelproject/pykube) which
is no longer maintained.  If you are interested in who brought that
lovely little library into the world, please check out [The Kel Project](https://github.com/kelproject).

The reason for this fork is to release the AWS EKS support I wrote for
the original project, before it was abandoned.  The new name `pykubeks`
is a portmanteau of `pykube` and `EKS`.

The python package name is still the same to make it simpler to "upgrade"
to this new version which supports user credentials supplied from client-go
credential plugins.  See [k8s documentation](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#client-go-credential-plugins)
for details.

## Features

* HTTP interface using requests using kubeconfig for authentication
* Python native querying of Kubernetes API objects

## Installation

To install pykubeks, use pip:

    pip install pykubeks

## Usage

Query for all ready pods in a custom namespace:

```python
import operator
import pykube

api = pykube.HTTPClient(pykube.KubeConfig.from_file("/Users/<username>/.kube/config"))
pods = pykube.Pod.objects(api).filter(namespace="gondor-system")
ready_pods = filter(operator.attrgetter("ready"), pods)
```

Access any attribute of the Kubernetes object:

```python
pod = pykube.Pod.objects(api).filter(namespace="gondor-system").get(name="my-pod")
pod.obj["spec"]["containers"][0]["image"]
```

Selector query:

```python
pods = pykube.Pod.objects(api).filter(
    namespace="gondor-system",
    selector={"gondor.io/name__in": {"api-web", "api-worker"}},
)
pending_pods = pykube.objects.Pod.objects(api).filter(
    field_selector={"status.phase": "Pending"}
)
```

Watch query:

```python
watch = pykube.Job.objects(api, namespace="gondor-system")
watch = watch.filter(field_selector={"metadata.name": "my-job"}).watch()

# watch is a generator:
for watch_event in watch:
    print(watch_event.type) # 'ADDED', 'DELETED', 'MODIFIED'
    print(watch_event.object) # pykube.Job object
```

Create a ReplicationController:

```
obj = {
    "apiVersion": "v1",
    "kind": "ReplicationController",
    "metadata": {
        "name": "my-rc",
        "namespace": "gondor-system"
    },
    "spec": {
        "replicas": 3,
        "selector": {
            "app": "nginx"
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "nginx"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx",
                        "ports": [
                            {"containerPort": 80}
                        ]
                    }
                ]
            }
        }
    }
}
pykube.ReplicationController(api, obj).create()
```

Delete a ReplicationController:

```python
obj = {
    "apiVersion": "v1",
    "kind": "ReplicationController",
    "metadata": {
        "name": "my-rc",
        "namespace": "gondor-system"
    }
}
pykube.ReplicationController(api, obj).delete()
```

Check server version:

```python
api = pykube.HTTPClient(pykube.KubeConfig.from_file("/Users/<username>/.kube/config"))
api.version
```

## HTTPie

pykube can be used together with HTTPie for Kubernetes command line querying goodness. For example:

```
pip install httpie
http pykube://minikube/api/v1/services
```

The above example will construct an HTTP request to the cluster behind the ``minikube`` context and
show you the response containing all services.

## Requirements

* Python 2.7 or 3.3+
* requests (included in ``install_requires``)
* PyYAML (included in ``install_requires``)

## License

The code in this project is licensed under the Apache License, version 2.0
(included in this repository under LICENSE).


## Contributing

By making a contribution to this project, you are agreeing to the `Developer
Certificate of Origin v1.1` (also included in this repository under DCO.txt).

[Developer Certificate of Origin v1.1](http://developercertificate.org)


## Code of Conduct

[Contributor Covenant Code of Conduct](http://contributor-covenant.org/version/1/4/)


## Commercial Support

No commercial support is available for this project.

