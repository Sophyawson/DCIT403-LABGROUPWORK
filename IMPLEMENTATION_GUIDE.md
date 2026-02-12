# Implementation Guide - FIPA-ACL Agent Communication

## Code Architecture Deep Dive

### 1. Sender Agent Architecture

#### Class Structure
```python
class SenderAgent(agent.Agent):
    """Inherits from SPADE Agent base class"""
    
    class SendBehaviour(OneShotBehaviour):
        """Inner class handling message sending"""
        
        async def run(self):
            # Message creation and sending logic
            pass
    
    async def setup(self):
        """Agent initialization"""
        pass
```

#### Behavior Types
- **OneShotBehaviour**: Executes once then completes
- **Use Case**: Sending finite sequence of messages
- **Advantage**: Simple, lightweight, no polling

#### Implementation Details

**Step 1: Message Creation**
```python
inform_msg = Message(to=receiver_jid)
inform_msg.set_metadata("performative", "inform")
inform_msg.body = "System status is operational..."
```
- `Message`: SPADE message object
- `to`: Receiver JID (agent@server)
- `performative`: Communication intent
- `body`: Message content

**Step 2: Message Sending**
```python
await self.send(inform_msg)
```
- Async operation (non-blocking)
- Returns immediately
- Actual transmission happens asynchronously

**Step 3: Timing Control**
```python
await asyncio.sleep(2)
```
- Pause between different message types
- Ensures receiver processing time
- Demonstrates sequential communication

**Step 4: Logging**
```python
logger.info(f"[INFORM] To: {receiver_jid}")
logger.info(f"[INFORM] Content: {inform_msg.body}")
logger.info(f"[INFORM] Timestamp: {datetime.now().isoformat()}")
```
- Records outgoing messages
- Timestamp for synchronization
- Enables message reconstruction

---

### 2. Receiver Agent Architecture

#### Class Structure
```python
class ReceiverAgent(agent.Agent):
    """Inherits from SPADE Agent base class"""
    
    class ReceiveBehaviour(CyclicBehaviour):
        """Inner class handling message reception"""
        
        async def run(self):
            # Message receiving and processing logic
            pass
        
        async def handle_inform(self, sender, content):
            # INFORM processing
            pass
        
        async def handle_request(self, sender, content):
            # REQUEST processing
            pass
```

#### Behavior Types
- **CyclicBehaviour**: Repeats until agent stops
- **Use Case**: Continuous listening
- **Advantage**: Responsive, handles multiple messages

#### Implementation Details

**Step 1: Message Reception**
```python
msg = await self.receive(timeout=10)
```
- Blocks until message received (or timeout)
- Timeout prevents indefinite blocking
- Returns None if timeout expires
- Async: doesn't block event loop

**Step 2: Message Parsing**
```python
performative = msg.metadata.get("performative")
sender = msg.sender
content = msg.body
```
- Extract metadata
- Identify message type
- Parse content

**Step 3: Performative-Based Routing**
```python
if performative == "inform":
    await self.handle_inform(sender, content)
elif performative == "request":
    await self.handle_request(sender, content)
```
- Route to appropriate handler
- Different logic per performative
- Scalable to many performative types

**Step 4: Response Generation**
```python
reply = Message(to=sender)
reply.set_metadata("performative", "inform")
reply.body = response_content
await self.send(reply)
```
- Create response message
- Set performative (usually "inform" for responses)
- Send back to original sender

#### Handler: handle_inform()
```python
async def handle_inform(self, sender, content):
    logger.info("[INFORM] Information received and acknowledged")
    
    # Create acknowledgement
    reply = Message(to=sender)
    reply.set_metadata("performative", "inform")
    reply.body = f"Acknowledgement: Received your information - '{content}'"
    
    await self.send(reply)
```
- Logs reception
- Creates confirmation message
- Sends acknowledgement back

#### Handler: handle_request()
```python
async def handle_request(self, sender, content):
    logger.info("[REQUEST] Request received, generating response...")
    
    # Generate response data
    response_content = self.generate_diagnostics_report()
    
    # Create and send response
    reply = Message(to=sender)
    reply.set_metadata("performative", "inform")
    reply.body = response_content
    
    await self.send(reply)
```
- Logs request reception
- Generates response content
- Sends result back
- Note: Response uses "inform" performative

#### Generator: generate_diagnostics_report()
```python
def generate_diagnostics_report(self):
    """Simulate retrieving system data"""
    report = """
SYSTEM DIAGNOSTICS REPORT
=========================
- CPU Usage: 45%
- Memory Usage: 62%
...
    """
    return report.strip()
```
- Encapsulates business logic
- Separates data generation from messaging
- Can be replaced with real system calls

---

### 3. Message Exchange Protocol

#### INFORM Message Flow
```
Timeline    Sender                          Receiver
=========   ======                          ========
T=0         Create INFORM(status)
            Send INFORM ──────────────────>
                                           Run receive()
                                           Parse performative="inform"
                                           handle_inform() called
                                           Create ACK reply
                                           Send reply ─────────────────>
T=0.5       Receive reply
            Parse performative="inform"
```

