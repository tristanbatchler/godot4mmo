import logging
from typing import Optional
from server.protocol.states import ProtocolState

class ProtocolLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        protocol_ident: int = self.extra.get('ident', -1)
        protocol_state: Optional[ProtocolState] = self.extra.get('state', None)
        return f"[#{protocol_ident:04d}][{protocol_state}] {msg}", kwargs