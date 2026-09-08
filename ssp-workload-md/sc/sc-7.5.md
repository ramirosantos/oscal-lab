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
  Calico CNI:
    - name: net-default-deny
      description: Default-Deny NetworkPolicy fuer Ingress und Egress je 
        Workload-Namespace
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
  sc-07.05_odp.01:
    alt-identifier: sc-7.5_prm_1
    profile-param-value-origin: <REPLACE_ME>
  sc-07.05_odp.02:
    alt-identifier: sc-7.5_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: K8s Workload Restricted (minikube Lab) - Tailoring des Platform 
      Baseline
    href: trestle://profiles/k8s-workload-restricted/profile.json
  sort-id: sc-07.05
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

# sc-7.5 - \[System and Communications Protection\] Deny by Default — Allow by Exception

## Control Statement

Deny network communications traffic by default and allow network communications traffic by exception [Selection (one or more): at managed interfaces; for [systems]].

## Control Assessment Objective

- \[SC-07(05)[01]\] network communications traffic is denied by default [Selection (one or more): at managed interfaces; for [systems]];

- \[SC-07(05)[02]\] network communications traffic is allowed by exception [Selection (one or more): at managed interfaces; for [systems]].

## Control guidance

Denying by default and allowing by exception applies to inbound and outbound network communications traffic. A deny-all, permit-by-exception network communications traffic policy ensures that only those system connections that are essential and approved are allowed. Deny by default, allow by exception also applies to a system that is connected to an external system.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Deny-by-default: jeder Workload-Namespace besitzt eine default-deny NetworkPolicy fuer Ingress und Egress.

#### Implementation Status: implemented

### Calico CNI

Deny-by-default fuer Ingress und Egress.

#### Rules:

  - net-default-deny

#### Implementation Status: implemented

______________________________________________________________________
