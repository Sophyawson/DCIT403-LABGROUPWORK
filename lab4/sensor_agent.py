"""
LAB 4: Communicating Sensor Agent
Extends Lab 2's SensorAgent with FIPA-ACL messaging capability.
"""

import asyncio
import json
import warnings
from datetime import datetime

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

# Import from Lab 2
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sensor_agent import DisasterEnvironment, EnvironmentState

# Import from this package
from .utils import Performative, MessageLogger

warnings.filterwarnings('ignore')


class CommunicatingSensorAgent(Agent):
    """
    Extended SensorAgent that uses DisasterEnvironment from Lab 2
    and sends INFORM messages to the CoordinatorAgent.
    """
    
    class SenseAndReportBehaviour(OneShotBehaviour):
        """
        Uses DisasterEnvironment from Lab 2 to sense conditions,
        then sends INFORM messages to coordinator.
        """
        
        def __init__(self, coordinator_jid: str, environment: DisasterEnvironment, num_readings: int = 3):
            super().__init__()
            self.coordinator_jid = coordinator_jid
            self.env = environment
            self.num_readings = num_readings
        
        async def run(self):
            agent_name = str(self.agent.jid).split("@")[0]
            print(f"\n🔍 [{agent_name}] Starting disaster monitoring...")
            
            for i in range(self.num_readings):
                await asyncio.sleep(2)
                
                # Use Lab 2's environment to get state
                state: EnvironmentState = self.env.step()
                
                # Convert to event data for messaging
                event = {
                    "reading_id": i + 1,
                    "damage_severity": state.damage_severity,
                    "water_level": state.water_level,
                    "fire_risk": state.fire_risk,
                    "is_accessible": state.is_accessible,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                
                # Create INFORM message (FIPA-ACL)
                msg = Message(to=self.coordinator_jid)
                msg.set_metadata("performative", Performative.INFORM)
                msg.set_metadata("ontology", "disaster-response")
                msg.set_metadata("message_id", f"reading-{i+1}")
                msg.body = json.dumps(event)
                
                await self.send(msg)
                MessageLogger.log(agent_name, "SENT", msg)
                print(f"   Environment: Damage={state.damage_severity}, Water={state.water_level:.2f}m, Fire={state.fire_risk}\n")
            
            print(f"🔍 [{agent_name}] Monitoring complete, sent {self.num_readings} readings")
            await asyncio.sleep(2)
            await self.agent.stop()
    
    async def setup(self):
        agent_name = str(self.jid).split("@")[0]
        print(f"🚀 [{agent_name}] Sensor agent started")
        
        
        env = DisasterEnvironment()
        
        behaviour = self.SenseAndReportBehaviour(
            coordinator_jid="coordinator@localhost",
            environment=env,
            num_readings=3
        )
        self.add_behaviour(behaviour)

