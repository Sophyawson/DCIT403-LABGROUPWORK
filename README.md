# Lab 4: Agent Communication Using FIPA-ACL

## Objective
Enable inter-agent communication using the Foundation for Intelligent Physical Agents – Agent Communication Language (FIPA-ACL) protocol.

## Background
Coordination in multi-agent systems depends on standardized message exchange. FIPA-ACL provides a standard format for agent communications, enabling heterogeneous agents to communicate effectively regardless of their implementation details.

### Key Concepts
- **FIPA-ACL**: Agent Communication Language standard for inter-agent messaging
- **Performatives**: Communication actions (e.g., `inform`, `request`, `agree`, `refuse`)
- **Agents**: Autonomous entities that can send and receive messages
- **Message Exchange**: Asynchronous communication between agents

## Project Structure

```
.
├── sender_agent.py       # Sender agent implementation
├── receiver_agent.py     # Receiver agent implementation  
├── main.py              # Main script to run both agents
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Files Description

### `sender_agent.py`
- **Purpose**: Initiates communication by sending both INFORM and REQUEST messages
- **Performatives Used**:
  - `INFORM`: Sends status information to receiver
  - `REQUEST`: Requests a diagnostics report from receiver
- **Features**:
  - OneShotBehaviour to send messages
  - Logs all outgoing messages with timestamps
  - Waits for responses

### `receiver_agent.py`
- **Purpose**: Receives and processes incoming messages
- **Performatives Handled**:
  - `INFORM`: Acknowledges information and sends acknowledgement
  - `REQUEST`: Processes request and sends diagnostics report
- **Features**:
  - CyclicBehaviour to continuously listen for messages
  - Message parsing and performative-based action triggering
  - Automatic response generation
  - Comprehensive message logging

### `main.py`
- **Purpose**: Orchestrates both agents in a unified communication session
- **Features**:
  - Async event loop management
  - Agent lifecycle management (start/stop)
  - Communication session timing
  - Error handling and graceful shutdown

## FIPA-ACL Message Format

Each ACL message contains:
- **Sender**: Agent identifier (JID) of the sender
- **Receiver**: Agent identifier (JID) of the receiver
- **Performative**: Communication action (e.g., inform, request)
- **Content**: Message body with actual information
- **Metadata**: Additional properties (e.g., performative type)

### Example Message Structure
```
Message:
  Sender: sender@localhost
  Receiver: receiver@localhost
  Performative: inform
  Content: "System status is operational"
```

## Performatives Used

### 1. INFORM
- **Purpose**: Send information to another agent
- **Usage**: "I am informing you that X is true"
- **Response**: Acknowledgement or processing notification

### 2. REQUEST
- **Purpose**: Ask another agent to perform an action
- **Usage**: "I request that you perform action X"
- **Response**: Result of requested action or refusal

## How to Run

### Prerequisites
- Python 3.8+
- Virtual environment setup (already completed)

### Installation
```bash
# Already done - SPADE is installed in venv
# If needed, install dependencies:
pip install spade
```

### Run the Complete Communication System
```bash
# Using virtual environment
./venv/bin/python3 main.py

# Or if activated:
source venv/bin/activate
python3 main.py
```

### Run Individual Agents (for testing)
```bash
# Run sender only
./venv/bin/python3 sender_agent.py

# Run receiver only
./venv/bin/python3 receiver_agent.py
```

## Expected Output

When you run `main.py`, you should see:

```
2026-02-12 ... - Main - INFO - LAB 4: AGENT COMMUNICATION USING FIPA-ACL
2026-02-12 ... - Main - INFO - Starting Multi-Agent Communication System...
2026-02-12 ... - ReceiverAgent - INFO - Receiver Agent starting up...
2026-02-12 ... - SenderAgent - INFO - Sender Agent starting up...
2026-02-12 ... - SenderAgent - INFO - SENDING INFORM MESSAGE
2026-02-12 ... - SenderAgent - INFO - [INFORM] To: receiver@localhost
2026-02-12 ... - SenderAgent - INFO - [INFORM] Content: System status is operational...
...
2026-02-12 ... - ReceiverAgent - INFO - MESSAGE #1 RECEIVED
2026-02-12 ... - ReceiverAgent - INFO - [FROM] sender@localhost
2026-02-12 ... - ReceiverAgent - INFO - [PERFORMATIVE] INFORM
...
```

## Message Logs

All messages are logged with timestamps in the console output. For persistent logging, you can redirect the output:

```bash
./venv/bin/python3 main.py > communication_log.txt 2>&1
```

## Key Features Implemented

✅ **ACL Message Exchange**: Agents send and receive FIPA-ACL formatted messages
✅ **INFORM Performative**: Status information exchange with acknowledgements
✅ **REQUEST Performative**: Request-response communication pattern
✅ **Message Parsing**: Incoming messages are parsed by performative type
✅ **Action Triggering**: Different actions triggered based on message performative
✅ **Message Logging**: All messages logged with sender, receiver, content, and timestamps
✅ **Error Handling**: Graceful handling of communication errors

## Communication Flow Diagram

```
Sender Agent              Receiver Agent
     |                         |
     |----[INFORM]---->       |
     |                    [Process INFORM]
     |                    [Generate ACK]
     |<---[ACK Result]----|    |
     |                         |
    [Wait 2 seconds]           |
     |                         |
     |----[REQUEST]---->       |
     |                    [Process REQUEST]
     |                    [Generate Report]
     |<---[Report]--------|    |
     |                         |
```

## Troubleshooting

### "No module named 'spade'"
Make sure you're using the virtual environment:
```bash
source venv/bin/activate
python3 main.py
```

### Messages not being received
- Check that both agents are using the same JID domain (localhost)
- Ensure no firewall is blocking communication
- Verify XMPP connectivity (if using external XMPP server)

### Agents hang during communication
- Press Ctrl+C to interrupt
- The script includes a timeout to prevent indefinite blocking

## Future Enhancements

1. **Multiple Agents**: Extend to 3+ agents with pub-sub patterns
2. **External XMPP Server**: Configure with real XMPP server (ejabberd, etc.)
3. **Message Persistence**: Store all messages in database
4. **Web Dashboard**: Real-time visualization of agent communication
5. **Advanced Performatives**: Implement agree, refuse, not-understood
6. **Authentication**: Add agent authentication and encryption

## References

- [FIPA ACL Message Structure](http://www.fipa.org/specs/fipa00061/SC00061G.html)
- [SPADE Framework Documentation](https://github.com/jacintosd/spade)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)