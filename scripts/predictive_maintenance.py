"""Rule-based predictive maintenance prototype for ERPNext/Frappe.

Academic prototype based on the final undergraduate project
"IA e IoT Aplicado em Manutenção Preditiva e Segurança de Dados na Indústria 4.0".
"""

from datetime import datetime

import frappe


THRESHOLDS = {
    "Temperatura": 70.0,
    "Pressão": 120.0,
    "Vibração": 15.0,
}


def classify_sensor(sensor_type: str, value: float) -> str | None:
    """Classify a supported sensor reading as ``Ok`` or ``Alerta``."""
    limit = THRESHOLDS.get(sensor_type)
    if limit is None:
        return None
    return "Ok" if value < limit else "Alerta"


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

            create_predictive_maintenance_record(reading, status, scenario)
            processed_readings += 1

        create_audit_log(scenario=scenario, status="Ok")
        frappe.db.commit()

        print(
            "Simulação concluída com sucesso. "
            f"{processed_readings} leituras processadas."
        )

    except Exception as error:
        frappe.db.rollback()

        try:
            create_audit_log(scenario=scenario, status="Erro")
            frappe.db.commit()
        except Exception:
            frappe.db.rollback()

        frappe.throw(f"Erro durante a manutenção preditiva: {error}")