#### REQUEST Message Flow
```
Timeline    Sender                          Receiver
=========   ======                          ========
T=2         Create REQUEST(diagnostics)
            Send REQUEST ──────────────────>
                                           Run receive()
                                           Parse performative="request"
                                           handle_request() called
                                           Generate diagnostics
                                           Create response
                                           Send response ────────────────>
T=2.5       Receive response
            Parse performative="inform"
```

---

### 4. Async/Await Pattern

#### Key Principles
1. **Non-blocking I/O**: Network calls don't freeze execution
2. **Concurrent Operations**: Multiple agents run simultaneously
3. **Event Loop**: Single-threaded concurrent execution

#### Code Examples

**Blocking vs Non-blocking**
```python
# ❌ BLOCKING (would freeze entire system)
import time
time.sleep(2)  # Entire event loop blocked

# ✅ NON-BLOCKING (other agents continue)
await asyncio.sleep(2)  # Other tasks continue
```

**Message Operations**
```python
# Send (returns immediately)
await self.send(msg)

# Receive (awaits until message or timeout)
msg = await self.receive(timeout=10)
```

#### Event Loop
```python
async def main():
    # Create agents
    sender = SenderAgent(...)
    receiver = ReceiverAgent(...)
    
    # Start both concurrently
    await receiver.start()      # Non-blocking
    await sender.start()        # Non-blocking
    
    # Both run simultaneously in event loop
    await asyncio.sleep(15)
    
    # Stop both
    await sender.stop()
    await receiver.stop()

# Run event loop
asyncio.run(main())
```

---

### 5. Logging Mechanism

#### Configuration
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SenderAgent")
```

#### Log Levels
- **DEBUG**: Detailed technical information
- **INFO**: General informational messages ✅ Used here
- **WARNING**: Warning messages (not used)
- **ERROR**: Error messages (not used)

#### Logging Patterns

**Outgoing Message**
```python
logger.info(f"[INFORM] To: {receiver_jid}")
logger.info(f"[INFORM] Content: {inform_msg.body}")
logger.info(f"[INFORM] Timestamp: {datetime.now().isoformat()}")
```

**Incoming Message**
```python
logger.info(f"[FROM] {sender}")
logger.info(f"[PERFORMATIVE] {performative.upper()}")
logger.info(f"[CONTENT] {content}")
logger.info(f"[TIMESTAMP] {datetime.now().isoformat()}")
```

**Action Triggers**
```python
logger.info("[ACTION] Processing INFORM message...")
logger.info("[REPLY] Sending acknowledgement to {sender}")
```

---

### 6. Message Format Compliance

#### FIPA-ACL Compliance
```python
# Standard FIPA-ACL message
Message {
    sender: "sender@localhost",
    receiver: "receiver@localhost",
    performative: "inform",
    content: "System status is operational",
    metadata: {
        "performative": "inform"  # For compatibility
    }
}
```

#### SPADE Implementation
```python
msg = Message(to="receiver@localhost")
msg.set_metadata("performative", "inform")
msg.body = "System status is operational"
```

---

### 7. Error Handling

#### Try-Catch Pattern (in main.py)
```python
try:
    await receiver.start(auto_register=False)
    await sender.start(auto_register=False)
    
    await asyncio.sleep(15)
    
    await sender.stop()
    await receiver.stop()
    
except Exception as e:
    logger.error(f"Error during agent communication: {e}")
    raise
finally:
    logger.info("Main process finished.")
```

#### Timeout Handling (in receiver)
```python
msg = await self.receive(timeout=10)

if msg:
    # Process message
else:
    # Timeout - no message received
    logger.debug("No message received (timeout)")
```

---

### 8. Extensibility Points

#### Adding New Performatives
```python
# In receiver_agent.py ReceiveBehaviour.run()

elif performative == "agree":
    await self.handle_agree(sender, content)

elif performative == "refuse":
    await self.handle_refuse(sender, content)

# Add new handlers
async def handle_agree(self, sender, content):
    # Implementation
    pass

async def handle_refuse(self, sender, content):
    # Implementation
    pass
```

#### Adding More Agents
```python
# In main.py

agent1 = Agent1("agent1@localhost", "password")
agent2 = Agent2("agent2@localhost", "password")
agent3 = Agent3("agent3@localhost", "password")

await agent1.start()
await agent2.start()
await agent3.start()
```

#### Custom Message Processing
```python
# Replace generate_diagnostics_report() with real system calls

def generate_diagnostics_report(self):
    import psutil  # Real system monitoring
    
    report = f"""
CPU: {psutil.cpu_percent()}%
Memory: {psutil.virtual_memory().percent}%
Disk: {psutil.disk_usage('/').percent}%
    """
    return report
```

---

## Summary

The implementation demonstrates:

1. **Sender-Receiver Pattern**: Asymmetric communication roles
2. **FIPA-ACL Compliance**: Standard message format
3. **Performative Routing**: Different handlers per message type
4. **Async Concurrency**: Non-blocking message exchange
5. **Comprehensive Logging**: Message tracking and debugging
6. **Error Handling**: Graceful failure management
7. **Extensibility**: Easy to add agents and performatives

This architecture serves as a foundation for building more complex multi-agent systems with standardized communication protocols.
