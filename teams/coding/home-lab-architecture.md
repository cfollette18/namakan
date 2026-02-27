# 🏠 Distributed Home Lab Architecture Plan

**Date:** 2026-02-15  
**Status:** Draft for review  
**Team:** Home‑Lab Specialists (incorporating universal primitives & federated architecture insights)

## EXECUTIVE SUMMARY

We are building a **distributed AI inference and data platform** across four heterogeneous devices connected via Tailscale. This system enables low‑latency RAG workflows, centralized observability, and container‑based orchestration, all managed through OpenClaw node pairing. The architecture embraces **universal primitives** (Entity, Relationship, Event) for data modeling and **federated querying** to keep compute close to data—inspired by our team’s universal data cloud vision.

## 🎯 CORE VALUE PROPOSITION

1. **Distributed, not centralized:** LLM inference on Jetson, embeddings on Dell, logging on Pi 5, control plane on ThinkPad.
2. **Tailscale‑native networking:** Zero‑config secure overlay; each device is a peer.
3. **Production‑ready containerization:** Docker on every node; Portainer for visual management.
4. **Observability by design:** Grafana Loki stack aggregates logs; Prometheus metrics optional.
5. **RAG workflow end‑to‑end:** From embedding generation to vector search to LLM completion.
6. **Steve Jobs‑level simplicity:** One‑command deployment, automatic discovery, self‑healing.

## 🏗️ HIGH‑LEVEL ARCHITECTURE

### System Diagram
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ThinkPad (control plane)                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ OpenClaw Gateway              │ Docker Engine                     │   │
│  │ • Node pairing manager        │ • Development containers          │   │
│  │ • Remote exec orchestration   │ • Portainer agent                 │   │
│  │ • Git repository              │ • NFS client (mounts Dell share)  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │ Tailscale (100.x.y.z)
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Dell Laptop (embedding + vector DB)              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Embedding Service (FastAPI)        │ Zvec Vector DB                │   │
│  │ • Model: BAAI/bge‑large‑en‑v1.5    │ • Alibaba embedded vector DB  │   │
│  │ • REST /embed endpoint             │ • Persistent storage on NFS   │   │
│  │ • GPU acceleration (CUDA)          │ • Index on NVMe SSD           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ NFS Server                         │ Docker Engine                 │   │
│  │ • Exports /data/vectors            │ • Hosts embedding + Zvec      │   │
│  │ • Exports /data/models (optional)  │ • Portainer agent             │   │
│  │ • Tailscale IP: 100.x.y.z          │                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │ Tailscale (100.x.y.z)
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Jetson Orin Nano (LLM inference)                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Ollama Server                      │ Docker Engine                 │   │
│  │ • Multiple model support           │ • Runs ollama/ollama container│   │
│  │ • REST API (port 11434)            │ • NFS client (mounts Dell)    │   │
│  │ • GPU‑accelerated inference        │ • Portainer agent             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │ Tailscale (100.x.y.z)
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Raspberry Pi 5 (logging + monitoring)            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Grafana Loki Stack                 │ Portainer                     │   │
│  │ • Loki (log aggregation)           │ • Container management UI     │   │
│  │ • Alloy (log collection)           │ • Multi‑node dashboard        │   │
│  │ • Grafana (visualization)          │ • Health checks               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Innovations vs Traditional Homelab

1. **Federated compute:** Each device specializes—no single point of failure.
2. **Universal primitives for telemetry:** Logs, metrics, and traces modeled as Events and Entities.
3. **Zero‑trust overlay:** Tailscale provides mutual TLS; no port‑forwarding required.
4. **Container‑first:** Every service runs in Docker; Portainer gives a single pane of glass.
5. **Embedded vector DB:** Zvec runs on Dell’s NVMe SSD, offering high‑throughput similarity search.

## 📋 DEVICE ROLES & TAILSCALE ASSIGNMENTS

