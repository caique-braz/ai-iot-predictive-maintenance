# AI & IoT Predictive Maintenance

Academic and practical project focused on the integration of **Artificial Intelligence (AI)**, **Internet of Things (IoT)** and **Information Security** for predictive maintenance in an Industry 4.0 environment.

This project was developed as the final undergraduate project for the **Information Security Technology** program at FATEC Americana.

## Project Overview

The project investigates how AI and IoT technologies can support predictive maintenance in industrial environments.

A functional prototype was developed using **ERPNext/Frappe**, where simulated sensor readings are stored and analyzed by a **rule-based expert system implemented in Python**. The system evaluates equipment conditions, identifies abnormal readings, creates predictive-maintenance records and keeps audit logs of automated executions.

Information security is part of the implementation through role-based access control, input validation, execution auditing and network-access restrictions.

## Architecture

```text
Simulated IoT Sensor Data
          |
          v
     ERPNext / Frappe
          |
          v
      SensorLeitura
          |
          v
 Python Expert System
          |
          v
    Rule Evaluation
          |
      +---+---+
      |       |
      v       v
     OK     ALERT
      |       |
      +---+---+
          |
          v
 ManutencaoPreditiva
          |
          +--> Predictive maintenance records
          |
          +--> LogExecucaoIA (audit trail)
```

## Rule-Based Expert System

The predictive analysis uses fixed expert-system rules rather than a trained machine-learning model. This approach was selected because the academic prototype did not have a sufficiently large historical dataset for supervised training.

The current prototype thresholds are centralized in the Python code:

| Sensor type | Alert threshold |
| --- | ---: |
| Temperature | `>= 70` |
| Pressure | `>= 120` |
| Vibration | `>= 15` |

These values represent the prototype configuration used by the implementation and can be adjusted for other test environments.

## ERPNext Integration

### `SensorLeitura`

Custom DocType used to store sensor readings, including:

- Sensor identifier
- Sensor type
- Reading value
- Measurement unit
- Date and time
- Status

### `ManutencaoPreditiva`

Custom DocType used to store predictive-analysis results, including:

- Related sensor
- Analysis timestamp
- Evaluated value
- Predicted status
- Analysis comments

The Python script retrieves records from `SensorLeitura`, evaluates each supported sensor and creates the corresponding `ManutencaoPreditiva` record.

### `LogExecucaoIA`

Custom DocType used to preserve execution traceability. Logs include information such as execution timestamp, user, scenario and execution status.

## Information Security

### Role-Based Access Control

ERPNext permissions were configured for different responsibilities, including:

- Operator
- Maintenance Technician
- AI Analyst
- Supervisor

The goal is to limit each role to the permissions necessary for its responsibilities.

### Data Validation

The project considers validation of formats, expected ranges, measurement units and duplicate data to reduce the risk of inconsistent information affecting automated analysis.

### Audit Logging

Automated analyses are recorded so previous executions and decisions can be reviewed.

### Network Access Restriction

In the laboratory environment, `iptables` rules were used to restrict access to the ERPNext development port:

```bash
sudo iptables -A INPUT -p tcp --dport 8000 -s 127.0.0.1 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000 -j REJECT
```

These rules were designed for the controlled development environment and are not a complete production firewall policy.

## Test Scenarios

Three simulated scenarios were used to validate the rule-based workflow:

### Scenario 1 — Sensor Instability

Small variations around expected operating values were used to evaluate whether the system could distinguish acceptable fluctuations from alert conditions.

### Scenario 2 — Mixed States

Normal and abnormal readings were combined to test classification under different equipment conditions in the same dataset.

### Scenario 3 — Multiple Failures

Multiple abnormal readings were introduced within a short period to evaluate the system response to simultaneous failure conditions.

## Results

The prototype demonstrated the complete workflow from sensor data to automated analysis and maintenance registration:

```text
Sensor Data
    |
    v
ERPNext
    |
    v
Expert-System Analysis
    |
    v
Equipment Classification
    |
    v
Predictive Maintenance Record
    |
    v
Audit Log
```

The experiments demonstrated:

- Automated processing of simulated sensor data
- Classification of supported sensor readings
- Detection of abnormal conditions according to defined rules
- Automatic creation of predictive-maintenance records
- Integration between Python and ERPNext/Frappe
- Execution audit logging
- Role-based access controls
- Network-access restrictions in the laboratory environment

## Technologies

- Python
- ERPNext
- Frappe Framework
- MariaDB
- Ubuntu Linux
- VirtualBox
- Bash
- iptables
- Redis
- Node.js
- Yarn
- IoT concepts
- Artificial Intelligence
- Expert Systems
- Information Security

## Repository Structure

```text
.
├── README.md
├── docs/
│   └── tcc.pdf
├── scripts/
│   ├── install_erpnext.sh
│   └── predictive_maintenance.py
├── data/
├── images/
├── .gitignore
└── LICENSE
```

## Security Improvements Applied to the Public Repository

The GitHub version differs slightly from the original academic appendix to make the public code safer and clearer:

- Hard-coded database and administrator passwords were removed.
- Passwords are requested interactively during setup.
- The predictive-maintenance field name was normalized to `valor_avaliado`.
- The related sensor field was aligned with the documented `id_do_sensor` field.
- Sensor thresholds were centralized in one configuration dictionary.
- Error handling includes rollback behavior before logging failures.
- Generated Frappe files, logs and local secrets are excluded through `.gitignore`.

## Future Improvements

- Replace fixed expert-system rules with supervised machine-learning models
- Use real historical sensor datasets
- Integrate physical IoT sensors
- Implement anomaly detection
- Create interactive monitoring dashboards
- Automate periodic predictive analysis
- Improve real-time data collection
- Expand security controls for production environments

Possible future approaches include decision trees, neural networks, logistic regression, clustering and other anomaly-detection techniques.

## Project Scope

This repository represents an **academic prototype and laboratory environment**.

The sensor datasets used during the experiments were simulated. The virtual machine, ERPNext configuration and firewall rules were designed for a controlled development environment. A real industrial deployment would require additional validation, security hardening, infrastructure planning and integration with physical sensors.

## Academic Project

**IA e IoT Aplicado em Manutenção Preditiva e Segurança de Dados na Indústria 4.0**  
Information Security Technology — FATEC Americana  
2025

The complete academic document is available in [`docs/tcc.pdf`](docs/tcc.pdf).

## Author

**Caique Martins Braz**

Information Security Technology — FATEC Americana
