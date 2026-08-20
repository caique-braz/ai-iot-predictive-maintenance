# Setup Guide

This guide explains how to reproduce the **academic development environment** used by the AI & IoT Predictive Maintenance project.

> **Important**
>
> This repository represents a laboratory prototype. The installation script and configuration are intended for a controlled Ubuntu development environment and are not a production deployment guide.

---

## 1. Environment Used in the Project

The practical implementation was developed in an Ubuntu virtual machine using Oracle VM VirtualBox.

The academic environment used:

- Ubuntu 64-bit
- 2 GB RAM
- 25 GB virtual disk
- NAT network adapter
- ERPNext / Frappe
- MariaDB
- Python
- Redis
- Node.js
- Yarn

The repository installation script pins the Frappe/ERPNext branch to:

```text
version-14
```

and Node.js to:

```text
18
```

---

## 2. Clone the Repository

Inside the Ubuntu environment, clone the repository:

```bash
git clone https://github.com/<your-github-username>/ai-iot-predictive-maintenance.git
cd ai-iot-predictive-maintenance
```

If you already downloaded the project, simply open a terminal inside the repository folder.

---

## 3. ERPNext Installation

The repository includes:

```text
scripts/install_erpnext.sh
```

The script installs and configures the main dependencies required by the academic environment, including:

- Python development packages
- MariaDB
- Redis
- NVM
- Node.js 18
- Yarn
- Bench CLI
- Frappe
- ERPNext

### Make the Script Executable

```bash
chmod +x scripts/install_erpnext.sh
```

### Run the Installer

```bash
./scripts/install_erpnext.sh
```

During installation, the script requests:

- MariaDB root password
- ERPNext Administrator password

Passwords are intentionally **not hard-coded** in the repository.

The default site created by the script is:

```text
meu_site.local
```

---

## 4. Start ERPNext

After installation:

```bash
cd ~/frappe-bench
bench start
```

The development server is expected to be available at:

```text
http://localhost:8000
```

---

## 5. Required Custom DocTypes

The predictive-maintenance script depends on three custom DocTypes.

### 5.1 SensorLeitura

Create a DocType named:

```text
SensorLeitura
```

Suggested fields based on the academic prototype:

| Label | Field Name | Type |
| --- | --- | --- |
| ID do Sensor | `id_do_sensor` | Data |
| Tipo do Sensor | `tipo_do_sensor` | Select |
| Valor da Leitura | `valor_da_leitura` | Float |
| Unidade | `unidade` | Data |
| Data/Hora da Leitura | `data_hora` | Datetime |
| Status | `status` | Select |

The sensor-type field should support:

```text
Temperatura
Pressão
Vibração
```

The original project also considered additional sensor categories in the ERP structure, but the predictive-maintenance script processes the three types above.

Screenshots of the configuration are available in:

```text
images/erpnext/
```

---

### 5.2 ManutencaoPreditiva

Create a DocType named:

```text
ManutencaoPreditiva
```

Required fields:

| Label | Field Name | Type |
| --- | --- | --- |
| ID do Sensor | `id_do_sensor` | Link |
| Data/Hora da Análise | `datahora_da_analise` | Datetime |
| Valor Avaliado | `valor_avaliado` | Float |
| Status Previsto | `status_previsto` | Select |
| Comentário | `comentario` | Small Text |

Configure `id_do_sensor` to reference:

```text
SensorLeitura
```

The repository version of the prototype uses these predicted states:

```text
Ok
Alerta
Manutenção
```

---

### 5.3 LogExecucaoIA

Create a DocType named:

```text
LogExecucaoIA
```

Required fields used by the Python script:

| Label | Field Name |
| --- | --- |
| Data/Hora da Execução | `data_hora_execucao` |
| Usuário | `usuario` |
| Cenário | `cenario` |
| Status | `status` |

This DocType provides traceability for the automated analysis.

The repository script may write:

```text
Ok
Erro
```

to the execution-status field.

---

## 6. Import the Test Datasets

Three CSV datasets are included in:

```text
data/
```

```text
scenario-1-sensor-instability.csv
scenario-2-mixed-states.csv
scenario-3-multiple-failures.csv
```

They represent:

1. Sensor instability near operational thresholds
2. Mixed operational states
3. Multiple failures in a short period

Import the desired CSV into the `SensorLeitura` DocType using ERPNext's data-import functionality.

### CSV Field Mapping

Map the CSV columns to the ERPNext fields as follows:

