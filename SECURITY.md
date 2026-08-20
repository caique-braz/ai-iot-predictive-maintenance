# Security

This document summarizes the security controls implemented in the academic prototype and clarifies the security scope of this repository.

## Project Scope

This repository represents an **academic prototype and laboratory environment** developed for predictive maintenance using ERPNext/Frappe, simulated sensor data, a rule-based expert system and information-security controls.

The implementation was designed for controlled development and testing. It should **not be considered production-ready** without additional validation, hardening and infrastructure controls.

---

## Implemented Security Controls

### Role-Based Access Control

ERPNext permissions were configured according to user responsibilities.

The project uses different profiles, including:

- Operator
- Maintenance Technician
- AI Analyst
- Supervisor

The goal is to restrict access according to each role's operational responsibilities and reduce the risk of unauthorized actions.

---

### Input Validation

Sensor data is validated before being processed by the predictive-maintenance logic.

Validation is intended to reduce risks related to:

- Invalid formats
- Unexpected values
- Incorrect measurement units
- Duplicate or inconsistent records
- Corrupted sensor data

Because the expert system relies directly on sensor readings, data integrity is essential for reliable classifications.

---

### Audit Logging

Automated executions are recorded through the custom ERPNext DocType:

```text
LogExecucaoIA
```

Audit records include information such as:

- Execution date and time
- Responsible user
- Simulation scenario
- Execution status

This provides traceability and supports review of automated decisions.

---

### Network Access Restriction

The development environment uses `iptables` to restrict access to the ERPNext service.

The laboratory configuration allows TCP port `8000` from localhost and rejects other incoming connections to that port:

```bash
sudo iptables -A INPUT -p tcp --dport 8000 -s 127.0.0.1 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000 -j REJECT
```

This reduces exposure of the ERPNext development service to unauthorized external access.

The corresponding firewall screenshot is available at:

```text
images/security/iptables-rules.png
```

---

## Credential Handling

Credentials must not be hard-coded in scripts committed to this repository.

The ERPNext installation script was adjusted so that passwords are requested during execution instead of being stored directly in the source code.

Sensitive files such as environment-variable files should remain outside version control.

Examples:

```text
.env
.env.*
```

---

## Repository Security Practices

The repository uses a `.gitignore` file to reduce the risk of accidentally committing:

- Environment-variable files
- Logs
- Virtual environments
- IDE configuration files
- Generated ERPNext/Frappe files

Before each commit, review the staged files with:

```bash
git status
git diff --staged
```

---

## Known Limitations

The current implementation has important limitations:

- Sensor datasets are simulated.
- The expert system uses predefined rules rather than a trained machine-learning model.
- The environment was developed for academic testing.
- The firewall configuration is limited to the laboratory scenario.
- No production-grade network segmentation or monitoring was implemented.
- No physical IoT sensors were used in the final prototype.
- Production deployment would require additional authentication, encryption, monitoring, backup, patch-management and infrastructure-hardening measures.

---

## Future Security Improvements

Possible improvements include:

- Stronger authentication mechanisms
- Encrypted communication between sensors and servers
- Network segmentation
- Improved firewall policies
- Centralized security monitoring
- Automated security logging and alerting
- Secure secret management
- Periodic vulnerability assessment
- Physical IoT device authentication
- Production hardening of ERPNext/Frappe
- Continuous review of access permissions

---

## Academic Context

The security controls documented here are based on the final undergraduate project:

**IA e IoT Aplicado em Manutenção Preditiva e Segurança de Dados na Indústria 4.0**

Information Security Technology  
FATEC Americana — Ministro Ralph Biasi  
2025
