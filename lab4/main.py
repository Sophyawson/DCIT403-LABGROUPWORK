"""
LAB 4: Main Entry Point
========================
Runs the FIPA-ACL communication demo with all agents.

Usage:
    python agents/lab4/main.py
    OR
    python -m agents.lab4.main (from project root)
"""

import asyncio
import warnings

import spade

# Import agents from this package
from .sensor_agent import CommunicatingSensorAgent
from .coordinator_agent import CoordinatorAgent
from .rescue_agent import CommunicatingRescueAgent

warnings.filterwarnings('ignore')


async def main():
    print(f"\n{'='*60}")
    print("   SPADE FIPA-ACL Communication - Lab 4")
    print(f"{'='*60}")
    print()
    print("FIPA-ACL Performatives Used:")
    print("   • INFORM  - Sensor reports disaster readings")
    print("   • REQUEST - Coordinator assigns rescue tasks")
    print("   • AGREE   - Rescue agent accepts task")
    print("   • REFUSE  - Rescue agent declines task")
    print(f"{'='*60}\n")
    
    # Create agents
    rescue = CommunicatingRescueAgent("rescue@localhost", "290405")
    coordinator = CoordinatorAgent("coordinator@localhost", "290405")
    sensor = CommunicatingSensorAgent("sensor@localhost", "290405")
    
    try:
        # Start agents in order (receivers first)
        await rescue.start(auto_register=True)
        await asyncio.sleep(0.5)
        
        await coordinator.start(auto_register=True)
        await asyncio.sleep(0.5)
        
        await sensor.start(auto_register=True)
        
        # Wait for all agents to complete
        while sensor.is_alive() or coordinator.is_alive() or rescue.is_alive():
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        for agent in [sensor, coordinator, rescue]:
            if agent.is_alive():
                await agent.stop()
        
        print(f"\n{'='*60}")
        print("   MESSAGE LOG SUMMARY")
        print(f"{'='*60}")
        print("   SensorAgent → CoordinatorAgent : INFORM (sensor readings)")
        print("   CoordinatorAgent → RescueAgent : REQUEST (rescue tasks)")
        print("   RescueAgent → CoordinatorAgent : AGREE/REFUSE (responses)")
        print(f"{'='*60}")
        print("\n✅ All agents stopped")


if __name__ == "__main__":
    spade.run(main())

