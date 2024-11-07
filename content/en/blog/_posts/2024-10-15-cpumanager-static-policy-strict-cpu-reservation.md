---
layout: blog
title: 'Kubernetes v1.32: New Kubernetes CPUManager Static Policy: Strict CPU Reservation'
date: 2024-10-15
slug: cpumanager-static-policy-strict-cpu-reservation
author: >
  [Jing Zhang](https://github.com/jingczhang) (Nokia)
---

In Kubernetes v1.32, after years of community discussion, we are excited to introduce strict system CPU reservation in `CPUManager` via `strict-cpu-reservation` option for the [CPUManager static policy](/docs/tasks/administer-cluster/cpu-management-policies/#static-policy-options). This feature is currently in alpha and hidden by default hence needs be enabled explicitly.


## Understanding the feature

The `CPUManager` static policy is used to reduce latency or improve performance. The `reservedSystemCPUs` defines an explicit CPU set for OS system daemons and kubernetes system daemons. This option is specifically designed for Telco/NFV use cases where uncontrolled interrupts/timers may impact the workload performance. you can use this option to define the explicit cpuset for the system/kubernetes daemons as well as the interrupts/timers, so the rest CPUs on the system can be used exclusively for workloads, with less impact from uncontrolled interrupts/timers. More details of this parameter can be found on the [Explicitly Reserved CPU List](/docs/tasks/administer-cluster/reserve-compute-resources/#explicitly-reserved-cpu-list) page.

If you want to protect your system daemons and interrupt processing, the obvious way is to use the `reservedSystemCPUs` option.

However, until now this isolation is only implemented for guaranteed pods with integer CPU requests. Admission only compares the CPU requests against the allocatable CPUs. Since the CPU limits are higher than the CPU requests, current implementation allows burstable and best-effort pods to use up the capacity of `reservedSystemCPUs` and causes host OS services to starve in real life deployments. This behavior also makes benchmarking infrastructure and workloads both inaccurate.

When this new `strict-cpu-reservation` policy option is enabled, the `CPUManager` static policy will not allow any workload to use the reserved system CPU cores.


## Enabling the feature

To enable this feature, you need to turn on both the `CPUManagerPolicyAlphaOptions` feature gate and the `strict-cpu-reservation` policy option. And you need to remove the `/var/lib/kubelet/cpu_manager_state` file if it exists and restart kubelet.

With the following Kubelet configuration:

```yaml
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
featureGates:
  ...
  CPUManagerPolicyOptions: true
  CPUManagerPolicyAlphaOptions: true
cpuManagerPolicy: static
cpuManagerPolicyOptions:
  strict-cpu-reservation: "true"
reservedSystemCPUs: "0,32,1,33,16,48"
...
```

When `strict-cpu-reservation` is not set or set to false:
```console
# cat /var/lib/kubelet/cpu_manager_state
{"policyName":"static","defaultCpuSet":"0-63","checksum":1058907510}
```

When `strict-cpu-reservation` is set to true:
```console
# cat /var/lib/kubelet/cpu_manager_state
{"policyName":"static","defaultCpuSet":"2-15,17-31,34-47,49-63","checksum":4141502832}
```


## Monitoring the feature

You can monitor the feature impact by checking the following `CPUManager` counters:
- `cpu_manager_shared_pool_size_millicores`: report shared pool size, in millicores (e.g. 13500m)
- `cpu_manager_exclusive_cpu_allocation_count`: report exclusively allocated cores, counting full cores (e.g. 16)

Your best-effort workloads may starve if the `cpu_manager_shared_pool_size_millicores` count is zero for prolonged time.

We believe any system critical daemon like a log forwarder should not run as best-effort, but you can review and adjust the amount of CPU cores reserved as needed.

## Conclusion

Strict CPU reservation is critical for Telco/NFV use cases. It is also a prerequisite for enabling the all-in-one type of deployments where workloads are placed on nodes having combined master+worker+storage roles.

We want you to start using the feature and looking forward to your feedback.


## Further reading

Please check out the [Control CPU Management Policies on the Node](/docs/tasks/administer-cluster/cpu-management-policies/)
task page to learn more about the CPU Manager, and how it fits in relation to the other node-level resource managers.


## Getting involved

This feature is driven by the [SIG Node](https://github.com/Kubernetes/community/blob/master/sig-node/README.md). If you are interested in helping develop this feature, sharing feedback, or participating in any other ongoing SIG Node projects, please attend the SIG Node meeting for more details.
