---
layout: blog
title: "Memory Manager goes GA"
date: 2024-10-28
slug: memory-manager-goes-ga
author: >
  [Talor Itzhak](https://github.com/Tal-or) (Red Hat)
---

With Kubernetes 1.32, the Memory Manager has officially graduated to General Availability (GA),
marking a significant milestone in the journey toward efficient and predictable memory allocation for containerized applications.
Since Kubernetes v1.22, where it graduated to beta, the Memory Manager has proved itself reliable, stable and a good complementary feature for the [CPU Manager](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/).

As part of Kubelet's workload admission process, 
the Memory manager provides topology hints 
to optimize memory allocation and alignment. 
This enables users to allocate exclusive
memory for `Guaranteed` [QoS class](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/#qos-classes) pods.
More details about the process can be found [here](https://kubernetes.io/blog/2021/08/11/kubernetes-1-22-feature-memory-manager-moves-to-beta/).

Most of the changes introduced since the Beta are bug fixes, internal refactoring and 
observability improvements, such as metrics and better logging.

## Observability Improvements

As part of the effort
to increase the observability of Memory Manager, new metrics have been added
to provide some statistics on memory allocation patterns.


**memory_manager_pinning_requests_total**
tracks the number of times the pod spec required the memory manager to pin memory pages.

**memory_manager_pinning_errors_total**
tracks the number of times the pod spec required the memory manager 
to pin memory pages, but the allocation failed.


## Improving Memory Manager Reliability and Consistency

Kubelet does not guarantee pod ordering
when admitting pods after a restart or reboot.

In certain edge cases, this behavior could cause
the Memory Manager to reject some pods,
and in more extreme cases, it may cause Kubelet to fail upon restart.

Previously, the beta implementation lacked certain checks and logic to prevent 
these issues.

To stabilize the Memory Manager for general availability (GA) readiness,
small but critical refinements have been
made to the algorithm, improving its robustness and handling of edge cases.

## Future Development

There is more to come for the future of Topology Manager in general,
and Memory Manager in particular: 
### Windows support

Efforts are underway to support [Memory Manager on Windows](https://github.com/kubernetes/kubernetes/pull/128560),
enabling CPU and memory affinity on Windows OS.  

## Getting involved

This feature is driven by the [SIG Node](https://github.com/Kubernetes/community/blob/master/sig-node/README.md) community.
Please join us to connect with the community
and share your ideas and feedback around the above feature and
beyond.
We look forward to hearing from you!

