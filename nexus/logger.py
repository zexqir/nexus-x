import logging
from pathlib import Path

def setup_logging(cfg):
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        filename="logs/nexus-x.log",
        level=getattr(logging, cfg.get("logging_level","INFO").upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
