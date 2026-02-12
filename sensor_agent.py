import asyncio
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


DEFAULT_LOGFILE = "disaster_events.log"


def setup_logger(logfile: str = DEFAULT_LOGFILE) -> logging.Logger:
    logger = logging.getLogger("sensor_agent")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = RotatingFileHandler(logfile, maxBytes=100_000, backupCount=2)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger


class SensorAgent:
    def __init__(self, queue: asyncio.Queue, logger: Optional[logging.Logger] = None):
        self.queue = queue
        self.logger = logger or setup_logger()
        self.running = False

    async def monitor_once(self, timeout: float = 1.0):        
        try:
            ev = await asyncio.wait_for(self.queue.get(), timeout)
           
            self.logger.info(f"EVENT type={ev['type']} severity={ev['severity']} location={ev['location']} id={ev['id']}")
            
            print(f"[Sensor] Detected {ev['type']} severity={ev['severity']} at {ev['location']}")
            return ev
        except asyncio.TimeoutError:
            
            return None

    async def monitor(self, cycles: int = 10, timeout: float = 0.5):
        self.running = True
        for _ in range(cycles):
            await self.monitor_once(timeout=timeout)
        self.running = False


async def demo_run(duration: float = 5.0):

    from disaster_environment import Environment

    q = asyncio.Queue()
    env = Environment(seed=1, base_probability=0.4)
    sensor = SensorAgent(q)

    
    env_task = asyncio.create_task(env.run(q, interval=0.5, duration=duration))
    sensor_task = asyncio.create_task(sensor.monitor(cycles=int(duration / 0.5) + 2, timeout=0.6))

    await asyncio.gather(env_task, sensor_task)


if __name__ == "__main__":
    asyncio.run(demo_run())
