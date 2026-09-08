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
  cp-09_odp.01:
    alt-identifier: cp-9_prm_1
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-09_odp.02:
    alt-identifier: cp-9_prm_2
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-09_odp.03:
    alt-identifier: cp-9_prm_3
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
  cp-09_odp.04:
    alt-identifier: cp-9_prm_4
    profile-values:
      - <REPLACE_ME>
    profile-param-value-origin: <REPLACE_ME>
x-trestle-global:
  profile:
    title: K8s Platform Baseline (minikube Lab) - Tailoring von NIST SP 800-53 
      Rev. 5
    href: trestle://profiles/k8s-platform-baseline/profile.json
  sort-id: cp-09
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

# cp-9 - \[Contingency Planning\] System Backup

## Control Statement

- \[a.\] Conduct backups of user-level information contained in [system components] [frequency];

- \[b.\] Conduct backups of system-level information contained in the system [frequency];

- \[c.\] Conduct backups of system documentation, including security- and privacy-related documentation [frequency] ; and

- \[d.\] Protect the confidentiality, integrity, and availability of backup information.

## Control Assessment Objective

- \[CP-09a.\] backups of user-level information contained in [system components] are conducted [frequency];

- \[CP-09b.\] backups of system-level information contained in the system are conducted [frequency];

- \[CP-09c.\] backups of system documentation, including security- and privacy-related documentation are conducted [frequency];

- \[CP-09d.\]

  - \[CP-09d.[01]\] the confidentiality of backup information is protected;
  - \[CP-09d.[02]\] the integrity of backup information is protected;
  - \[CP-09d.[03]\] the availability of backup information is protected.

## Control guidance

System-level information includes system state information, operating system software, middleware, application software, and licenses. User-level information includes information other than system-level information. Mechanisms employed to protect the integrity of system backups include digital signatures and cryptographic hashes. Protection of system backup information while in transit is addressed by [MP-5](#mp-5) and [SC-8](#sc-8) . System backups reflect the requirements in contingency plans as well as other organizational requirements for backing up information. Organizations may be subject to laws, executive orders, directives, regulations, or policies with requirements regarding specific categories of information (e.g., personal health information). Organizational personnel consult with the senior agency official for privacy and legal counsel regarding such requirements.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Der Cluster ist bewusst zustandsarm: die vollstaendige Konfiguration liegt auf GitHub. Zusaetzlich wird taeglich ein etcd-Snapshot erzeugt und im Repository abgelegt.

#### Implementation Status: implemented

______________________________________________________________________