| CSV Column | ERPNext Field |
| --- | --- |
| ID do Sensor | `id_do_sensor` |
| Tipo do Sensor | `tipo_do_sensor` |
| Valor da Leitura | `valor_da_leitura` |
| Unidade | `unidade` |
| Data/Hora da Leitura | `data_hora` |
| Status | `status` |

---

## 7. Predictive-Maintenance Logic

The analysis implementation is located at:

```text
scripts/predictive_maintenance.py
```

It retrieves readings from `SensorLeitura`, applies the expert-system rules and creates records in `ManutencaoPreditiva`.

The repository version classifies readings into:

```text
Ok
Alerta
Manutenção
```

The configured thresholds are centralized in the Python file.

### Current Repository Thresholds

| Sensor | Alert | Maintenance |
| --- | ---: | ---: |
| Temperature | 75.0 °C | 85.0 °C |
| Pressure | 90.0 Pa | 100.0 Pa |
| Vibration | 12.0 mm/s | 15.0 mm/s |

> **Note about the temperature maintenance threshold**
>
> The final test results classify 78 °C as `Alerta` and 88 °C as `Manutenção`, but the exact transition value between these states is not explicitly documented in the academic text. The repository therefore uses **85 °C as a configurable prototype parameter** to reproduce the final classification behavior without presenting it as an experimentally established limit.

---

## 8. Running the Predictive Script

The Python implementation imports `frappe` and is designed to execute **inside a configured Frappe/ERPNext environment**.

The academic project documents the logic as being executed in the Frappe/ERPNext environment, either manually or through scheduling.

This repository currently provides the analysis script as source code, but it does **not yet package the function as an installable custom Frappe application**.

Before running it, ensure that:

- ERPNext is running
- The required DocTypes exist
- Sensor data has been imported
- The field names match the configuration in this guide
- The Python code is integrated into a Frappe execution context

Packaging the logic into a dedicated custom Frappe app is listed as a possible repository improvement.

---

## 9. Laboratory Firewall Configuration

The academic environment used `iptables` to restrict access to the ERPNext development service.

Allow localhost access to TCP port 8000:

```bash
sudo iptables -A INPUT -p tcp --dport 8000 -s 127.0.0.1 -j ACCEPT
```

Reject other incoming connections to the same port:

```bash
sudo iptables -A INPUT -p tcp --dport 8000 -j REJECT
```

Verify the rules:

```bash
sudo iptables -L -n -v
```

A screenshot of the laboratory configuration is available at:

```text
images/security/iptables-rules.png
```

> Applying these rules prevents other machines from accessing the ERPNext service on port 8000. Use them only when this behavior is appropriate for your test environment.

---

## 10. Validate the Environment

Before running an analysis, verify:

```bash
node --version
yarn --version
python3 --version
bench --version
```

Then confirm that ERPNext starts successfully:

```bash
cd ~/frappe-bench
bench start
```

Open:

```text
http://localhost:8000
```

Inside ERPNext, confirm that:

- `SensorLeitura` exists
- `ManutencaoPreditiva` exists
- `LogExecucaoIA` exists
- The selected CSV dataset was imported successfully

---

## 11. Repository Files Used During Setup

```text
.
├── scripts/
│   ├── install_erpnext.sh
│   └── predictive_maintenance.py
│
├── data/
│   ├── scenario-1-sensor-instability.csv
│   ├── scenario-2-mixed-states.csv
│   └── scenario-3-multiple-failures.csv
│
└── images/
    ├── erpnext/
    └── security/
```

---

## Troubleshooting

### `bench: command not found`

The installation script installs Bench for the current user and adds:

```bash
$HOME/.local/bin
```

to the current script environment.

If Bench is not found in a new terminal session, try:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

You can add this path to your shell configuration if necessary.

### ERPNext does not open on port 8000

Confirm that Bench is running:

```bash
cd ~/frappe-bench
bench start
```

Then verify the firewall rules:

```bash
sudo iptables -L -n -v
```

### CSV import fails

Verify that the ERPNext field names and data types match the mapping documented above.

Pay particular attention to:

- Datetime format
- Decimal values
- Sensor-type spelling
- Measurement units

---

## Security Notice

Do not commit real credentials, API keys, production data or `.env` files to the repository.

For additional security information, see:

```text
SECURITY.md
```

---

## Academic Context

This setup guide is based on the environment used for the final undergraduate project:

**IA e IoT Aplicado em Manutenção Preditiva e Segurança de Dados na Indústria 4.0**

Information Security Technology  
FATEC Americana — Ministro Ralph Biasi  
2025