| Device           | Hostname      | Tailscale IP  | Role                                      | Specs (example)                 |
|------------------|---------------|---------------|-------------------------------------------|---------------------------------|
| ThinkPad         | thinkpad-lab  | 100.xx.xx.xx  | Control plane, development, OpenClaw gateway | x86_64, 16 GB RAM, 512 GB SSD   |
| Dell Laptop      | dell-embed    | 100.xx.xx.xx  | Embedding service, Zvec vector DB, NFS server | x86_64, 32 GB RAM, 1 TB NVMe, GPU |
| Jetson Orin Nano | jetson-llm    | 100.xx.xx.xx  | Reasoning model inference (Ollama)        | ARM64, 8 GB RAM, GPU (Jetson)   |
| Raspberry Pi 5   | pi5-monitor   | 100.xx.xx.xx  | Centralized logging, Portainer UI         | ARM64, 8 GB RAM, 128 GB microSD |

**Note:** Tailscale IPs are dynamic; use MagicDNS (`hostname.tailscale.ts.net`) for stable addressing.

## 🐳 CONTAINER DEFINITIONS PER NODE

### 1. ThinkPad (control plane)
```yaml
# docker-compose.thinkpad.yml
services:
  openclaw-gateway:
    image: openclaw/gateway:latest
    container_name: openclaw-gateway
    ports:
      - "8080:8080"          # Gateway API
      - "9090:9090"          # Optional metrics
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./openclaw/config:/config
    environment:
      - NODE_NAME=thinkpad-lab
      - TAILSCALE_AUTHKEY=${TAILSCALE_AUTHKEY}
    restart: unless-stopped

  portainer-agent:
    image: portainer/agent:latest
    container_name: portainer-agent
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/lib/docker/volumes:/var/lib/docker/volumes
    environment:
      - AGENT_CLUSTER_ADDR=tasks.portainer-agent
    networks:
      - portainer
    deploy:
      mode: global
```

### 2. Dell Laptop (embedding + vector DB)
```yaml
# docker-compose.dell.yml
services:
  embedding-service:
    build:
      context: ./embedding
      dockerfile: Dockerfile.cuda    # Use CUDA base image
    container_name: embedding-service
    ports:
      - "8000:8000"          # FastAPI endpoint
    volumes:
      - /data/models:/models        # Pre‑downloaded BAAI model
      - /data/vectors:/vectors      # Zvec data volume (NFS export)
    environment:
      - MODEL_NAME=BAAI/bge-large-en-v1.5
      - ZVEC_PATH=/vectors/zvec.db
      - CUDA_VISIBLE_DEVICES=0
    restart: unless-stopped

  zvec:
    image: alibaba/zvec:latest      # Placeholder; adjust as needed
    container_name: zvec
    volumes:
      - /data/vectors:/data
    ports:
      - "8081:8081"          # Vector DB REST API
    environment:
      - DATA_PATH=/data/zvec.db
      - MAX_DIM=1024
    restart: unless-stopped

  nfs-server:
    image: erichough/nfs-server:latest
    container_name: nfs-server
    volumes:
      - /data:/data
      - ./nfs/exports:/etc/exports.d
    ports:
      - "2049:2049"          # NFS
    cap_add:
      - SYS_ADMIN
    restart: unless-stopped

  portainer-agent:
    image: portainer/agent:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    # ... same as above
```

### 3. Jetson Orin Nano (Reasoning model inference)
```yaml
# docker-compose.jetson.yml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"          # Ollama API port
    volumes:
      - /data/models:/root/.ollama   # NFS mount from Dell for model storage
      - /var/run/docker.sock:/var/run/docker.sock  # optional for GPU passthrough
    environment:
      - OLLAMA_KEEP_ALIVE=24h
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped
    # If GPU passthrough needed (Jetson NVIDIA):
    # devices:
    #   - /dev/dri:/dev/dri
    #   - /dev/nvidia0:/dev/nvidia0
    # runtime: nvidia  # Requires NVIDIA Container Toolkit on Jetson host

  portainer-agent:
    image: portainer/agent:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    # ... same as above
```

