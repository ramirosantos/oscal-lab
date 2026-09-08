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
  cm-03_odp.01:
    alt-identifier: cm-3_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-03_odp.02:
    alt-identifier: cm-3_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-03_odp.03:
    alt-identifier: cm-3_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-03_odp.04:
    alt-identifier: cm-3_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-03_odp.05:
    alt-identifier: cm-3_prm_5
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: K8s Platform Baseline (minikube Lab) - Tailoring von NIST SP 800-53 
      Rev. 5
    href: trestle://profiles/k8s-platform-baseline/profile.json
  sort-id: cm-03
system-characteristics:
  system-ids:
    - identifier-type: https://cyberlab.local/ns/system-id
      id: OSCAL-LAB-PLATFORM-001
  system-name: Kubernetes Platform Baseline (minikube Lab)
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

# cm-3 - \[Configuration Management\] Configuration Change Control

## Control Statement

- \[a.\] Determine and document the types of changes to the system that are configuration-controlled;

- \[b.\] Review proposed configuration-controlled changes to the system and approve or disapprove such changes with explicit consideration for security and privacy impact analyses;

- \[c.\] Document configuration change decisions associated with the system;

- \[d.\] Implement approved configuration-controlled changes to the system;

- \[e.\] Retain records of configuration-controlled changes to the system for [time period];

- \[f.\] Monitor and review activities associated with configuration-controlled changes to the system; and

- \[g.\] Coordinate and provide oversight for configuration change control activities through [configuration change control element] that convenes [Selection (one or more): [frequency]; when [configuration change conditions]].

## Control Assessment Objective

- \[CM-03a.\] the types of changes to the system that are configuration-controlled are determined and documented;

- \[CM-03b.\]

  - \[CM-03b.[01]\] proposed configuration-controlled changes to the system are reviewed;
  - \[CM-03b.[02]\] proposed configuration-controlled changes to the system are approved or disapproved with explicit consideration for security and privacy impact analyses;

- \[CM-03c.\] configuration change decisions associated with the system are documented;

- \[CM-03d.\] approved configuration-controlled changes to the system are implemented;

- \[CM-03e.\] records of configuration-controlled changes to the system are retained for [time period];

- \[CM-03f.\]

  - \[CM-03f.[01]\] activities associated with configuration-controlled changes to the system are monitored;
  - \[CM-03f.[02]\] activities associated with configuration-controlled changes to the system are reviewed;

- \[CM-03g.\]

  - \[CM-03g.[01]\] configuration change control activities are coordinated and overseen by [configuration change control element];
  - \[CM-03g.[02]\] the configuration control element convenes [Selection (one or more): [frequency]; when [configuration change conditions]].

## Control guidance

Configuration change control for organizational systems involves the systematic proposal, justification, implementation, testing, review, and disposition of system changes, including system upgrades and modifications. Configuration change control includes changes to baseline configurations, configuration items of systems, operational procedures, configuration settings for system components, remediate vulnerabilities, and unscheduled or unauthorized changes. Processes for managing configuration changes to systems include Configuration Control Boards or Change Advisory Boards that review and approve proposed changes. For changes that impact privacy risk, the senior agency official for privacy updates privacy impact assessments and system of records notices. For new systems or major upgrades, organizations consider including representatives from the development organizations on the Configuration Control Boards or Change Advisory Boards. Auditing of changes includes activities before and after changes are made to systems and the auditing activities required to implement such changes. See also [SA-10](#sa-10).

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

<!-- Add implementation prose for the main This System component for control: cm-3 -->

#### Implementation Status: planned

______________________________________________________________________
