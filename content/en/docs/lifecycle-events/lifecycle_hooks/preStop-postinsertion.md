---
title: "PreStop Hook"
content_type: "reference"
weight: 50
auto_generated: true
description: "Documentation for the PreStop hook test suite within lifecycle events."
---

# PreStop Hook

The PreStop hook is a special lifecycle hook that runs a command or sends an HTTP request before the container is terminated. When a preStop hook is defined on a container, the specified command will execute before the container is shut down. This behavior allows the container to perform any necessary cleanup or finalisation tasks.

<!-- prestop_basic_execution_test_starts -->

When you have a PreStop hook defined on your container, it will execute before the container is terminated.

Imagine You Have a Pod with the Following Specification

metadata:
    name: prestop-pod
  spec:
    containers:
    - args:
      - pause
      image: registry.k8s.io/e2e-test-images/agnhost:2.53
      lifecycle:
        preStop:
          exec:
            command:
            - sh
            - -c
            - echo 'PreStop Hook Executed' > /data/prestop_hook_executed; sleep 10
      name: prestop-container
      resources: {}
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
          - ALL
        runAsGroup: 1000
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile:
          type: RuntimeDefault
      volumeMounts:
      - mountPath: /data
        name: shared-data
    terminationGracePeriodSeconds: 60
    volumes:
    - emptyDir: {}
      name: shared-data
  
This Pod should start successfully and run for some time
When the container is terminated, the PreStop hook will be triggered within the grace period
Once the PreStop hook is successfully executed, the container terminates successfully


###Logs for the test
PreStop hook executed successfully


<!-- prestop_basic_execution_test_ends -->

<!-- prestop_basic_failure_test_starts -->
<!-- Test details, pod specs, steps, and logs for PreStop Basic Failure Test will be auto-inserted here -->
<!-- prestop_basic_failure_test_ends -->

<!-- prestop_multiple_containers_test_starts -->
<!-- Test details, pod specs, steps, and logs for PreStop Multiple Container Test will be auto-inserted here -->
<!-- prestop_multiple_containers_test_ends -->
