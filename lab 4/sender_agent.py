"""
Sender Agent - Lab 4: Agent Communication using FIPA-ACL
Sends INFORM and REQUEST messages to the Receiver Agent
"""

import asyncio
import logging
from datetime import datetime
from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SenderAgent")


class SenderAgent(agent.Agent):
    """Sender Agent that initiates communication with INFORM and REQUEST messages"""

    class SendBehaviour(OneShotBehaviour):
        """Behaviour to send messages"""

        async def run(self):
            receiver_jid = "receiver@localhost"
            
            # Send INFORM message
            logger.info("=" * 60)
            logger.info("SENDING INFORM MESSAGE")
            logger.info("=" * 60)
            
            inform_msg = Message(to=receiver_jid)
            inform_msg.set_metadata("performative", "inform")
            inform_msg.body = "System status is operational. All systems functioning normally."
            
            logger.info(f"[INFORM] To: {receiver_jid}")
            logger.info(f"[INFORM] Content: {inform_msg.body}")
            logger.info(f"[INFORM] Timestamp: {datetime.now().isoformat()}")
            
            await self.send(inform_msg)
            logger.info("[INFORM] Message sent successfully\n")
            
            # Wait briefly before sending REQUEST
            await asyncio.sleep(2)
            
            # Send REQUEST message
            logger.info("=" * 60)
            logger.info("SENDING REQUEST MESSAGE")
            logger.info("=" * 60)
            
            request_msg = Message(to=receiver_jid)
            request_msg.set_metadata("performative", "request")
            request_msg.body = "Please provide system diagnostics report"
            
            logger.info(f"[REQUEST] To: {receiver_jid}")
            logger.info(f"[REQUEST] Content: {request_msg.body}")
            logger.info(f"[REQUEST] Timestamp: {datetime.now().isoformat()}")
            
            await self.send(request_msg)
            logger.info("[REQUEST] Message sent successfully\n")
            
            # Wait to receive responses
            await asyncio.sleep(5)

    async def setup(self):
        """Initialize the sender agent"""
        logger.info("Sender Agent starting up...")
        b = self.SendBehaviour()
        self.add_behaviour(b)
