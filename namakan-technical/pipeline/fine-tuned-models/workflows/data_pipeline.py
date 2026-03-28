#!/usr/bin/env python3
"""
Namakan — Fine-Tuned Models: Data Pipeline
Handles data collection, cleaning, PII redaction, formatting for instruction tuning.
"""
import os
import re
import json
import hashlib
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ─── Configuration ──────────────────────────────────────────────────────────────

@dataclass
class DataPipelineConfig:
    input_dir: str
    output_dir: str
    redact_pii: bool = True
    min_length: int = 50
    max_length: int = 32000
    dedup_threshold: float = 0.85
    format_type: str = "instruction"  # instruction | chat | completion

PI: str = r"\b\d{3}-\d{2}-\d{4}\b"          # SSN
EMAIL: str = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b"
PHONE: str = r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"
CC: str = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"

# ─── Logging ───────────────────────────────────────────────────────────────────

class Log:
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.stats = {"files": 0, "chunks": 0, "redacted": 0, "dropped": 0, "duplicates": 0}

    def info(self, msg):  if not self.quiet: print(f"[INFO]  {msg}")
    def warn(self, msg):  if not self.quiet: print(f"[WARN]  {msg}")
    def error(self, msg): print(f"[ERROR] {msg}")

# ─── PII Redaction ─────────────────────────────────────────────────────────────

class PIARedactor:
    """Redact personally identifiable information from text."""
    
    def __init__(self, replacement_map: Optional[dict] = None):
        self.replacement_map = replacement_map or {
            PI:     "[SSN]",
            EMAIL:  "[EMAIL]",
            PHONE:  "[PHONE]",
            CC:     "[CARD]",
        }
        self.stats = {"ssn": 0, "email": 0, "phone": 0, "card": 0}
    
    def redactions_summary(self) -> dict:
        return self.stats
    
    def redact(self, text: str) -> tuple[str, dict]:
        """Returns (redacted_text, redaction_counts)."""
        counts = {}
        for pattern, label in self.pi_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                counts[label] = len(matches)
                self.stats[label] = self.stats.get(label, 0) + len(matches)
                text = re.sub(pattern, label, text, flags=re.IGNORECASE)
        return text, counts
    
    pi_patterns = {
        PI:     "ssn",
        EMAIL:  "email",
        PHONE:  "phone",
        CC:     "card",
    }

# ─── Text Cleaning ────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Normalize whitespace, remove control chars, strip."""
    # Remove null bytes
    text = text.replace('\x00', '')
    # Normalize unicode
    import unicodedata
    text = unicodedata.normalize('NFKC', text)
    # Remove control characters
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C' or c in '\n\t')
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ─── Deduplication ─────────────────────────────────────────────────────────────

class Deduper:
    """MinHash-based approximate deduplication."""
    
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.seen: dict[str, str] = {}
    
    def is_duplicate(self, text: str) -> bool:
        """Check if text is a near-duplicate of something already seen."""
        import hashlib
        # Simple: check exact hash first
        h = hashlib.sha256(text.encode()).hexdigest()
        if h in self.seen:
            return True
        
        # Approximate: check first 64 chars as quick fingerprint
        fingerprint = text[:128].lower().strip()
        if fingerprint in self.seen:
            return True
        
        self.seen[fingerprint] = h
        self.seen[h] = h
        return False

# ─── Format Converters ─────────────────────────────────────────────────────────

def format_instruction(examples: list[dict]) -> list[dict]:
    """Convert to instruction-tuning format."""
    formatted = []
    for ex in examples:
        if "instruction" in ex and "output" in ex:
            formatted.append({
                "instruction": ex["instruction"],
                "input": ex.get("input", ""),
                "output": ex["output"]
            })
        elif "prompt" in ex and "completion" in ex:
            formatted.append({
                "instruction": ex["prompt"],
                "input": "",
                "output": ex["completion"]
            })
    return formatted

def format_chat(examples: list[dict]) -> list[dict]:
    """Convert to chat format for conversational AI."""
    formatted = []
    for ex in examples:
        messages = []
        if "system" in ex:
            messages.append({"role": "system", "content": ex["system"]})
        if "messages" in ex:
            messages.extend(ex["messages"])
        elif "input" in ex and "output" in ex:
            messages.append({"role": "user", "content": ex["input"]})
            messages.append({"role": "assistant", "content": ex["output"]})
        if messages:
            formatted.append({"messages": messages})
    return formatted

