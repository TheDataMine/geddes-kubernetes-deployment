<p align="center">
  <a href="https://datamine.purdue.edu"><img width="100%" src="./images/banner.png" alt='Purdue University'></a>
</p>

# Deploying Python Applications to Geddes via Kubernetes
Contact Justin Gould (gould29@purdue.edu) for more information.

# Getting Started
## What is Kubernetes?
To explain what Kubernetes is, I will reference [language used by the developers of Kubernetes](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)...

Kubernetes, also known as K8s, is an open-source system for automating deployment, scaling, and management of containerized applications.. It groups containers that make up an application into logical units for easy management and discovery. Kubernetes builds upon 15 years of experience of running production workloads at Google, combined with best-of-breed ideas and practices from the community.

Let's take a look at why Kubernetes is so useful by going back in time.
![Image](https://d33wubrfki0l68.cloudfront.net/26a177ede4d7b032362289c6fccd448fc4a91174/eb693/images/docs/container_evolution.svg)

**Traditional deployment era:** Early on, organizations ran applications on physical servers. There was no way to define resource boundaries for applications in a physical server, and this caused resource allocation issues. For example, if multiple applications run on a physical server, there can be instances where one application would take up most of the resources, and as a result, the other applications would underperform. A solution for this would be to run each application on a different physical server. But this did not scale as resources were underutilized, and it was expensive for organizations to maintain many physical servers.

**Virtualized deployment era:** As a solution, virtualization was introduced. It allows you to run multiple Virtual Machines (VMs) on a single physical server's CPU. Virtualization allows applications to be isolated between VMs and provides a level of security as the information of one application cannot be freely accessed by another application.

Virtualization allows better utilization of resources in a physical server and allows better scalability because an application can be added or updated easily, reduces hardware costs, and much more. With virtualization you can present a set of physical resources as a cluster of disposable virtual machines.

Each VM is a full machine running all the components, including its own operating system, on top of the virtualized hardware.

**Container deployment era:** Containers are similar to VMs, but they have relaxed isolation properties to share the Operating System (OS) among the applications. Therefore, containers are considered lightweight. Similar to a VM, a container has its own filesystem, share of CPU, memory, process space, and more. As they are decoupled from the underlying infrastructure, they are portable across clouds and OS distributions.

Containers have become popular because they provide extra benefits, such as:
- Agile application creation and deployment: increased ease and efficiency of container image creation compared to VM image use.
- Continuous development, integration, and deployment: provides for reliable and frequent container image build and deployment with quick and efficient rollbacks (due to image immutability).
- Dev and Ops separation of concerns: create application container images at build/release time rather than deployment time, thereby decoupling applications from infrastructure.
- Observability not only surfaces OS-level information and metrics, but also application health and other signals.
- Environmental consistency across development, testing, and production: Runs the same on a laptop as it does in the cloud.
- Cloud and OS distribution portability: Runs on Ubuntu, RHEL, CoreOS, on-premises, on major public clouds, and anywhere else.
- Application-centric management: Raises the level of abstraction from running an OS on virtual hardware to running an application on an OS using logical resources.
- Loosely coupled, distributed, elastic, liberated micro-services: applications are broken into smaller, independent pieces and can be deployed and managed dynamically – not a monolithic stack running on one big single-purpose machine.
- Resource isolation: predictable application performance.
- Resource utilization: high efficiency and density.

Containers are a good way to bundle and run your applications. In a production environment, you need to manage the containers that run the applications and ensure that there is no downtime. For example, if a container goes down, another container needs to start. Wouldn't it be easier if this behavior was handled by a system?

That's how Kubernetes comes to the rescue! Kubernetes provides you with a framework to run distributed systems resiliently. It takes care of scaling and failover for your application, provides deployment patterns, and more. For example, Kubernetes can easily manage a canary deployment for your system.

Kubernetes provides you with:
- Service discovery and load balancing Kubernetes can expose a container using the DNS name or using their own IP address. If traffic to a container is high, Kubernetes is able to load balance and distribute the network traffic so that the deployment is stable.
- Storage orchestration Kubernetes allows you to automatically mount a storage system of your choice, such as local storages, public cloud providers, and more.
- Automated rollouts and rollbacks You can describe the desired state for your deployed containers using Kubernetes, and it can change the actual state to the desired state at a controlled rate. For example, you can automate Kubernetes to create new containers for your deployment, remove existing containers and adopt all their resources to the new container.
- Automatic bin packing You provide Kubernetes with a cluster of nodes that it can use to run containerized tasks. You tell Kubernetes how much CPU and memory (RAM) each container needs. Kubernetes can fit containers onto your nodes to make the best use of your resources.
- Self-healing Kubernetes restarts containers that fail, replaces containers, kills containers that don't respond to your user-defined health check, and doesn't advertise them to clients until they are ready to serve.
- Secret and configuration management Kubernetes lets you store and manage sensitive information, such as passwords, OAuth tokens, and SSH keys. You can deploy and update secrets and application configuration without rebuilding your container images, and without exposing secrets in your stack configuration.

## Kubernetes Architecture and Components
When you deploy Kubernetes, you get a cluster.

A Kubernetes cluster consists of a set of worker machines, called nodes, that run containerized applications. Every cluster has at least one worker node.

The worker node(s) host the Pods that are the components of the application workload. The control plane manages the worker nodes and the Pods in the cluster. In production environments, the control plane usually runs across multiple computers and a cluster usually runs multiple nodes, providing fault-tolerance and high availability.

This document outlines the various components you need to have a complete and working Kubernetes cluster.

Here's the diagram of a Kubernetes cluster with all the components tied together.

![Diagram](https://d33wubrfki0l68.cloudfront.net/2475489eaf20163ec0f54ddc1d92aa8d4c87c96b/e7c81/images/docs/components-of-kubernetes.svg)

# Deploying your First Python Application on Geddes via Kubernetes
Overview:

_Prerequisite Steps_

1. Install necessary software on your computer
2. Request access to Geddes from ITaP

_Application-specific Steps_

3. Configure local Kubernetes config, based off Geddes config
4. Locally develop and test Docker image
5. Create a project or namespace on `geddes-registry`, or find an existing one to contribute to
6. Tag and push local Docker image to `geddes-registry` project or namespace
7. Create robot account on `geddes-registry`, if necessary
8. Create a project or namespace on Rancher, or find an existing one to contribute to
9. Add your registry to a project or namespace on Rancher
10. Add robot account to Rancher
11. Use registry in a deployment on Rancher

## Install Necessary Software on your Computer

Before deploying to Kubernetes on Geddes, you need to install and set up the following on your local machine:

- Docker
  - https://www.docker.com/products/docker-desktop
  - Once downloaded and installed, be sure to start docker and verify it is installed correctly by opening a terminal on Mac and Linux and running the command `docker` (on Windows, you will need a UNIX shell, so open PowerShell). You should see helpful information on commands, etc.
- Kubernetes
  - http://kubernetes.io/docs/user-guide/prereqs/
  - By walking through the above guide, you will install and set up Kubernetes for your local computing environment

## Request access to Geddes from ITaP

Access to Geddes can be requested via a ticket to rcac-help@purdue.edu. 

## Configure Local Kubernetes

Once you have access to Geddes, [connect to Purdue's VPN](https://www.itap.purdue.edu/connections/vpn/), if off campus, and log on to Rancher at https://beta.geddes.rcac.purdue.edu/login.

You should see this upon authentication:
![Rancher](./images/rancher_home.png)

Click on the `geddes` cluster:
![Rancher](./images/geddes_cluster.png)

Find the "Kubeconfig File" button in the upper right, which will pull up this pop-up window:
![Rancher](./images/popup.png)

