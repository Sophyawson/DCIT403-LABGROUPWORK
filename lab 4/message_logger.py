"""
Message Logger - Lab 4: Agent Communication using FIPA-ACL
Utilities for logging and storing agent communication messages
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ACLMessageLogger:
    """Logger for FIPA-ACL messages with file persistence"""
    
    def __init__(self, log_file: str = "agent_communication_log.json"):
        """Initialize the message logger
        
        Args:
            log_file: Path to JSON file for storing message logs
        """
        self.log_file = Path(log_file)
        self.messages: List[Dict] = []
        self.logger = logging.getLogger(__name__)
    
    def log_message(self, sender: str, receiver: str, performative: str, 
                   content: str, message_type: str = "outgoing"):
        """Log an ACL message
        
        Args:
            sender: Sender agent JID
            receiver: Receiver agent JID
            performative: Message performative (inform, request, etc.)
            content: Message body content
            message_type: "outgoing" or "incoming"
        """
        message_record = {
            "timestamp": datetime.now().isoformat(),
            "type": message_type,
            "sender": sender,
            "receiver": receiver,
            "performative": performative.upper(),
            "content": content
        }
        
        self.messages.append(message_record)
        self.logger.debug(f"Logged {message_type} message from {sender}")
    
    def save_logs(self):
        """Save all logged messages to JSON file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.messages, f, indent=2)
            self.logger.info(f"Messages saved to {self.log_file}")
        except Exception as e:
            self.logger.error(f"Failed to save logs: {e}")
    
    def get_summary(self) -> Dict:
        """Get a summary of communication statistics
        
        Returns:
            Dictionary with communication summary
        """
        summary = {
            "total_messages": len(self.messages),
            "outgoing": sum(1 for m in self.messages if m["type"] == "outgoing"),
            "incoming": sum(1 for m in self.messages if m["type"] == "incoming"),
            "by_performative": {},
            "unique_senders": set(),
            "unique_receivers": set()
        }
        
        # Count by performative
        for msg in self.messages:
            perf = msg["performative"]
            summary["by_performative"][perf] = summary["by_performative"].get(perf, 0) + 1
            summary["unique_senders"].add(msg["sender"])
            summary["unique_receivers"].add(msg["receiver"])
        
        summary["unique_senders"] = list(summary["unique_senders"])
        summary["unique_receivers"] = list(summary["unique_receivers"])
        
        return summary
    
    def print_summary(self):
        """Print a formatted summary of communication"""
        summary = self.get_summary()
        
        print("\n" + "=" * 70)
        print("COMMUNICATION SUMMARY")
        print("=" * 70)
        print(f"Total Messages: {summary['total_messages']}")
        print(f"Outgoing: {summary['outgoing']}")
        print(f"Incoming: {summary['incoming']}")
        print(f"\nPerformatives Used:")
        for perf, count in summary['by_performative'].items():
            print(f"  - {perf}: {count}")
        print(f"\nParticipating Agents:")
        print(f"  Senders: {', '.join(summary['unique_senders'])}")
        print(f"  Receivers: {', '.join(summary['unique_receivers'])}")
        print("=" * 70 + "\n")


# Global logger instance
message_logger = ACLMessageLogger()
