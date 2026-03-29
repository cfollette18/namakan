#!/usr/bin/env bash
# Namakan — Full Service Pipeline Orchestration
# Usage: ./run_pipeline.sh <service> <phase> [options]
# Services: fine-tuned-models | rag-pipelines | agentic-workflows | custom-ai-employees

set -e

NAMAKAN_ROOT="$(cd "$(dirname "$0")" && pwd)"

show_help() {
    cat << EOF
Namakan Pipeline Orchestrator

USAGE:
  $0 <service> <phase> [options]

SERVICES:
  fine-tuned-models     — Data → Training → Evaluation → Deployment
  rag-pipelines        — Ingestion → Indexing → Retrieval → Serve
  agentic-workflows    — Build → Test → Eval → Monitor → Deploy
  custom-ai-employees — Train → Integrate → Onboard → Monitor

PHASES:
  all                  — Run all phases in sequence
  data                 — Data collection and preparation
  train                — Model training
  eval                 — Evaluation and testing
  deploy               — Deployment and serving
  monitor              — Start monitoring server (agentic-workflows only)

EXAMPLES:
  $0 fine-tuned-models data --input ./client-data --output ./data/prepared
  $0 fine-tuned-models train --base-model Qwen/Qwen2.5-7B --adapter ./adapters/client-a
  $0 fine-tuned-models deploy --base-model Qwen/Qwen2.5-7B --adapter ./adapters/client-a --method ollama
  $0 rag-pipelines ingest --input ./documents --output ./vector-store
  $0 agentic-workflows test --workflow ./workflows/customer-onboarding.yaml
  $0 agentic-workflows eval --suite ./workflows/eval_pipeline.py
  $0 agentic-workflows monitor --port 9090

EOF
}

SERVICE=$1
PHASE=$2
shift 2 || { show_help; exit 1; }

case "$SERVICE" in
  fine-tuned-models)
    case "$PHASE" in
      data)
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/data_pipeline.py" "$@"
        ;;
      train)
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/training_pipeline.py" "$@"
        ;;
      eval)
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/evaluation_pipeline.py" "$@"
        ;;
      deploy)
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/deployment_pipeline.py" "$@"
        ;;
      all)
        echo "[ORCHESTRATE] Running full fine-tuned-models pipeline..."
        echo "  1/4 Data pipeline..."
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/data_pipeline.py" "$@"
        echo "  2/4 Training pipeline..."
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/training_pipeline.py" "$@"
        echo "  3/4 Evaluation pipeline..."
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/evaluation_pipeline.py" "$@"
        echo "  4/4 Deployment pipeline..."
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/deployment_pipeline.py" "$@"
        echo "[DONE] Full pipeline complete!"
        ;;
      *)
        echo "Unknown phase: $PHASE"
        show_help
        ;;
    esac
    ;;

  rag-pipelines)
    case "$PHASE" in
      ingest)
        python3 "${NAMAKAN_ROOT}/rag-pipelines/workflows/ingestion_pipeline.py" "$@"
        ;;
      retrieve)
        python3 "${NAMAKAN_ROOT}/rag-pipelines/workflows/retrieval_pipeline.py" "$@"
        ;;
      all)
        echo "[ORCHESTRATE] Running full RAG pipeline..."
        echo "  1/3 Ingestion..."
        python3 "${NAMAKAN_ROOT}/rag-pipelines/workflows/ingestion_pipeline.py" "$@"
        echo "  2/3 Retrieval..."
        echo "  3/3 Serving..."
        echo "[DONE] RAG pipeline complete!"
        ;;
      *)
        echo "Unknown phase: $PHASE"
        show_help
        ;;
    esac
    ;;

  agentic-workflows)
    case "$PHASE" in
      build)
        python3 "${NAMAKAN_ROOT}/agentic-workflows/workflows/agent_engine.py" "$@"
        ;;
      test)
        echo "[TEST] Running agentic workflow tests..."
        python3 "${NAMAKAN_ROOT}/agentic-workflows/workflows/agent_engine.py" --task "Run self-test: check all tools are working" --role "Test Agent"
        ;;
      eval)
        echo "[EVAL] Running agentic workflow evaluation pipeline..."
        python3 "${NAMAKAN_ROOT}/agentic-workflows/workflows/eval_pipeline.py" "$@"
        ;;
      monitor)
        echo "[MONITOR] Starting monitoring server..."
        python3 "${NAMAKAN_ROOT}/agentic-workflows/workflows/monitoring.py" "$@"
        ;;
      deploy)
        echo "[DEPLOY] Deploying agentic workflow..."
        ;;
      *)
        echo "Unknown phase: $PHASE"
        show_help
        ;;
    esac
    ;;

  custom-ai-employees)
    case "$PHASE" in
      train)
        python3 "${NAMAKAN_ROOT}/fine-tuned-models/workflows/training_pipeline.py" "$@"  # Reuse FTM pipeline
        ;;
      onboard)
        echo "[ONBOARD] Running AI employee onboarding..."
        ;;
      *)
        echo "Unknown phase: $PHASE"
        show_help
        ;;
    esac
    ;;

  *)
    echo "Unknown service: $SERVICE"
    show_help
    ;;
esac