### 4. Raspberry Pi 5 (logging + monitoring)
```yaml
# docker-compose.pi5.yml
services:
  loki:
    image: grafana/loki:latest
    container_name: loki
    ports:
      - "3100:3100"          # Loki API
    volumes:
      - ./loki/config:/etc/loki
      - ./loki/data:/loki
    command: -config.file=/etc/loki/loki-config.yaml
    restart: unless-stopped

  alloy:
    image: grafana/alloy:latest
    container_name: alloy
    volumes:
      - ./alloy/config:/etc/alloy
      - /var/log:/var/log
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/alloy/alloy.yaml
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"          # Grafana UI
    volumes:
      - ./grafana/data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    restart: unless-stopped

  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    ports:
      - "9000:9000"          # Portainer UI
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./portainer/data:/data
    restart: unless-stopped
```

## 🌐 NETWORK ARCHITECTURE

### Tailscale Configuration
- Each device joins the same Tailscale network using an auth key.
- MagicDNS enabled (`*.tailscale.ts.net` resolves to device IPs).
- Subnet routers optional; we use direct peer‑to‑peer.

### Firewall Rules (UFW / iptables)
On each node:
```bash
# Allow Tailscale interface
sudo ufw allow in on tailscale0
sudo ufw allow out on tailscale0

# Allow specific container ports (optional)
sudo ufw allow 8000/tcp   # embedding service
sudo ufw allow 8081/tcp   # Zvec
sudo ufw allow 11434/tcp   # Ollama
sudo ufw allow 3100/tcp   # Loki
sudo ufw allow 3000/tcp   # Grafana
sudo ufw allow 9000/tcp   # Portainer
```

### NFS Setup
**On Dell (server):**
- Export `/data/vectors` and `/data/models` to Tailscale IPs of Jetson and ThinkPad.
- `/etc/exports.d/lab.exports`:
```
/data/vectors 100.64.0.0/10(rw,sync,no_subtree_check,no_root_squash)
/data/models  100.64.0.0/10(rw,sync,no_subtree_check,no_root_squash)
```

**On clients (ThinkPad, Jetson):**
```bash
sudo mount -t nfs dell-embed.tailscale.ts.net:/data/vectors /mnt/vectors
sudo mount -t nfs dell-embed.tailscale.ts.net:/data/models /mnt/models
```

**Automount via `/etc/fstab`:**
```
dell-embed.tailscale.ts.net:/data/vectors /mnt/vectors nfs defaults,nofail,noatime 0 0
```

## 💾 STORAGE LAYOUT

| Path (on Dell)         | Purpose                          | Size Estimate | Backup Strategy |
|------------------------|----------------------------------|---------------|-----------------|
| `/data/models/bge`     | BAAI embedding model             | 1.3 GB        | Git LFS / S3    |
| `/data/models`          | Ollama model storage (models stored in `models/` subdirectory) | scalable      | Git LFS / S3    |
| `/data/vectors/zvec.db`| Zvec vector database             | scalable      | Periodic rsync to ThinkPad |
| `/data/logs`           | Local logs (optional)            | –             | Rotated weekly  |

**Note:** The Dell’s NVMe SSD provides high‑throughput storage for vector indexes and model files. Jetson mounts the model directory via NFS to avoid duplication.

## 📋 STEP‑BY‑STEP DEPLOYMENT CHECKLIST

### Phase 1: Tailscale & OpenClaw Pairing
- [ ] Install Tailscale on all four devices.
- [ ] Generate Tailscale auth key; join each device to the network.
- [ ] Verify connectivity: `ping thinkpad-lab.tailscale.ts.net`.
- [ ] Pair each device with OpenClaw (use `openclaw nodes pair`).
- [ ] Label nodes in OpenClaw: `thinkpad-lab`, `dell-embed`, `jetson-llm`, `pi5-monitor`.

### Phase 2: Docker Installation
- [ ] Install Docker Engine and Docker Compose on each node.
- [ ] Add user to `docker` group.
- [ ] Test `docker run hello-world`.

