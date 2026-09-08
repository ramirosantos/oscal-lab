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
  Kubernetes Control Plane:
    - name: api-anonymous-off
      description: Anonymer Zugriff ist auf die Health-Endpunkte /healthz, 
        /livez und /readyz beschraenkt
x-trestle-global:
  profile:
    title: K8s Workload Restricted (minikube Lab) - Tailoring des Platform 
      Baseline
    href: trestle://profiles/k8s-workload-restricted/profile.json
  sort-id: ac-03
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

# ac-3 - \[Access Control\] Access Enforcement

## Control Statement

Enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies.

## Control Assessment Objective

approved authorizations for logical access to information and system resources are enforced in accordance with applicable access control policies.

## Control guidance

Access control policies control access between active entities or subjects (i.e., users or processes acting on behalf of users) and passive entities or objects (i.e., devices, files, records, domains) in organizational systems. In addition to enforcing authorized access at the system level and recognizing that systems can host many applications and services in support of mission and business functions, access enforcement mechanisms can also be employed at the application and service level to provide increased information security and privacy. In contrast to logical access controls that are implemented within the system, physical access controls are addressed by the controls in the Physical and Environmental Protection ( [PE](#pe) ) family.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

Zugriffe werden am kube-apiserver durch RBAC und anschliessend durch die Admission-Kette (PodSecurity, Kyverno) erzwungen. Anonymer Zugriff ist per AuthenticationConfiguration auf /healthz, /livez und /readyz beschraenkt.

#### Implementation Status: implemented

### Kubernetes Control Plane

Access Enforcement durch RBAC am API-Server.

#### Rules:

  - api-anonymous-off

#### Implementation Status: implemented

### Pod Security Admission

Access Enforcement auf Pod-Spezifikationsebene durch PSS restricted.

#### Rules:

  - psa-restricted-enforce

#### Implementation Status: implemented

______________________________________________________________________
