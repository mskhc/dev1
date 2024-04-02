---
layout: blog
title: "Introducing JobSet"
date: 2024-04-02
slug: introducing-jobset
---

**Authors**: Daniel Vega-Myhre (Google), Abdullah Gharaibeh (Google), Kevin Hannon (Red Hat)

In this article, we introduce [JobSet](https://jobset.sigs.k8s.io/), an open source API for representing distributed jobs. The goal of JobSet is to provide a stable API for running/building APIs with AI/ML and HPC use cases in mind.

## Why JobSet?

The Kubernetes community’s recent enhancements to the batch ecosystem on Kubernetes attracted ML engineers who have found it to be a natural fit for the requirements of running distributed training workloads. 

Large ML models (particularly LLMs) which cannot fit into the memory of the GPU or TPU chips on a single host are often distributed across tens of thousands of accelerator chips, which in turn may span thousands of hosts. 

As such, the model training code is often containerized and executed simultaneously on all these hosts, performing distributed computations which often shard both the model parameters and/or the training dataset across the target accelerator chips, using communication collective primitives like all-gather and all-reduce to perform distributed computations and synchronize gradients between hosts. 

These workload characteristics make Kubernetes a great fit for this type of workload, as efficiently scheduling and managing the lifecycle of containerized applications across a cluster of compute resources is an area where it shines. 

It is also very extensible, allowing developers to define their own Kubernetes APIs, objects, and controllers which manage the behavior and life cycle of these objects, allowing engineers to develop custom distributed training orchestration solutions to fit their needs.

However, as distributed ML training techniques continue to evolve, existing Kubernetes primitives do not adequately model them alone anymore. Furthermore, the landscape of Kubernetes distributed training orchestration APIs has become fragmented, and each of the existing solutions in this fragmented landscape has certain limitations that make it non-optimal for distributed ML training. 

On the one hand, the KubeFlow training operator defines custom APIs for different ML frameworks (e.g. PyTorchJob, TFJob, MPIJob, etc.); however, each of these job types are in fact a solution fit specifically to the target framework, each with different semantics and behavior. 

On the other hand, the Job API fixed many gaps for running batch workloads, including Indexed completion mode, higher scalability, Pod failure policies and Pod backoff policy to mention a few of the most recent enhancements. However, running ML training and HPC workloads using the upstream Job API requires extra orchestration to fill the following gaps:

1) **Multi-template Pods**: Most HPC or ML training jobs include more than one type of Pods. The different Pods are part of the same workload, but they need to run a different container, request different resources or have different failure policies. A common example is the driver-worker pattern.

2) **Job Groups**: Large scale training workloads span multiple network topologies, running across multiple racks for example. Such workloads are network latency sensitive, and aim to localize communication and minimize traffic crossing the higher-latency network links. To facilitate this, the workload needs to be split into groups of Pods each assigned to a network topology.

3) **Network setup**: Create and manage the resources (e.g. headless services) necessary to establish communication between the Pods of a job. 

4) **Startup sequence**: Some jobs require a specific start sequence of pods; sometimes the driver is expected to start first (like Ray or Spark), in other cases the workers are expected to be ready before starting the driver (like MPI). 

JobSet aims to address those gaps using the Job API as a building block to build a richer API for large-scale distributed HPC and ML use cases.

## How JobSet Works
JobSet models a distributed batch workload as a group of Kubernetes Jobs. This allows a user to easily specify different pod templates for different distinct groups of pods (e.g. a leader, workers, parameter servers, etc.). 

It uses the abstraction of a ReplicatedJob to manage child Jobs, where a ReplicatedJob is essentially a Job Template with some desired number of Job replicas specified. This provides a declarative way to easily create identical child-jobs to run on different islands of accelerators, without resorting to scripting or Helm charts to generate many versions of the same job but with different names.

![JobSet Architecture Diagram](jobset_diagram.png "JobSet Architecture")

Some other key JobSet features which address the problems described above include:

1) **Job Groups**: In modern data centers, hardware accelerators like GPUs and TPUs allocated in islands of homogenous accelerators connected via a specialized, high bandwidth network links. For example, a user might provision nodes containing a group of hosts co-located on a rack, each with H100 GPUs, where GPU chips within each host are connected via NVLink, with a NVLink Switch connecting the multiple NVLinks. TPU Pods are another example of this: TPU ViperLitePods consist of 64 hosts, each with 4 TPU v5e chips attached, all connected via ICI mesh. 
When running a distributed training job across multiple of these islands, we often want to partition the workload into a group of smaller identical jobs, 1 per island, where each pod primarily communicates with the pods within the same island to do segments of distributed computation, and keeping the gradient synchronization over DCN (data center network, which is lower bandwidth than ICI) to a bare minimum. 

2) **Automatic headless service creation, configuration, and lifecycle management**: pod-to-pod communication via pod hostname is enabled by default, with automatic configuration and lifecycle management of the headless service enabling this. 
Configurable success policies: JobSet has configurable success policies which target specific ReplicatedJobs, with operators to target “Any” or “All” of their child jobs. For example, you can configure the JobSet to be marked complete if and only if all pods that are part of the “worker” ReplicatedJob are completed.

