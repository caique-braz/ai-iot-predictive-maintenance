"""Rule-based predictive maintenance prototype for ERPNext/Frappe.

Academic prototype based on the final undergraduate project
"IA e IoT Aplicado em Manutenção Preditiva e Segurança de Dados na Indústria 4.0".

The repository version uses three operational states documented in the final
test scenarios: Ok, Alerta and Manutenção.
"""

from datetime import datetime

import frappe


# Thresholds aligned with the final documented test scenarios.
#
# Alert boundaries are evidenced by Scenario 1:
# - Temperature: 74.9 -> Ok / 75.1 -> Alerta
# - Pressure: 89.8 -> Ok / 90.2 -> Alerta
# - Vibration: 11.9 -> Ok / 12.1 -> Alerta
#
# Maintenance boundaries for pressure and vibration are consistent with the
# critical values documented in the TCC. The temperature maintenance boundary
# (85 °C) is a repository parameter inferred from the final classifications
# (78 °C -> Alerta and 88 °C -> Manutenção), because the exact boundary is not
# explicitly stated in the academic document.
THRESHOLDS = {
    "Temperatura": {
        "alert": 75.0,
        "maintenance": 85.0,
    },
    "Pressão": {
        "alert": 90.0,
        "maintenance": 100.0,
    },
    "Vibração": {
        "alert": 12.0,
        "maintenance": 15.0,
    },
}


def classify_sensor(sensor_type: str, value: float) -> str | None:
    """Classify a supported sensor reading.

    Returns:
        "Ok", "Alerta", "Manutenção" or None for unsupported sensor types.
    """
    limits = THRESHOLDS.get(sensor_type)

    if limits is None:
        return None

    if value >= limits["maintenance"]:
        return "Manutenção"

    if value >= limits["alert"]:
        return "Alerta"

    return "Ok"


def get_sensor_readings():
    """Retrieve sensor readings stored in the SensorLeitura DocType."""
    readings = frappe.get_all(
        "SensorLeitura",
        fields=[
            "name",
            "valor_da_leitura",
            "tipo_do_sensor",
            "data_hora",
            "unidade",
        ],
    )

    if not readings:
        frappe.throw("Nenhuma leitura de sensor foi encontrada.")

    return readings


def create_predictive_maintenance_record(reading, status: str, scenario: str):
    """Create one ManutencaoPreditiva record from a sensor reading."""
    maintenance = frappe.get_doc(
        {
            "doctype": "ManutencaoPreditiva",
            "id_do_sensor": reading["name"],
            "datahora_da_analise": datetime.now(),
            "valor_avaliado": reading["valor_da_leitura"],
            "status_previsto": status,
            "comentario": (
                f"Análise do sensor {reading['tipo_do_sensor']} "
                f"no cenário {scenario}"
            ),
        }
    )

    maintenance.insert(ignore_permissions=True)


def create_audit_log(scenario: str, status: str = "Ok"):
    """Register an execution in the LogExecucaoIA DocType."""
    log = frappe.new_doc("LogExecucaoIA")
    log.data_hora_execucao = datetime.now()
    log.usuario = frappe.session.user
    log.cenario = scenario
    log.status = status
    log.insert()


def simulate_predictive_maintenance(scenario: str = "default"):
    """Run the rule-based predictive-maintenance workflow."""
    processed_readings = 0

    try:
        readings = get_sensor_readings()

        for reading in readings:
            sensor_type = reading["tipo_do_sensor"]
            value = reading["valor_da_leitura"]

            status = classify_sensor(sensor_type, value)

            if status is None:
                continue

            create_predictive_maintenance_record(
                reading=reading,
                status=status,
                scenario=scenario,
            )

            processed_readings += 1

        create_audit_log(
            scenario=scenario,
            status="Ok",
        )

        frappe.db.commit()

        print(
            "Simulação concluída com sucesso. "
            f"{processed_readings} leituras processadas."
        )

    except Exception as error:
        frappe.db.rollback()

        try:
            create_audit_log(
                scenario=scenario,
                status="Erro",
            )
            frappe.db.commit()
        except Exception:
            frappe.db.rollback()

        frappe.throw(
            f"Erro durante a manutenção preditiva: {error}"
        )