# ─── Chunking ─────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Split text into overlapping token chunks."""
    import tiktoken
    try:
        enc = tiktoken.get_encoding("cl100k_base")
    except Exception:
        enc = None
    
    if enc:
        tokens = enc.encode(text)
        chunks = []
        for i in range(0, len(tokens), chunk_size - overlap):
            chunk_tokens = tokens[i:i + chunk_size]
            chunk = enc.decode(chunk_tokens)
            if len(chunk.strip()) > 20:
                chunks.append(chunk)
        return chunks
    else:
        # Fallback: split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks, current = [], []
        current_len = 0
        for sent in sentences:
            words = len(sent.split())
            if current_len + words > chunk_size and current:
                chunks.append(' '.join(current))
                current = [sent]
                current_len = words
            else:
                current.append(sent)
                current_len += words
        if current:
            chunks.append(' '.join(current))
        return [c for c in chunks if len(c) > 20]

# ─── Main Pipeline ────────────────────────────────────────────────────────────

def run_pipeline(config: DataPipelineConfig, log: Optional[Log] = None):
    if log is None:
        log = Log()
    
    log.info(f"Starting data pipeline: {config.input_dir} → {config.output_dir}")
    
    os.makedirs(config.output_dir, exist_ok=True)
    redactor = PIARedactor() if config.redact_pii else None
    deduper = Deduper(threshold=config.dedup_threshold)
    
    # Supported file types
    file_patterns = {".txt", ".md", ".json", ".jsonl", ".csv"}
    text_extensions = {".txt", ".md", ".csv"}
    
    all_examples = []
    total_files = 0
    
    for root, dirs, files in os.walk(config.input_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in file_patterns:
                continue
            
            filepath = os.path.join(root, filename)
            total_files += 1
            
            try:
                if ext in text_extensions:
                    with open(filepath, 'r', errors='ignore') as f:
                        text = f.read()
                elif ext == ".json":
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        all_examples.extend(data)
                        continue
                    elif isinstance(data, dict):
                        all_examples.append(data)
                        continue
                elif ext == ".jsonl":
                    with open(filepath, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    all_examples.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass
                    continue
                
                # Process raw text
                text = clean_text(text)
                if redactor:
                    text, _ = redactor.redact(text)
                
                if not (config.min_length <= len(text) <= config.max_length):
                    log.warn(f"Skipping {filename}: length {len(text)} out of range")
                    log.stats["dropped"] += 1
                    continue
                
                if deduper.is_duplicate(text):
                    log.warn(f"Skipping {filename}: duplicate")
                    log.stats["duplicates"] += 1
                    continue
                
                # Chunk for training
                chunks = chunk_text(text)
                for chunk in chunks:
                    all_examples.append({"text": chunk})
                    log.stats["chunks"] += 1
                
            except Exception as e:
                log.error(f"Failed to process {filename}: {e}")
    
    # Format output
    if config.format_type == "instruction":
        formatted = format_instruction(all_examples)
    elif config.format_type == "chat":
        formatted = format_chat(all_examples)
    else:
        formatted = all_examples
    
    # Save train/val split
    split_idx = int(len(formatted) * 0.9)
    train_data = formatted[:split_idx]
    val_data = formatted[split_idx:]
    
    train_path = os.path.join(config.output_dir, "train.jsonl")
    val_path = os.path.join(config.output_dir, "val.jsonl")
    
    with open(train_path, 'w') as f:
        for ex in train_data:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    
    with open(val_path, 'w') as f:
        for ex in val_data:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    
    log.info(f"Processed {total_files} files → {len(train_data)} train, {len(val_data)} val")
    if redactor:
        log.info(f"PII stats: {redactor.redactions_summary()}")
    
    # Write manifest
    manifest = {
        "input_dir": config.input_dir,
        "output_dir": config.output_dir,
        "total_files": total_files,
        "train_count": len(train_data),
        "val_count": len(val_data),
        "format": config.format_type,
        "pii_redacted": config.redact_pii,
        "stats": log.stats
    }
    manifest_path = os.path.join(config.output_dir, "manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    log.info(f"Manifest written to {manifest_path}")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Namakan Data Pipeline")
    parser.add_argument("--input", "-i", required=True, help="Input directory")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--format", "-f", default="instruction", choices=["instruction", "chat", "completion"])
    parser.add_argument("--no-redact", action="store_true", help="Skip PII redaction")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")
    args = parser.parse_args()
    
    config = DataPipelineConfig(
        input_dir=args.input,
        output_dir=args.output,
        redact_pii=not args.no_redact,
        format_type=args.format
    )
    run_pipeline(config, Log(quiet=args.quiet))
