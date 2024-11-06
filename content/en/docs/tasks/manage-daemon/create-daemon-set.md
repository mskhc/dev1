---
title: Building a Basic DaemonSet  
content_type: task  
weight: 30  
---
<!-- overview -->

This page demonstrates how to build a basic DaemonSet that runs a Pod on every node in a Kubernetes cluster. It covers a simple use case of mounting a file from the host, logging its contents using an init container, and utilizing a pause container.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

## Building a DaemonSet

In this task, you'll create a basic DaemonSet that mounts the `/etc/machine-id` file from each node, logs its contents using an init container, and runs a pause container.

### Step 1: Create the DaemonSet Manifest

Let's create a DaemonSet manifest that ensures one Pod is scheduled on every node. The Pod will use an init container to read and log the contents of `/etc/machine-id` from the host, while the main container will be a `pause` container, which keeps the Pod running.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: example-daemonset
spec:
  selector:
    matchLabels:
      app: example
  template:
    metadata:
      labels:
        app: example
    spec:
      containers:
name: pause
        image: gcr.io/google_containers/pause:3.1
        # This is the main container, which doesn't do much but keeps the Pod alive.
      initContainers:
name: log-machine-id
        image: busybox
        command: ['sh', '-c', 'cat /etc/machine-id > /var/log/machine-id.log']
        volumeMounts:
name: machine-id
          mountPath: /etc/machine-id
          readOnly: true
name: log-dir
          mountPath: /var/log
      volumes:
name: machine-id
        hostPath:
          path: /etc/machine-id
          type: File
name: log-dir
        hostPath:
          path: /var/log
```

### Step 2: Apply the DaemonSet

Apply the DaemonSet to your Kubernetes cluster by saving the manifest to a file (For example, `daemonset.yaml`) and using the following command:

```bash
kubectl apply -f daemonset.yaml
```

### Step 3: Verify the DaemonSet

Once applied, you can verify that the DaemonSet is running a Pod on every node in the cluster:

```bash
kubectl get pods -o wide
```

The output will list one Pod per node, similar to:

```
NAME                                READY   STATUS    RESTARTS   AGE    IP       NODE
example-daemonset-xxxxx             1/1     Running   0          5m     x.x.x.x  node-1
example-daemonset-yyyyy             1/1     Running   0          5m     x.x.x.x  node-2
```

### Step 4: Inspect the Log

You can inspect the contents of the logged `/etc/machine-id` file by checking the log directory mounted from the host:

```bash
kubectl exec <pod-name> -- cat /var/log/machine-id.log
```

### Key Features of DaemonSets

DaemonSets provide several features for managing Pods on a per-node basis:

**Host Path Volume Mounts**: DaemonSets can mount host directories (like `/etc/machine-id`) into Pods to access system-level files or logs.
**Init Containers**: Init containers can perform setup tasks before the main container starts, such as logging or preparing the environment.
**Pause Containers**: You can use a pause container as the main container when the Pod's primary function is handled by an init container, but you still want the Pod to remain running.

This simple DaemonSet example introduces key components like init containers and host path volumes, which can be expanded upon for more advanced use cases.



