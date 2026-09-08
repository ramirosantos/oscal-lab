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
  Pod Security Admission:
    - name: psa-restricted-enforce
      description: Namespace erzwingt Pod Security Standard 'restricted'
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
  cm-06_odp.01:
    values:
      - CIS Kubernetes Benchmark v1.12 und Pod Security Standard 'restricted'
    alt-identifier: cm-6_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-06_odp.02:
    alt-identifier: cm-6_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cm-06_odp.03:
    alt-identifier: cm-6_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: K8s Workload Restricted (minikube Lab) - Tailoring des Platform 
      Baseline
    href: trestle://profiles/k8s-workload-restricted/profile.json
  sort-id: cm-06
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

# cm-6 - \[Configuration Management\] Configuration Settings

## Control Statement

- \[a.\] Establish and document configuration settings for components employed within the system that reflect the most restrictive mode consistent with operational requirements using [CIS Kubernetes Benchmark v1.12 und Pod Security Standard 'restricted'];

- \[b.\] Implement the configuration settings;

- \[c.\] Identify, document, and approve any deviations from established configuration settings for [system components] based on [operational requirements] ; and

- \[d.\] Monitor and control changes to the configuration settings in accordance with organizational policies and procedures.

## Control Assessment Objective

- \[CM-06a.\] configuration settings that reflect the most restrictive mode consistent with operational requirements are established and documented for components employed within the system using [CIS Kubernetes Benchmark v1.12 und Pod Security Standard 'restricted'];

- \[CM-06b.\] the configuration settings documented in CM-06a are implemented;

- \[CM-06c.\]

  - \[CM-06c.[01]\] any deviations from established configuration settings for [system components] are identified and documented based on [operational requirements];
  - \[CM-06c.[02]\] any deviations from established configuration settings for [system components] are approved;

- \[CM-06d.\]

  - \[CM-06d.[01]\] changes to the configuration settings are monitored in accordance with organizational policies and procedures;
  - \[CM-06d.[02]\] changes to the configuration settings are controlled in accordance with organizational policies and procedures.

## Control guidance

Configuration settings are the parameters that can be changed in the hardware, software, or firmware components of the system that affect the security and privacy posture or functionality of the system. Information technology products for which configuration settings can be defined include mainframe computers, servers, workstations, operating systems, mobile devices, input/output devices, protocols, and applications. Parameters that impact the security posture of systems include registry settings; account, file, or directory permission settings; and settings for functions, protocols, ports, services, and remote connections. Privacy parameters are parameters impacting the privacy posture of systems, including the parameters required to satisfy other privacy controls. Privacy parameters include settings for access controls, data processing preferences, and processing and retention permissions. Organizations establish organization-wide configuration settings and subsequently derive specific configuration settings for systems. The established settings become part of the configuration baseline for the system.

Common secure configurations (also known as security configuration checklists, lockdown and hardening guides, and security reference guides) provide recognized, standardized, and established benchmarks that stipulate secure configuration settings for information technology products and platforms as well as instructions for configuring those products or platforms to meet operational requirements. Common secure configurations can be developed by a variety of organizations, including information technology product developers, manufacturers, vendors, federal agencies, consortia, academia, industry, and other organizations in the public and private sectors.

Implementation of a common secure configuration may be mandated at the organization level, mission and business process level, system level, or at a higher level, including by a regulatory agency. Common secure configurations include the United States Government Configuration Baseline [USGCB](#98498928-3ca3-44b3-8b1e-f48685373087) and security technical implementation guides (STIGs), which affect the implementation of [CM-6](#cm-6) and other controls such as [AC-19](#ac-19) and [CM-7](#cm-7) . The Security Content Automation Protocol (SCAP) and the defined standards within the protocol provide an effective method to uniquely identify, track, and control configuration settings.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Konfigurationseinstellungen folgen dem Pod Security Standard restricted. Abweichungen sind ueber die Namespace-Labels sichtbar und messbar.

#### Implementation Status: implemented

### Pod Security Admission

Configuration Settings entsprechen dem Pod Security Standard restricted.

#### Rules:

  - psa-restricted-enforce

#### Implementation Status: implemented

______________________________________________________________________