### Phase 3: NFS Server (Dell)
- [ ] Create `/data/{models,vectors,logs}` directories.
- [ ] Deploy `nfs-server` container.
- [ ] Configure exports and start NFS server.
- [ ] Test locally with `showmount -e localhost`.

### Phase 4: Embedding & Vector DB (Dell)
- [ ] Download BAAI/bge‑large‑en‑v1.5 model to `/data/models/bge`.
- [ ] Build/pull embedding‑service image.
- [ ] Deploy `docker-compose.dell.yml`.
- [ ] Verify embedding API: `curl http://localhost:8000/embed -d '{"text":"hello"}'`.
- [ ] Verify Zvec API: `curl http://localhost:8081/health`.

### Phase 5: LLM Inference (Jetson)
- [ ] Mount NFS shares (`/data/models`).
- [ ] Deploy `docker-compose.jetson.yml`.
- [ ] Pull LLM model: `docker exec ollama ollama pull llama2`.
- [ ] Test completion: `curl http://localhost:11434/api/generate -d '{"model":"llama2", "prompt":"Hello"}'`.

### Phase 6: Logging & Monitoring (Pi 5)
- [ ] Deploy Loki, Alloy, Grafana, Portainer via `docker-compose.pi5.yml`.
- [ ] Set Grafana admin password.
- [ ] Configure Alloy to scrape Docker logs and syslog.
- [ ] Add Loki data source in Grafana.
- [ ] Access Portainer at `http://pi5-monitor.tailscale.ts.net:9000`.

### Phase 7: Integration & Validation
- [ ] From ThinkPad, test embedding service via Tailscale IP.
- [ ] Insert sample vectors into Zvec.
- [ ] Perform RAG query: embed → search → LLM completion.
- [ ] Verify logs appear in Grafana.
- [ ] Confirm all containers visible in Portainer.

## 🧪 VALIDATION TESTS

### 1. Embedding API
```bash
curl -X POST http://dell-embed.tailscale.ts.net:8000/embed \
  -H "Content-Type: application/json" \
  -d '{"text":"The quick brown fox jumps over the lazy dog."}' | jq .
```
**Expected:** 1024‑dimensional float array.

### 2. Vector Insertion & Search
```bash
# Insert
curl -X POST http://dell-embed.tailscale.ts.net:8081/insert \
  -H "Content-Type: application/json" \
  -d '{"id":"doc1", "vector":[0.1,...,0.9], "metadata":{"title":"Test"}}'

# Search
curl -X POST http://dell-embed.tailscale.ts.net:8081/search \
  -H "Content-Type: application/json" \
  -d '{"vector":[0.1,...,0.9], "k":5}'
```

### 3. LLM Inference with RAG
```bash
# Pseudocode
embedding=$(curl -s .../embed -d '{"text":"query"}')
results=$(curl -s .../search -d "{\"vector\":$embedding, \"k\":3}")
context=$(echo $results | jq -r '.results[].metadata.text')
curl -X POST http://jetson-llm.tailscale.ts.net:11434/api/generate \
  -d "{\"model\":\"llama2\", \"prompt\":\"Answer based on: $context\n\nQuery: query\"}"
```

### 4. Log Ingestion
```bash
# Send a test log via Loki API
curl -X POST http://pi5-monitor.tailscale.ts.net:3100/loki/api/v1/push \
  -H "Content-Type: application/json" \
  -d '{"streams":[{"stream":{"service":"test"},"values":[["'$(date +%s)000000000'","Test log entry"]]}]}'
```
Check Grafana Explore → Loki.

### 5. Portainer Access
- Browse to `http://pi5-monitor.tailscale.ts.net:9000`
- Should see all four nodes (after agents connect).

## 📊 MONITORING & OBSERVABILITY

