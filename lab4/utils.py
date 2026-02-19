"""
LAB 4: Utility classes for FIPA-ACL communication
"""

from datetime import datetime
from spade.message import Message


class Performative:
    """Standard FIPA-ACL performatives used in this system."""
    INFORM = "inform"       # Sharing information
    REQUEST = "request"     # Requesting an action
    AGREE = "agree"         # Agreeing to perform action
    REFUSE = "refuse"       # Refusing to perform action


class MessageLogger:
    """Simple logger for ACL messages."""
    
    @staticmethod
    def log(agent_name: str, direction: str, msg: Message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        perf = msg.get_metadata("performative") or "unknown"
        sender = str(msg.sender).split("@")[0] if msg.sender else "?"
        receiver = str(msg.to).split("@")[0] if msg.to else "?"
        
        if direction == "SENT":
            print(f"📤 [{timestamp}] {agent_name} → {receiver}")
        else:
            print(f"📥 [{timestamp}] {sender} → {agent_name}")
        
        print(f"   Performative: {perf.upper()}")
        print(f"   Content: {msg.body[:60]}..." if len(msg.body) > 60 else f"   Content: {msg.body}")

