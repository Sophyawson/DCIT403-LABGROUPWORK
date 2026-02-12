import asyncio
import random
from pathlib import Path
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.container import run_container

# Log file path (lab3/execution_trace.txt)
LOG_PATH = Path(__file__).parent / "execution_trace.txt"


def log(msg: str):
    print(msg, flush=True)
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception as e:
        print(f"Failed to write log: {e}", flush=True)

class IdleState(State):
    async def run(self):
        log("State: IDLE - waiting for sensor event")
        await asyncio.sleep(0.5)
        severity = random.choice(["Low", "Medium", "High", "Critical"])
        log(f"Sensor event severity: {severity}")
        if severity in ["High", "Critical"]:
            self.set_next_state("RESCUING")
        else:
            self.set_next_state("IDLE")

class RescuingState(State):
    async def run(self):
        log("State: RESCUING - performing rescue")
        await asyncio.sleep(2)
        log("Rescue actions completed")
        self.set_next_state("COMPLETED")

class CompletedState(State):
    async def run(self):
        log("State: COMPLETED - mission finished")
        await asyncio.sleep(0.2)
        self.set_next_state("IDLE")

class RescueAgent(Agent):
    async def setup(self):
        log("RescueAgent starting...")
        fsm = FSMBehaviour()
        fsm.add_state(name="IDLE", state=IdleState(), initial=True)
        fsm.add_state(name="RESCUING", state=RescuingState())
        fsm.add_state(name="COMPLETED", state=CompletedState())
        fsm.add_transition(source="IDLE", dest="RESCUING")
        fsm.add_transition(source="IDLE", dest="IDLE")
        fsm.add_transition(source="RESCUING", dest="COMPLETED")
        fsm.add_transition(source="COMPLETED", dest="IDLE")
        self.add_behaviour(fsm)

async def main():
    agent = RescueAgent("rescue@localhost", "password")
    await agent.start(auto_register=True)
    await asyncio.sleep(10)
    await agent.stop()

if __name__ == "__main__":
    run_container(main(), embedded_xmpp_server=True)
