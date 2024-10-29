---
title: PreStop Hook
---

# PreStop Hook

The PreStop hook is a special lifecycle hook that runs a command or sends an HTTP request before the container is terminated.When a preStop hook is defined on a container, the specified command will execute before the container is shut down. This behavior allows the container to perform any necessary cleanup or finalization tasks.


## Basic PreStop Behavior

When you have a PreStop hook defined on your container, it will execute before the container is terminated.

Imagine You Have a Pod with the Following Specification:

metadata:
    name: prestop-pod
  spec:
    containers:
    - image: registry.k8s.io/e2e-test-images/agnhost:2.53
      lifecycle:
        preStop:
          exec:
            command:
            - sh
            - -c
            - echo 'PreStop Hook Executed' > /data/prestop_hook_executed; sleep 10
      name: prestop-container
      volumeMounts:
      - mountPath: /data
        name: shared-data
    terminationGracePeriodSeconds: 30
    volumes:
    - emptyDir: {}
      name: shared-data
  
This Pod should start successfully and run for some time
When the container is terminated, the PreStop hook will be triggered within the grace period
Once the PreStop hook is successfully executed, the container terminates successfully


### These are logs for reference when running this test:

Creating a Pod with PreStop hook that writes to a shared volume
Pod is created successfully
The Pod is running successfully
Pod was deleted successfully
prestop_hook_executed


<!-- init_container_failing -->

