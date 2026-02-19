"""
Main Script - Lab 4: Agent Communication using FIPA-ACL
Demonstrates FIPA-ACL message exchange between agents
"""

import asyncio
import logging
from datetime import datetime
from message_logger import ACLMessageLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FIPA-ACL-Demo")

# Create message logger
msg_logger = ACLMessageLogger("agent_communication_log.json")


class FIPAACLDemo:
    """Simulates FIPA-ACL message exchange between Sender and Receiver agents"""
    
    def __init__(self):
        self.sender_jid = "sender@localhost"
        self.receiver_jid = "receiver@localhost"
        self.message_count = 0
    
    async def send_inform_message(self):
        """Sender: Send INFORM message"""
        self.message_count += 1
        
        logger.info("=" * 70)
        logger.info(f"MESSAGE #{self.message_count}: SEND INFORM")
        logger.info("=" * 70)
        
        content = "System status is operational. All systems functioning normally."
        
        logger.info(f"From: {self.sender_jid}")
        logger.info(f"To: {self.receiver_jid}")
        logger.info(f"Performative: INFORM")
        logger.info(f"Content: {content}")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        
        # Log message
        msg_logger.log_message(self.sender_jid, self.receiver_jid, "inform", content, "outgoing")
        
        await asyncio.sleep(0.5)
    
    async def receive_inform_message(self):
        """Receiver: Receive and process INFORM message"""
        self.message_count += 1
        
        logger.info("=" * 70)
        logger.info(f"MESSAGE #{self.message_count}: RECEIVE INFORM")
        logger.info("=" * 70)
        
        content = "System status is operational. All systems functioning normally."
        
        logger.info(f"From: {self.sender_jid}")
        logger.info(f"To: {self.receiver_jid}")
        logger.info(f"Performative: INFORM")
        logger.info(f"Content: {content}")
        logger.info(f"[ACTION] Processing INFORM message...")
        
        # Log message
        msg_logger.log_message(self.sender_jid, self.receiver_jid, "inform", content, "incoming")
        
        await asyncio.sleep(0.5)
    
    async def send_inform_acknowledgement(self):
        """Receiver: Send acknowledgement"""
        self.message_count += 1
        
        logger.info("=" * 70)
        logger.info(f"MESSAGE #{self.message_count}: SEND ACK (INFORM)")
        logger.info("=" * 70)
        
        content = "Acknowledgement: Received your information - 'System status is operational...'"
        
        logger.info(f"From: {self.receiver_jid}")
        logger.info(f"To: {self.sender_jid}")
        logger.info(f"Performative: INFORM")
        logger.info(f"Content: {content}")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        
        # Log message
        msg_logger.log_message(self.receiver_jid, self.sender_jid, "inform", content, "outgoing")
        
        await asyncio.sleep(0.5)
    
    async def receive_acknowledgement(self):
        """Sender: Receive acknowledgement"""
        self.message_count += 1
        
        logger.info("=" * 70)
        logger.info(f"MESSAGE #{self.message_count}: RECEIVE ACK")
        logger.info("=" * 70)
        
        content = "Acknowledgement: Received your information - 'System status is operational...'"
        
        logger.info(f"From: {self.receiver_jid}")
        logger.info(f"To: {self.sender_jid}")
        logger.info(f"Performative: INFORM")
        logger.info(f"Content: {content}")
        
        # Log message
        msg_logger.log_message(self.receiver_jid, self.sender_jid, "inform", content, "incoming")
        
        await asyncio.sleep(1)  # Wait before next message
    
    async def send_request_message(self):
        """Sender: Send REQUEST message"""
        self.message_count += 1
        
        logger.info("=" * 70)
        logger.info(f"MESSAGE #{self.message_count}: SEND REQUEST")
        logger.info("=" * 70)
        
        content = "Please provide system diagnostics report"
        
        logger.info(f"From: {self.sender_jid}")
        logger.info(f"To: {self.receiver_jid}")
        logger.info(f"Performative: REQUEST")
        logger.info(f"Content: {content}")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        
        # Log message
        msg_logger.log_message(self.sender_jid, self.receiver_jid, "request", content, "outgoing")
        
        await asyncio.sleep(0.5)
    
    async def receive_request_message(self):
        """Receiver: Receive and process REQUEST message"""
        self.message_count += 1
        
        logger.info("=" * 70)
        logger.info(f"MESSAGE #{self.message_count}: RECEIVE REQUEST")
        logger.info("=" * 70)
        
        content = "Please provide system diagnostics report"
        
        logger.info(f"From: {self.sender_jid}")
        logger.info(f"To: {self.receiver_jid}")
        logger.info(f"Performative: REQUEST")
        logger.info(f"Content: {content}")
        logger.info(f"[ACTION] Processing REQUEST message...")
        logger.info(f"[ACTION] Generating diagnostics report...")
        
        # Log message
        msg_logger.log_message(self.sender_jid, self.receiver_jid, "request", content, "incoming")
        
        await asyncio.sleep(0.5)
    
    async def send_diagnostics_report(self):
        """Receiver: Send diagnostics report (response to REQUEST)"""
        self.message_count += 1
        
        logger.info("=" * 70)
        logger.info(f"MESSAGE #{self.message_count}: SEND DIAGNOSTICS REPORT")
        logger.info("=" * 70)
        
        report = """SYSTEM DIAGNOSTICS REPORT
=========================
- CPU Usage: 45%
- Memory Usage: 62%
- Network Status: OK
- Disk Space: 87GB available
- System Uptime: 48 hours
- All Services: OPERATIONAL"""
        
        logger.info(f"From: {self.receiver_jid}")
        logger.info(f"To: {self.sender_jid}")
        logger.info(f"Performative: INFORM")
        logger.info(f"Content:\n{report}")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        
        # Log message
        msg_logger.log_message(self.receiver_jid, self.sender_jid, "inform", report, "outgoing")
        
        await asyncio.sleep(0.5)
    
    async def receive_report(self):
        """Sender: Receive diagnostics report"""
        self.message_count += 1
        
        logger.info("=" * 70)
        logger.info(f"MESSAGE #{self.message_count}: RECEIVE REPORT")
        logger.info("=" * 70)
        
        report = """SYSTEM DIAGNOSTICS REPORT
=========================
- CPU Usage: 45%
- Memory Usage: 62%
- Network Status: OK
- Disk Space: 87GB available
- System Uptime: 48 hours
- All Services: OPERATIONAL"""
        
        logger.info(f"From: {self.receiver_jid}")
        logger.info(f"To: {self.sender_jid}")
        logger.info(f"Performative: INFORM")
        logger.info(f"Content:\n{report}")
        
        # Log message
        msg_logger.log_message(self.receiver_jid, self.sender_jid, "inform", report, "incoming")
    
    async def run(self):
        """Execute the FIPA-ACL communication sequence"""
        logger.info("\n" + "=" * 70)
        logger.info("LAB 4: AGENT COMMUNICATION USING FIPA-ACL")
        logger.info("=" * 70)
        logger.info("Simulating FIPA-ACL Message Exchange\n")
        
        # Message sequence: INFORM exchange
        await self.send_inform_message()
        await self.receive_inform_message()
        await self.send_inform_acknowledgement()
        await self.receive_acknowledgement()
        
        # Message sequence: REQUEST-INFORM exchange
        await self.send_request_message()
        await self.receive_request_message()
        await self.send_diagnostics_report()
        await self.receive_report()
        
        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("COMMUNICATION SUMMARY")
        logger.info("=" * 70)
        msg_logger.print_summary()
        
        # Save logs
        msg_logger.save_logs()
        logger.info("✅ Message logs saved to: agent_communication_log.json")


async def main():
    """Main entry point"""
    try:
        demo = FIPAACLDemo()
        await demo.run()
        logger.info("\n✅ Communication session completed successfully!")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        logger.info("Process finished.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nAgent communication interrupted by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
