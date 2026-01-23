"""
Service Connectors - Bridge between voice agent and backend modules
"""

from voice_agent.connectors.financial_connector import FinancialTrackingConnector, get_financial_connector
from voice_agent.connectors.collaborative_connector import CollaborativeFarmingConnector, get_collaborative_connector
from voice_agent.connectors.inventory_connector import InventoryConnector, get_inventory_connector
from voice_agent.connectors.alerts_connector import AlertsConnector, get_alerts_connector

__all__ = [
    "FinancialTrackingConnector",
    "CollaborativeFarmingConnector",
    "InventoryConnector",
    "AlertsConnector",
    "get_financial_connector",
    "get_collaborative_connector",
    "get_inventory_connector",
    "get_alerts_connector",
]