3) **Configurable failure policies**: JobSet has configurable failure policies which allow the user to specify a maximum number of times the JobSet should be restarted in the event of a failure. If any job is marked failed, the entire JobSet will be recreated, allowing the workload to resume from the last checkpoint. When no failure policy is specified, if any job fails, the JobSet simply fails. 

4) **Exclusive placement per topology domain**: JobSet allows users to express that child jobs have 1:1 exclusive assignment to a topology domain, typically an accelerator island like a rack. For example, if the JobSet creates two child jobs, then this feature will enforce that the pods of each child job will be co-located on the same island, and that only one child job is allowed to schedule per island. This useful for scenarios where, for example, we want to use a data parallel distributed training strategy to train a model using multiple islands of compute resources (GPU racks or TPU slices), running 1 model replica in each accelerator island, ensuring the forward and backward passes themselves occur within a single model replica occurs over the high bandwidth interconnect linking the accelerators chips within the island, and only the gradient synchronization between model replicas occurs across accelerator islands over the lower bandwidth data center network.

5) **Integration with Kueue**: users can submit JobSets via [Kueue](https://kueue.sigs.k8s.io/) to oversubscribe their clusters, queue workloads to run as capacity becomes available, prevent partial scheduling and deadlocks, enable multi-tenancy, and more.

## Example Use Case

One can install JobSet as follows:


```bash
VERSION=v0.4.0
kubectl apply --server-side -f https://github.com/kubernetes-sigs/jobset/releases/download/$VERSION/manifests.yaml
```

Pytorch training

The following example demonstrates how to run distributed training using PyTorch. JobSet creates a Job with 4 pods and a headless service defined as pytorch. This allows for communication between the replicas. JobSet streamlines the creation of the headless service and allows for a single CRD for representing these jobs.

```yaml
# Distributed training of a traditional CNN model to do image classification 
# using the MNIST dataset and PyTorch.
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: pytorch
spec:
  replicatedJobs:
  - name: workers
    template:
      spec:
        parallelism: 4
        completions: 4
        backoffLimit: 0
        template:
          spec:
            containers:
            - name: pytorch
              image: gcr.io/k8s-staging-jobset/pytorch-mnist:latest
              ports:
              - containerPort: 3389
              env:
              - name: MASTER_ADDR
                value: "pytorch-workers-0-0.pytorch"
              - name: MASTER_PORT
                value: "3389"
              - name: RANK
                valueFrom:
                  fieldRef:
                    fieldPath: metadata.annotations['batch.kubernetes.io/job-completion-index']
              # Force python to not buffer output and write directly to stdout, so we can view training logs via `kubectl logs`.
              - name: PYTHONUNBUFFERED
                value: "0"
              command:
              - bash
              - -xc
              - |
                torchrun --rdzv_id=123 --nnodes=4 --nproc_per_node=1 --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT --node_rank=$RANK mnist.py --epochs=1 --log-interval=1 
```

Leader-Worker

A popular paradigm for distributed workloads is the leader-worker design. Leader-worker entails having a leader pod, with a different template than workers, and worker pods. The leader must be started before the workers are started and if all the workers finish we can consider the workload complete and the overallworkload can be considered successful.

a) Different pod templates for workers and leaders
b) Success policies on the workers
c) Startup policies


Example workload

```yaml
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: success-policy
spec:
# We want to start our JobSet in order with leader starting first and then workers starting
  startupPolicy:
    startupPolicyOrder: InOrder
# We want to declare our JobSet successful if workers finish.
# If workers finish we should clean up the remaining replicatedJobs.
  successPolicy:
    operator: All
    targetReplicatedJobs:
    - workers
  replicatedJobs:
  - name: leader
    replicas: 1
    template:
      spec:
        # Set backoff limit to 0 so job will immediately fail if any pod fails.
        backoffLimit: 0 
        completions: 1
        parallelism: 1
        template:
          spec:
            containers:
            - name: leader
              image: bash:latest
              command:
              - bash
              - -xc
              - |
                sleep 10000
  - name: workers
    replicas: 1
    template:
      spec:
        backoffLimit: 0 
        completions: 2
        parallelism: 2
        template:
          spec:
            containers:
            - name: worker
              image: bash:latest
              command:
              - bash
              - -xc
              - |
                sleep 10
```

## Future work and getting involved
We have a number of features on the JobSet roadmap planned for development this year, which can be found in the [JobSet roadmap](https://github.com/kubernetes-sigs/jobset?tab=readme-ov-file#roadmap).

Please feel free to reach out with feedback of any kind. We’re also open to additional contributors, whether it is to fix or report bugs, or help add new features or write documentation. 

You can get in touch with
us via our [repo](http://sigs.k8s.io/jobset), [mailing list](https://groups.google.com/a/kubernetes.io/g/wg-batch) or on 
[Slack](https://kubernetes.slack.com/messages/wg-batch).

Last but not least, thanks to all [our contributors](https://github.com/kubernetes-sigs/jobset/graphs/contributors) who made this project possible!
