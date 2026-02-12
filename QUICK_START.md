# Lab 4 Quick Start Guide

## Overview
This project implements agent communication using FIPA-ACL with the SPADE framework.

## Files Included

| File | Purpose |
|------|---------|
| `sender_agent.py` | Sends INFORM and REQUEST messages |
| `receiver_agent.py` | Receives messages and sends responses |
| `main.py` | Orchestrates both agents |
| `message_logger.py` | Logging utilities for ACL messages |
| `README.md` | Detailed project documentation |
| `LAB_REPORT.md` | Complete lab report with analysis |
| `sample_communication_log.json` | Example of message log output |
| `requirements.txt` | Python dependencies |

## Prerequisites ✅
- Python 3.8+ (system has 3.12)
- Virtual environment with SPADE installed (already done)

## How to Run

### Step 1: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 2: Run the Demo
```bash
python3 main.py
```

Or use direct path:
```bash
./venv/bin/python3 main.py
```

### Step 3: View Output
The script will show:
- Agent startup messages
- INFORM message sent and received
- ACK response from receiver
- REQUEST message sent and received
- Diagnostics report response
- Communication summary

## Expected Runtime
- **Duration**: ~15 seconds
- **Messages**: 6 total (2 INFORM, 2 REQUEST, 2 responses)
- **Output**: Console logs + JSON message history

## Message Flow

```
[Sender Agent]                    [Receiver Agent]
      |                                  |
      |---- INFORM (system status) ----->|
      |                                  |
      |<--- ACK (acknowledgement) -------|
      |                                  |
      |---- REQUEST (diagnostics) ----->|
      |                                  |
      |<--- REPORT (diagnostics data) ---|
      |                                  |
```

## Performatives Used

### 1. INFORM
- **Definition**: Sends information to another agent
- **Example**: "System status is operational"
- **Usage in Code**:
```python
msg = Message(to=receiver_jid)
msg.set_metadata("performative", "inform")
msg.body = "Information content here"
```

### 2. REQUEST
- **Definition**: Asks another agent to perform an action
- **Example**: "Please provide diagnostics report"
- **Usage in Code**:
```python
msg = Message(to=receiver_jid)
msg.set_metadata("performative", "request")
msg.body = "Action request content here"
```

## Key Implementation Points

✅ **FIPA-ACL Compliant**: Messages use standard ACL format
✅ **Performative-based**: Different handlers for INFORM vs REQUEST
✅ **Message Logging**: All messages logged with timestamps
✅ **Async/Await**: Non-blocking concurrent operations
✅ **Error Handling**: Graceful shutdown and error management

## Troubleshooting

### Issue: "No module named 'spade'"
**Solution**: Activate virtual environment first
```bash
source venv/bin/activate
```

### Issue: Nothing happens for a while
**Don't worry!** The agents need time to:
1. Initialize XMPP connections
2. Register on localhost
3. Set up communication channels

Just wait 2-3 seconds and you'll see output.

### Issue: Script hangs
**Solution**: Press Ctrl+C to stop
```bash
Ctrl+C
```

## File Examination

### To see agent code:
```bash
cat sender_agent.py
cat receiver_agent.py
```

### To see complete report:
```bash
cat LAB_REPORT.md
```

### To see message format:
```bash
cat sample_communication_log.json
```

## Deliverables Checklist

✅ **Agent Communication Code**
  - sender_agent.py: Sends INFORM and REQUEST
  - receiver_agent.py: Processes and responds
  - main.py: Orchestration

✅ **Message Logs**
  - Console output with timestamps
  - JSON message history (sample_communication_log.json)
  - Message logger utilities (message_logger.py)

✅ **Documentation**
  - README.md: Technical documentation
  - LAB_REPORT.md: Complete analysis
  - This quick start guide

## Next Steps

1. **Run the demo**: `python3 main.py`
2. **Review the output**: Check console messages
3. **Examine code**: Read sender_agent.py and receiver_agent.py
4. **Read report**: Check LAB_REPORT.md for detailed analysis
5. **Extend**: Try adding more agents or performatives

---

**Ready to go!** Run `./venv/bin/python3 main.py` to see agents communicate.
