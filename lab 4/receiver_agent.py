"""
Receiver Agent - Lab 4: Agent Communication using FIPA-ACL
Receives and responds to INFORM and REQUEST messages
"""

import asyncio
import logging
from datetime import datetime
from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ReceiverAgent")


class ReceiverAgent(agent.Agent):
    """Receiver Agent that processes INFORM and REQUEST messages"""

    class ReceiveBehaviour(CyclicBehaviour):
        """Behaviour to receive and process messages"""

        def __init__(self, agent):
            super().__init__()
            self.agent = agent
            self.message_count = 0

        async def run(self):
            msg = await self.receive(timeout=10)
            
            if msg:
                self.message_count += 1
                sender = msg.sender
                performative = msg.metadata.get("performative", "unknown")
                content = msg.body
                
                logger.info("=" * 60)
                logger.info(f"MESSAGE #{self.message_count} RECEIVED")
                logger.info("=" * 60)
                logger.info(f"[FROM] {sender}")
                logger.info(f"[PERFORMATIVE] {performative.upper()}")
                logger.info(f"[CONTENT] {content}")
                logger.info(f"[TIMESTAMP] {datetime.now().isoformat()}")
                
                # Handle INFORM performative
                if performative == "inform":
                    logger.info("[ACTION] Processing INFORM message...")
                    await self.handle_inform(sender, content)
                
                # Handle REQUEST performative
                elif performative == "request":
                    logger.info("[ACTION] Processing REQUEST message...")
                    await self.handle_request(sender, content)
                
                logger.info()
            else:
                logger.debug("No message received (timeout)")

        async def handle_inform(self, sender, content):
            """Handle INFORM messages"""
            logger.info("[INFORM] Information received and acknowledged")
            
            # Send acknowledgement reply
            reply = Message(to=sender)
            reply.set_metadata("performative", "inform")
            reply.body = f"Acknowledgement: Received your information - '{content}'"
            
            logger.info(f"[REPLY] Sending INFORM acknowledgement to {sender}")
            logger.info(f"[REPLY] Content: {reply.body}")
            
            await self.send(reply)
            logger.info("[REPLY] Acknowledgement sent\n")

        async def handle_request(self, sender, content):
            """Handle REQUEST messages"""
            logger.info("[REQUEST] Request received, generating response...")
            
            # Generate a response to the request
            response_content = self.generate_diagnostics_report()
            
            # Send response back
            reply = Message(to=sender)
            reply.set_metadata("performative", "inform")
            reply.body = response_content
            
            logger.info(f"[REPLY] Sending diagnostics report to {sender}")
            logger.info(f"[REPLY] Content:\n{response_content}")
            
            await self.send(reply)
            logger.info("[REPLY] Report sent\n")

        def generate_diagnostics_report(self):
            """Generate a mock diagnostics report"""
            report = """
SYSTEM DIAGNOSTICS REPORT
=========================
- CPU Usage: 45%
- Memory Usage: 62%
- Network Status: OK
- Disk Space: 87GB available
- System Uptime: 48 hours
- All Services: OPERATIONAL
            """
            return report.strip()

    async def setup(self):
        """Initialize the receiver agent"""
        logger.info("Receiver Agent starting up...")
        logger.info("Waiting for incoming messages...\n")
        b = self.ReceiveBehaviour(self)
        self.add_behaviour(b)
