#!/usr/bin/env python3
"""
Namakan — Fine-Tuned Models: Deployment Pipeline
Converts LoRA adapters to GGUF, creates Ollama model, or deploys via vLLM/FastAPI.
"""
import os
import json
import argparse
import subprocess
import shutil
from pathlib import Path

def merge_and_export(
    base_model: str,
    adapter_path: str,
    output_path: str,
    method: str = "ollama"  # ollama | vllm | huggingface
):
    """Merge LoRA adapter with base model and export."""
    print(f"[DEPLOY] Merging adapter with base model...")
    print(f"  Base: {base_model}")
    print(f"  Adapter: {adapter_path}")
    print(f"  Output: {output_path}")
    print(f"  Method: {method}")
    
    os.makedirs(output_path, exist_ok=True)
    
    if method == "huggingface":
        _deploy_huggingface(base_model, adapter_path, output_path)
    elif method == "ollama":
        _deploy_ollama(base_model, adapter_path, output_path)
    elif method == "vllm":
        _deploy_vllm(base_model, adapter_path, output_path)
    elif method == "llama_cpp":
        _export_gguf(base_model, adapter_path, output_path)
    
    print(f"[DEPLOY] Done!")

def _deploy_huggingface(base_model: str, adapter_path: str, output_path: str):
    """Export merged model in HuggingFace format."""
    print("[DEPLOY] Exporting as HuggingFace format...")
    
    code = f"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

print("Loading base model...")
base = AutoModelForCausalLM.from_pretrained(
    "{base_model}",
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True,
)
print("Merging adapter...")
model = PeftModel.from_pretrained(base, "{adapter_path}")
model = model.merge_and_unload()
print("Saving merged model...")
model.save_pretrained("{output_path}")
tokenizer = AutoTokenizer.from_pretrained("{base_model}", trust_remote_code=True)
tokenizer.save_pretrained("{output_path}")
print("Done!")
"""
    
    with open("/tmp/merge_model.py", "w") as f:
        f.write(code)
    
    result = subprocess.run(["python3", "/tmp/merge_model.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Merge failed: {result.stderr}")
        raise RuntimeError(result.stderr)
    print("[DEPLOY] Merged model saved.")

def _export_gguf(base_model: str, adapter_path: str, output_path: str):
    """Export to GGUF format for llama.cpp."""
    print("[DEPLOY] Exporting as GGUF (llama.cpp format)...")
    # Requires llama.cpp conversion tools
    print("[WARN] GGUF export needs llama.cpp build: git clone https://github.com/ggerganov/llama.cpp")

def _deploy_ollama(base_model: str, adapter_path: str, output_path: str):
    """Create Ollama model with adapter."""
    # First merge, then create Ollama model
    merged_path = os.path.join(output_path, "merged")
    os.makedirs(merged_path, exist_ok=True)
    
    _deploy_huggingface(base_model, adapter_path, merged_path)
    
    # Create Modelfile
    modelfile = (
        "FROM ./\n"
        '"""{{{{ if .System }}}<|im_start|>system\n'
        "{{{{ .System }}}<|im_end|>{{ end }}{{{ range .Messages }}}<|im_start|>{{{{ .Role }}}\n"
        "{{{{ .Content }}}<|im_end|>{{ end }}<|im_start|>assistant\n"
        '"""\n'
        "PARAMETER temperature 0.3\n"
        "PARAMETER top_p 0.9\n"
        "PARAMETER repeat_penalty 1.1\n"
        "PARAMETER num_ctx 2048"
    )
    
    with open(os.path.join(output_path, "Modelfile"), "w") as f:
        f.write(modelfile)
    
    # Build Ollama model
    model_name = os.path.basename(output_path)
    print(f"[DEPLOY] Building Ollama model '{model_name}'...")
    result = subprocess.run(
        ["ollama", "create", model_name, "-f", os.path.join(output_path, "Modelfile")],
        capture_output=True, text=True, cwd=output_path
    )
    if result.returncode == 0:
        print(f"[DEPLOY] Ollama model created: ollama run {model_name}")
    else:
        print(f"[WARN] Ollama create failed (may need llama.cpp rebuild): {result.stderr}")

def _deploy_vllm(base_model: str, adapter_path: str, output_path: str):
    """Deploy via vLLM with LoRA support."""
    print("[DEPLOY] vLLM deployment with LoRA...")
    print("[DEPLOY] Run this to serve:")
    print(f"  python -m vllm.entrypoints.openai.api_server \\")
    print(f"    --model {base_model} \\")
    print(f"    --lora-module {adapter_path} \\")
    print(f"    --port 8000")


# ─── FastAPI Server ───────────────────────────────────────────────────────────

def create_api_server(model_path: str, port: int = 8000):
    """Generate FastAPI server for the model."""
    server_code = f'''\
#!/usr/bin/env python3
"""Namakan Fine-Tuned Model API Server."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

app = FastAPI(title="Namakan Fine-Tuned Model API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading model from {model_path}...")
tokenizer = AutoTokenizer.from_pretrained("{model_path}", trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(
    "{model_path}",
    torch_dtype=torch.float16,
    device_map="auto",
)
model = base_model  # Already merged
print("Model ready!")

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.3
    top_p: float = 0.9
    repetition_penalty: float = 1.1

class GenerateResponse(BaseModel):
    output: str
    tokens_generated: int
    latency_ms: float

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    import time
    start = time.time()
    
    inputs = tokenizer(req.prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
            repetition_penalty=req.repetition_penalty,
            do_sample=True,
        )
    
    response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    latency = (time.time() - start) * 1000
    
    return GenerateResponse(
        output=response,
        tokens_generated=len(outputs[0]) - len(inputs["input_ids"][0]),
        latency_ms=round(latency, 2)
    )

@app.get("/health")
async def health():
    return {{"status": "healthy", "model": "{model_path}"}}

@app.get("/")
async def root():
    return {{"service": "Namakan Fine-Tuned Model API", "model": "{model_path}"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port={port})
'''
    
    api_path = os.path.join(model_path, "api_server.py")
    with open(api_path, "w") as f:
        f.write(server_code)
    print(f"[DEPLOY] API server written to {api_path}")
    print(f"[DEPLOY] Run: python3 {api_path}")
    return api_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Namakan Deployment Pipeline")
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--adapter", required=True, help="Path to LoRA adapter")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--method", default="huggingface", choices=["huggingface", "ollama", "vllm", "llama_cpp"])
    parser.add_argument("--serve", action="store_true", help="Also create FastAPI server")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    
    merge_and_export(args.base_model, args.adapter, args.output, args.method)
    
    if args.serve:
        create_api_server(args.output, args.port)
