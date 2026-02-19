"""
LAB 4: Agent Communication Using FIPA-ACL
==========================================
Package containing agents for inter-agent communication demo.

This lab builds upon:
- Lab 2: DisasterEnvironment, EnvironmentState (sensor_agent.py)
- Lab 3: RescueGoals (rescue_agent.py)
"""

from .utils import Performative, MessageLogger
from .sensor_agent import CommunicatingSensorAgent
from .coordinator_agent import CoordinatorAgent
from .rescue_agent import CommunicatingRescueAgent

__all__ = [
    "Performative",
    "MessageLogger",
    "CommunicatingSensorAgent",
    "CoordinatorAgent",
    "CommunicatingRescueAgent",
]

