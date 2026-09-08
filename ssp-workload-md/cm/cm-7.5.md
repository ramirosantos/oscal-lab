---
x-trestle-add-props: []
  # Add or modify control properties here
  # Properties may be at the control or part level
  # Add control level properties like this:
  #   - name: ac1_new_prop
  #     value: new property value
  #
  # Add properties to a statement part like this, where "b." is the label of the target statement part
  #   - name: ac1_new_prop
  #     value: new property value
  #     smt-part: b.
  #
x-trestle-comp-def-rules:
  Kyverno Admission Controller:
    - name: kyv-signed-images
      description: Nur signierte Images aus docker.io/labuser sind zugelassen
x-trestle-set-params:
  # You may set values for parameters in the assembled SSP by adding
  #
  # ssp-values:
  #   - value 1
  #   - value 2
  #
  # below a section of values:
  # The values list refers to the values in the resolved profile catalog, and the ssp-values represent new values
  # to be placed in SetParameters of the SSP.
  #
  cm-07.05_odp.01:
    guidelines:
      - prose: software programs authorized to execute on the system are 
          defined;
    values:
      - Container-Images aus dem Docker-Hub-Repository docker.io/cb2dolw mit 
        gueltiger Cosign-Signatur
    alt-identifier: cm-7.5_prm_1
    profile-param-value-origin: <REPLACE_ME>
  cm-07.05_odp.02:
    alt-identifier: cm-7.5_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: K8s Workload Restricted (minikube Lab) - Tailoring des Platform 
      Baseline
    href: trestle://profiles/k8s-workload-restricted/profile.json
  sort-id: cm-07.05
system-characteristics:
  system-ids:
    - identifier-type: https://cyberlab.local/ns/system-id
      id: OSCAL-LAB-WORKLOAD-001
  system-name: Kubernetes Workload Platform (minikube Lab)
  description: >-
    minikube-Cluster v1.35.1 mit zwei Nodes auf der VM k8s1. Namespaces
    prod-payments und prod-batch. Enforcement durch Kyverno 1.18, Pod Security
    Admission und Calico-NetworkPolicies.
  security-sensitivity-level: moderate
  system-information:
    information-types:
      - uuid: 7f6c8e11-0000-4000-8000-0000000000a1
        title: Zahlungsverkehrsdaten (simuliert)
        description: Testdaten ohne Personenbezug.
        confidentiality-impact: {base: fips-199-moderate}
        integrity-impact: {base: fips-199-high}
        availability-impact: {base: fips-199-moderate}
  security-impact-level:
    security-objective-confidentiality: fips-199-moderate
    security-objective-integrity: fips-199-high
    security-objective-availability: fips-199-moderate
  status: {state: under-development}
  authorization-boundary:
    description: >-
      Die Autorisierungsgrenze umfasst den minikube-Cluster auf k8s1 mit allen
      darauf laufenden Workloads. Das Lab-Netz ist flach; die Grenze ist daher
      logisch und wird durch RBAC, NetworkPolicies und Credentials gezogen,
      nicht durch Netzsegmentierung. GitHub (Quellcode und CI) und Docker Hub
      (Registry) sind externe, nicht kontrollierte Dienste, auf die sich CM-2,
      CM-3, CM-14 und CP-9 stuetzen; ihre Verfuegbarkeit und Integritaet ist
      eine Annahme, kein Nachweis. oscal1 liegt als bewertende Instanz
      ausserhalb der Grenze.
---

# cm-7.5 - \[Configuration Management\] Authorized Software — Allow-by-exception

## Control Statement

- \[(a)\] Identify [Container-Images aus dem Docker-Hub-Repository docker.io/cb2dolw mit gueltiger Cosign-Signatur];

- \[(b)\] Employ a deny-all, permit-by-exception policy to allow the execution of authorized software programs on the system; and

- \[(c)\] Review and update the list of authorized software programs [frequency].

## Control Assessment Objective

- \[CM-07(05)(a)\] [Container-Images aus dem Docker-Hub-Repository docker.io/cb2dolw mit gueltiger Cosign-Signatur] are identified;

- \[CM-07(05)(b)\] a deny-all, permit-by-exception policy to allow the execution of authorized software programs on the system is employed;

- \[CM-07(05)(c)\] the list of authorized software programs is reviewed and updated [frequency].

## Control guidance

Authorized software programs can be limited to specific versions or from a specific source. To facilitate a comprehensive authorized software process and increase the strength of protection for attacks that bypass application level authorized software, software programs may be decomposed into and monitored at different levels of detail. These levels include applications, application programming interfaces, application modules, scripts, system processes, system services, kernel functions, registries, drivers, and dynamic link libraries. The concept of permitting the execution of authorized software may also be applied to user actions, system ports and protocols, IP addresses/ranges, websites, and MAC addresses. Organizations consider verifying the integrity of authorized software programs using digital signatures, cryptographic checksums, or hash functions. Verification of authorized software can occur either prior to execution or at system startup. The identification of authorized URLs for websites is addressed in [CA-3(5)](#ca-3.5) and [SC-7](#sc-7).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Allow-by-exception ueber eine Positivliste signierter Images aus dem eigenen Docker-Hub-Repository.

#### Implementation Status: implemented

### Kyverno Admission Controller

Allow-by-exception: nur signierte Images aus der eigenen Docker-Hub-Organisation.

#### Rules:

  - kyv-signed-images

#### Implementation Status: implemented

______________________________________________________________________
