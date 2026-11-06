#!/usr/bin/env python3
"""Script do Kill Switch de Faturamento.

Desvincula o projeto da conta de faturamento do GCP caso qualquer
cobrança seja detectada acima de R$ 0,00 pelo orçamento de segurança.
"""
import base64
import json
import logging
import sys

from googleapiclient import discovery
import google.auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("billing-kill-switch")

PROJECT_ID = "agente-estudos-513901"


def unlink_billing_account(project_id: str = PROJECT_ID):
    """Desvincula a conta de faturamento do projeto."""
    credentials, _ = google.auth.default()
    billing_service = discovery.build("cloudbilling", "v1", credentials=credentials)
    project_name = f"projects/{project_id}/billingInfo"
    
    logger.warning("ALERTA DE SEGURANÇA: Desvinculando faturamento de %s...", project_id)
    billing_info = billing_service.projects().updateBillingInfo(
        name=project_name,
        body={"billingAccountName": ""}
    ).execute()
    
    logger.info("Faturamento desativado com sucesso. Status atual: %s", billing_info)
    return billing_info


def handle_pubsub_message(event, context=None):
    """Manipulador de eventos do Pub/Sub do Cloud Billing Budget."""
    pubsub_data = base64.b64decode(event.get("data", "")).decode("utf-8")
    data = json.loads(pubsub_data)
    
    cost_amount = float(data.get("costAmount", 0.0))
    logger.info("Notificação de orçamento recebida: Custo atual = R$ %.4f", cost_amount)
    
    if cost_amount > 0.0:
        logger.error("Custo detectado acima de R$ 0,00! Ativando Kill Switch...")
        unlink_billing_account()
    else:
        logger.info("Custo dentro do limite gratuito (R$ 0,00). Nenhuma ação necessária.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--trigger-now":
        unlink_billing_account()
    else:
        print("Uso: python billing_kill_switch.py [--trigger-now]")
