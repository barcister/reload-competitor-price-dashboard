from services.collector.connectors.backmarket_ch import BackMarketCHConnector
from services.collector.connectors.digitec_secondhand import DigitecSecondhandConnector
from services.collector.connectors.galaxus_refurbished import GalaxusRefurbishedConnector
from services.collector.connectors.mediamarkt_refurbished import MediaMarktRefurbishedConnector
from services.collector.connectors.refurbed_ch import RefurbedCHConnector
from services.collector.connectors.revendo import RevendoConnector

CONNECTOR_REGISTRY = {
    "revendo": RevendoConnector,
    "refurbed_ch": RefurbedCHConnector,
    "backmarket_ch": BackMarketCHConnector,
    "digitec_secondhand": DigitecSecondhandConnector,
    "galaxus_refurbished": GalaxusRefurbishedConnector,
    "mediamarkt_refurbished": MediaMarktRefurbishedConnector,
}
