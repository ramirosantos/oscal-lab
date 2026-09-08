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
  si-7.1_prm_1:
    aggregates:
      - si-07.01_odp.01
      - si-07.01_odp.05
      - si-07.01_odp.09
    profile-param-value-origin: <REPLACE_ME>
  si-7.1_prm_2:
    aggregates:
      - si-07.01_odp.02
      - si-07.01_odp.06
      - si-07.01_odp.10
    profile-param-value-origin: <REPLACE_ME>
  si-7.1_prm_3:
    aggregates:
      - si-07.01_odp.03
      - si-07.01_odp.07
      - si-07.01_odp.11
    profile-param-value-origin: <REPLACE_ME>
  si-7.1_prm_4:
    aggregates:
      - si-07.01_odp.04
      - si-07.01_odp.08
      - si-07.01_odp.12
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.01:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.02:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.03:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.04:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.05:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.06:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.07:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.08:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.09:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.10:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.11:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  si-07.01_odp.12:
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: K8s Workload Restricted (minikube Lab) - Tailoring des Platform 
      Baseline
    href: trestle://profiles/k8s-workload-restricted/profile.json
  sort-id: si-07.01
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

# si-7.1 - \[System and Information Integrity\] Integrity Checks

## Control Statement

Perform an integrity check of [organization-defined software, firmware, and information] [Selection (one or more): at startup; at [organization-defined transitional states or security-relevant events]; [organization-defined frequency]].

## Control Assessment Objective

- \[SI-07(01)[01]\] an integrity check of [software] is performed [Selection (one or more): at startup; at [transitional states or security-relevant events]; [frequency]];

- \[SI-07(01)[02]\] an integrity check of [firmware] is performed [Selection (one or more): at startup; at [transitional states or security-relevant events]; [frequency]];

- \[SI-07(01)[03]\] an integrity check of [information] is performed [Selection (one or more): at startup; at [transitional states or security-relevant events]; [frequency]].

## Control guidance

Security-relevant events include the identification of new threats to which organizational systems are susceptible and the installation of new hardware, software, or firmware. Transitional states include system startup, restart, shutdown, and abort.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Der naechtliche CI-Lauf vergleicht den Cluster-Zustand mit dem GitHub-Repo und meldet Abweichungen als Regression.

#### Implementation Status: implemented

______________________________________________________________________
