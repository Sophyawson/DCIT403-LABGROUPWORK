"""
LAB 4: Communicating Rescue Agent
Extends Lab 3's RescueAgent with FIPA-ACL messaging capability.
"""

import asyncio
import json
import random
import warnings

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

# Import from this package
from .utils import Performative, MessageLogger

warnings.filterwarnings('ignore')


class CommunicatingRescueAgent(Agent):
    """
    Extended RescueAgent that receives REQUEST messages and responds
    with AGREE or REFUSE. Uses RescueGoals from Lab 3.
    """
    
    class HandleRequestBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.tasks_handled = 0
            self.is_busy = False
        
        async def run(self):
            agent_name = str(self.agent.jid).split("@")[0]
            
            # Wait for REQUEST message
            msg = await self.receive(timeout=10)
            
            if msg:
                MessageLogger.log(agent_name, "RECEIVED", msg)
                
                # Parse the task
                task = json.loads(msg.body)
                sender_jid = str(msg.sender)
                
                # Show which Lab 3 goals were assigned
                print(f"   Goals from Lab 3: {task.get('goals', [])}")
                
                # Decide whether to accept (80% chance if not busy)
                if not self.is_busy and random.random() > 0.2:
                    # Send AGREE
                    response = Message(to=sender_jid)
                    response.set_metadata("performative", Performative.AGREE)
                    response.set_metadata("ontology", "disaster-response")
                    response.body = f"Accepting task with goals: {task.get('goals', [])}"
                    
                    await self.send(response)
                    print(f"   ✅ [{agent_name}] Agreed to task\n")
                    
                    # Simulate doing the work
                    self.is_busy = True
                    self.tasks_handled += 1
                    await asyncio.sleep(1)
                    self.is_busy = False
                else:
                    # Send REFUSE
                    response = Message(to=sender_jid)
                    response.set_metadata("performative", Performative.REFUSE)
                    response.set_metadata("ontology", "disaster-response")
                    response.body = "Currently busy with another task"
                    
                    await self.send(response)
                    print(f"   ❌ [{agent_name}] Refused task (busy)\n")
            
            # Stop after handling enough requests
            if self.tasks_handled >= 3:
                await asyncio.sleep(2)
                print(f"🚑 [{agent_name}] Completed {self.tasks_handled} rescue tasks")
                self.kill()
                await self.agent.stop()
    
    async def setup(self):
        agent_name = str(self.jid).split("@")[0]
        print(f"🚀 [{agent_name}] Rescue agent started")
        
        # Template for REQUEST messages
        request_template = Template()
        request_template.set_metadata("performative", Performative.REQUEST)
        
        behaviour = self.HandleRequestBehaviour()
        self.add_behaviour(behaviour, request_template)

