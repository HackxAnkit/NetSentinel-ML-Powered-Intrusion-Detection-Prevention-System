## how to run
activate virtual environment
source venv/bin/activate 
cd backend
python3 main.py

cd frontend
npm run dev

# run sniffer to track threats
 sudo python core/sniffer.py
type password if prompted for mac user

1. curl -A "Nmap Scripting Engine" http://example.com
2. curl "http://example.com/../../etc/passwd"
3. curl "http://example.com/login?user=admin' OR '1'='1"

# Check dashboard
open http://localhost:5173/ in browser  

3 alerts pop up in 10 seconds

## About intrusion detection
how to check if it is working for any intrusion detection
To check if the Intrusion Detection System (IDS) is working, you'll need to run the packet sniffer and then simulate malicious network traffic. The system has built-in signatures to catch things like SQL injections, directory traversal attacks, and Nmap scans.

Here is a step-by-step guide to testing it:

Step 1: Start the Sniffer (Requires Root/Admin)
The core of the IDS is the sniffer.py script. It needs to monitor raw network traffic, which requires sudo privileges on macOS.

Open a terminal and navigate to your project's backend directory:
bash
cd "Documents/wipro project/backend"
Start the sniffer (you may be prompted for your Mac password):
bash
sudo python core/sniffer.py
(Note: By default, it listens on en0, which is typically your Wi-Fi interface on macOS. You should see "Starting packet capture on interface: en0")
Step 2: Trigger a Fake Attack
Open a new, separate terminal window and run one of these curl commands. These commands will send HTTP requests over your network containing payloads that match the IDS's threat signatures.

1. Simulate an Nmap Scan (Low Severity) By spoofing the User-Agent to look like the Nmap Scripting Engine, you'll trigger the SIG-005 rule:

bash
curl -A "Nmap Scripting Engine" http://example.com
2. Simulate a Directory Traversal Attack (Medium Severity) Sending a URL with ../.. will trigger the SIG-004 rule:

bash
curl "http://example.com/../../etc/passwd"
3. Simulate a SQL Injection (High Severity) Sending a classic SQL injection payload will trigger the SIG-001 rule:

bash
curl "http://example.com/login?user=admin' OR '1'='1"
Step 3: Verify the Detection
Check the Sniffer Terminal: Go back to the terminal where sniffer.py is running. You should immediately see a red alert printed out, something like:
text
[ALERT] LOW Threat detected! <Your_IP> -> 93.184.215.14 : Nmap User-Agent
[!] MALICIOUS PACKET: TCP <Your_IP>:<Port> -> 93.184.215.14:80 | Len: 134
Check the Dashboard: If you have your FastAPI server (python main.py) and Vite frontend (npm run dev) running, open your dashboard in the browser. You should see these alerts populate in real-time under the alerts table and stats!
9:40

## How to check the ids.db Database

To check the contents of your SQLite database (`ids.db`), you can use the built-in `sqlite3` command-line tool.

### 1. Open the Database
Navigate to your backend folder and open the database:
```bash
cd backend
sqlite3 ids.db
```

### 2. View the Tables
To see what tables exist in the database, type:
```sql
.tables
```
*(You should see `alerts`, `blocked_ips`, and `packets`)*

### 3. Run Queries to Check Data
Format the output to make it easier to read:
```sql
.mode column
.headers on
```

**View the last 5 alerts:**
```sql
SELECT timestamp, src_ip, threat_type, severity FROM alerts ORDER BY timestamp DESC LIMIT 5;
```

**View the last 5 packets captured:**
```sql
SELECT timestamp, src_ip, dst_ip, protocol, length FROM packets ORDER BY timestamp DESC LIMIT 5;
```

### 4. Exit the Database
When you are done looking around, exit the prompt by typing:
```sql
.quit
```
