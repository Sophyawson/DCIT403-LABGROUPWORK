import asyncio
import random
import time
import uuid
from typing import Optional, Dict

EVENT_TYPES = ["Earthquake", "Flood", "Fire", "Landslide"]
LOCATIONS = [
    "Madina",
    "Circle",
    "Teshie",
    "Krofrom",
    "Ashtown",
    "Kantamanto",
    "Nima",
]


class Environment:
    def __init__(self, seed: Optional[int] = None, base_probability: float = 0.2):
        self.rand = random.Random(seed)
        self.base_probability = base_probability

    def generate_event(self) -> Optional[Dict]:
        if self.rand.random() > self.base_probability:
            return None

        ev_type = self.rand.choice(EVENT_TYPES)
        severity = self.rand.randint(1, 5)
        location = self.rand.choice(LOCATIONS)
        event = {
            "id": str(uuid.uuid4()),
            "type": ev_type,
            "severity": severity,
            "location": location,
            "timestamp": time.time(),
        }
        return event

    async def run(self, queue: asyncio.Queue, interval: float = 1.0, duration: Optional[float] = None):
        start = time.time()
        while True:
            ev = self.generate_event()
            if ev:
                await queue.put(ev)
            if duration is not None and (time.time() - start) >= duration:
                break
            await asyncio.sleep(interval)


if __name__ == "__main__":
    # demo when run directly
    async def demo():
        q = asyncio.Queue()
        env = Environment(seed=42, base_probability=0.5)
        async def consumer():
            for _ in range(5):
                ev = await q.get()
                print(ev)
        await asyncio.gather(env.run(q, interval=0.1, duration=1.0), consumer())

    asyncio.run(demo())