### Metrics to Track
| Metric                          | Source          | Purpose |
|---------------------------------|-----------------|---------|
| GPU utilization (%)             | NVIDIA‑SMI / Jetson stats | Inference load |
| Embedding request latency (ms)  | Embedding service logs | API performance |
| Vector search QPS               | Zvec metrics    | DB throughput |
| LLM tokens/second               | Ollama server    | Inference speed |
| Container memory/CPU            | Docker stats → Prometheus | Resource health |
| Tailscale peer latency          | `tailscale ping` | Network health |

### Grafana Dashboards
1. **Home‑Lab Overview**: Uptime, request rates, error counts across all services.
2. **GPU Utilization**: Jetson and Dell GPU metrics.
3. **Vector DB Performance**: Insert/search latency, index size.
4. **Log Volume & Errors**: Loki log streams, error patterns.
5. **Container Resources**: Per‑node CPU/memory/network (via Portainer or cAdvisor).

**Implementation:** Use Grafana’s provisioning to pre‑load dashboards (JSON files in `./grafana/provisioning/dashboards`).

## 🔧 INCORPORATED TEAM INSIGHTS

### From Universal Data Cloud
- **Entities & Events:** Each service (embedding, LLM, vector DB) emits structured logs as Events; devices are Entities.
- **Federated Querying:** The RAG pipeline queries the nearest capable node (embedding on Dell, LLM on Jetson).
- **Domain‑Awareness:** The “domain” here is AI inference; plugins could be “embedding plugin”, “LLM plugin”.

### From Data Platform Architecture
- **Separation of concerns:** Storage (Dell), compute (Jetson), control (ThinkPad), observability (Pi 5).
- **Scalability:** Adding another Jetson or Dell is trivial—just join Tailscale and deploy containers.

### From AI Workflow Design
- **End‑to‑end RAG:** Embedding → search → context enrichment → completion.
- **Testing:** Validation scripts ensure each component meets latency/accuracy thresholds.

### From Steve Jobs‑Level Ideation
- **Magical simplicity:** One command `./deploy‑lab.sh` sets up the entire cluster.
- **Progressive disclosure:** Basic monitoring (Portainer) for beginners; advanced metrics (Grafana) for experts.
- **Delightful UX:** Tailscale MagicDNS means no IP memorization; everything “just works.”

## 🚀 RECOMMENDED NEXT STEPS

1. **Immediate:**
   - Confirm Tailscale connectivity among all four devices.
   - Pair each node with OpenClaw (run `openclaw nodes pair` on each).
   - Create the directory structure on Dell’s NVMe.

2. **Short‑term (this week):**
   - Deploy NFS server and test mounts.
   - Deploy embedding service and vector DB.
   - Run validation tests 1‑2.

3. **Medium‑term (next week):**
   - Set up Jetson with Ollama and integrate with NFS.
   - Deploy Loki stack and Portainer on Pi 5.
   - Run end‑to‑end RAG test.

4. **Long‑term:**
   - Add Prometheus for custom metrics.
   - Build a simple UI for RAG queries (hosted on ThinkPad).
   - Implement automated backup of vector DB.

## 📝 APPENDIX

### OpenClaw Node Pairing Commands
```bash
# On each device after installing OpenClaw CLI
openclaw nodes pair --label thinkpad-lab --description "Control plane"
```

### Docker Compose Overrides for Development
Use `docker-compose.override.yml` to mount local source code for active development on ThinkPad.

### Troubleshooting
- **Tailscale not connecting:** Check firewall, ensure `tailscale up --auth-key=...`.
- **NFS mount fails:** Verify exports list, check `rpcinfo -p dell-embed`.
- **CUDA errors on Dell:** Ensure NVIDIA drivers and `nvidia-container-toolkit` installed.
- **Jetson out of memory:** Reduce `N_GPU_LAYERS` or use smaller quant.

### Security Notes
- Tailscale provides mutual TLS; still restrict NFS exports to Tailscale IP range.
- Use unique passwords for Grafana, Portainer.
- Consider `tailscale lock` for mandatory key expiry.

---

**Deliverable:** This plan, once reviewed, will be implemented by the team using OpenClaw remote execution and the existing team’s expertise in data platforms, AI workflows, and product vision.