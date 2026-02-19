"""
LAB 4: Coordinator Agent
Receives INFORM from sensors, sends REQUEST to rescue agents.
"""

import asyncio
import json
import warnings

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

# Import from Lab 3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rescue_agent import RescueGoals

# Import from this package
from .utils import Performative, MessageLogger

warnings.filterwarnings('ignore')


class CoordinatorAgent(Agent):
    """
    CoordinatorAgent that receives INFORM messages from sensors
    and sends REQUEST messages to RescueAgents using Lab 3's goals.
    """
    
    class ReceiveAlertBehaviour(CyclicBehaviour):
        def __init__(self, rescue_jid: str):
            super().__init__()
            self.rescue_jid = rescue_jid
            self.alerts_received = 0
        
        async def run(self):
            agent_name = str(self.agent.jid).split("@")[0]
            
            # Wait for INFORM message from sensor
            msg = await self.receive(timeout=10)
            
            if msg:
                MessageLogger.log(agent_name, "RECEIVED", msg)
                self.alerts_received += 1
                
                # Parse the sensor reading
                reading = json.loads(msg.body)
                
                # Determine goals based on severity (using Lab 3's RescueGoals)
                if reading["damage_severity"] > 50 or reading["fire_risk"] > 50:
                    goals = [RescueGoals.SAVE_LIVES, RescueGoals.ASSESS_DAMAGE]
                    priority = "high"
                else:
                    goals = [RescueGoals.ASSESS_DAMAGE, RescueGoals.SECURE_AREA]
                    priority = "normal"
                
                # Create REQUEST message for rescue agent
                request_msg = Message(to=self.rescue_jid)
                request_msg.set_metadata("performative", Performative.REQUEST)
                request_msg.set_metadata("ontology", "disaster-response")
                request_msg.set_metadata("action", "rescue")
                
                task = {
                    "action": "respond_to_disaster",
                    "sensor_reading": reading,
                    "goals": goals,
                    "priority": priority
                }
                request_msg.body = json.dumps(task)
                
                await self.send(request_msg)
                MessageLogger.log(agent_name, "SENT", request_msg)
                print(f"   Goals assigned: {goals} ({priority} priority)\n")
            
            # Stop after receiving 3 alerts
            if self.alerts_received >= 3:
                await asyncio.sleep(3)
                print(f"📋 [{agent_name}] Processed all alerts, shutting down")
                self.kill()
                await self.agent.stop()
    
    class ReceiveResponseBehaviour(CyclicBehaviour):
        """Receives AGREE/REFUSE responses from RescueAgent."""
        
        async def run(self):
            agent_name = str(self.agent.jid).split("@")[0]
            msg = await self.receive(timeout=5)
            
            if msg:
                perf = msg.get_metadata("performative")
                sender = str(msg.sender).split("@")[0]
                
                if perf == Performative.AGREE:
                    print(f"✅ [{agent_name}] {sender} AGREED to task")
                elif perf == Performative.REFUSE:
                    print(f"❌ [{agent_name}] {sender} REFUSED task: {msg.body}")
    
    async def setup(self):
        agent_name = str(self.jid).split("@")[0]
        print(f"🚀 [{agent_name}] Coordinator agent started")
        
        # Template for INFORM messages from sensors
        inform_template = Template()
        inform_template.set_metadata("performative", Performative.INFORM)
        
        alert_behaviour = self.ReceiveAlertBehaviour("rescue@localhost")
        response_behaviour = self.ReceiveResponseBehaviour()
        
        self.add_behaviour(alert_behaviour, inform_template)
        self.add_behaviour(response_behaviour)

