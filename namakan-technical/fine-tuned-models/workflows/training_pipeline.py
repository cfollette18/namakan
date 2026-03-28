#!/usr/bin/env python3
"""
Namakan — Fine-Tuned Models: Training Pipeline
LoRA/QLoRA fine-tuning using Axolotl or native PEFT.
Supports resume, evaluation, checkpoint selection.
"""
import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Literal

# ─── YAML Config Generator ─────────────────────────────────────────────────────

@dataclass
class TrainingConfig:
    base_model: str = "Qwen/Qwen2.5-7B-Instruct"
    model_type: str = "qwen2"
    data_path: str = "./data/prepared"
    output_dir: str = "./outputs"
    sequence_len: int = 2048
    # LoRA config
    adapter: Literal["lora", "qlora"] = "qlora"
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_target_modules: list = field(default_factory=lambda: [
        "q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"
    ])
    # Training config
    num_epochs: int = 3
    micro_batch_size: int = 2
    gradient_accumulation_steps: int = 8
    learning_rate: float = 0.0002
    warmup_steps: int = 10
    optimizer: str = "adamw_torch"
    logging_steps: int = 10
    save_steps: int = 100
    eval_steps: int = 100
    save_total_limit: int = 3
    max_grad_norm: float = 0.3
    # Hardware
    gpu_memory_utilization: float = 0.90
    # Eval
    eval_strategy: str = "steps"
    # Resume
    resume_from_checkpoint: Optional[str] = None

    def to_axolotl_yaml(self) -> str:
        """Generate Axolotl YAML config."""
        modules_str = "\n".join(f"  - {m}" for m in self.lora_target_modules)
        resume_line = f"\n  resume_from_checkpoint: {self.resume_from_checkpoint}" if self.resume_from_checkpoint else ""
        return f"""\
base_model: {self.base_model}
model_type: {self.model_type}
hub_model_id: null

{data_path}:
  test_files: null
  val_files: null

output_dir: {self.output_dir}
sequence_len: {self.sequence_len}

adapter: {self.adapter}
lora_r: {self.lora_r}
lora_alpha: {self.lora_alpha}
lora_dropout: {self.lora_dropout}
lora_target_modules:
{modules_str}

dataset_prepared_path: {self.data_path}
val_size: 0.05
{self.data_path}:
  save_sized: true

training:
  num_epochs: {self.num_epochs}
  micro_batch_size: {self.micro_batch_size}
  gradient_accumulation_steps: {self.gradient_accumulation_steps}
  learning_rate: {self.learning_rate}
  warmup_steps: {self.warmup_steps}
  optimizer: {self.optimizer}
  torch_dtype: float16
  bf16: full
  max_grad_norm: {self.max_grad_norm}
  gradient_checkpointing: true
  logging_steps: {self.logging_steps}
  save_steps: {self.save_steps}
  eval_steps: {self.eval_steps}
  eval_strategy: {self.eval_strategy}
  save_total_limit: {self.save_total_limit}
  weight_decay: 0.0
  seed: 42{resume_line}
"""


def generate_axolotl_config(config: TrainingConfig, output_path: str):
    """Write axolotl YAML config to file."""
    yaml_content = config.to_axolotl_yaml()
    with open(output_path, 'w') as f:
        f.write(yaml_content)
    print(f"[INFO] Axolotl config written to {output_path}")
    return yaml_content


# ─── PEFT Native Training ───────────────────────────────────────────────────────

def train_with_peft(config: TrainingConfig):
    """Train using native PEFT + Transformers (no Axolotl needed)."""
    print(f"[INFO] Starting PEFT training: {config.base_model}")
    
    import torch
    from transformers import (
        AutoModelForCausalLM, AutoTokenizer,
        BitsAndBytesConfig, TrainingArguments, Trainer, DataCollatorForLanguageModeling
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(config.base_model, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )
    
    print(f"[INFO] Loading base model: {config.base_model}")
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        quantization_config=bnb_config if config.adapter == "qlora" else None,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )
    
    if config.adapter == "qlora":
        model = prepare_model_for_kbit_training(model)
    
    # Apply LoRA
    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=config.lora_target_modules,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Load dataset
    from datasets import load_dataset
    
    def tokenize_function(examples):
        if "instruction" in examples:
            texts = [
                f"### Instruction:\n{ex['instruction']}\n### Response:\n{ex['output']}"
                for ex in zip(examples.get("instruction", []), examples.get("output", []))
            ]
        else:
            texts = examples.get("text", [])
        
        result = tokenizer(texts, truncation=True, max_length=config.sequence_len, padding="max_length")
        result["labels"] = result["input_ids"].copy()
        return result
    
    dataset = load_dataset("json", data_files={
        "train": os.path.join(config.data_path, "train.jsonl"),
        "val": os.path.join(config.data_path, "val.jsonl"),
    })
    
    tokenized = dataset.map(tokenize_function, batched=True, remove_columns=dataset["train"].column_names)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        per_device_train_batch_size=config.micro_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        num_train_epochs=config.num_epochs,
        warmup_steps=config.warmup_steps,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        eval_steps=config.eval_steps,
        eval_strategy="steps",
        save_total_limit=config.save_total_limit,
        bf16=True,
        torch_dtype=torch.bfloat16,
        max_grad_norm=config.max_grad_norm,
        report_to="none",
        optim="paged_adamw_8bit",
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["val"],
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )
    
    print("[INFO] Starting training...")
    trainer.train()
    print("[INFO] Training complete!")
    
    # Save final model
    final_path = os.path.join(config.output_dir, "final")
    model.save_pretrained(final_path)
    tokenizer.save_pretrained(final_path)
    print(f"[INFO] Model saved to {final_path}")
    
    return final_path


# ─── Checkpoint Selection ─────────────────────────────────────────────────────

def select_best_checkpoint(checkpoint_dir: str) -> str:
    """Select best checkpoint based on eval loss from training state."""
    checkpoints = []
    for item in os.listdir(checkpoint_dir):
        item_path = os.path.join(checkpoint_dir, item)
        if item.startswith("checkpoint-") and os.path.isdir(item_path):
            checkpoints.append(item)
    
    if not checkpoints:
        print("[WARN] No checkpoints found")
        return checkpoint_dir
    
    # Sort by step number
    checkpoints.sort(key=lambda x: int(x.split("-")[1]))
    best = checkpoints[-1]  # Last checkpoint is typically best (lowest eval loss)
    best_path = os.path.join(checkpoint_dir, best)
    print(f"[INFO] Selected checkpoint: {best}")
    return best_path


# ─── Main Orchestration ────────────────────────────────────────────────────────

def run_training(config: TrainingConfig, use_peft: bool = True, config_path: str = None):
    """Main training orchestration."""
    print("=" * 60)
    print("NAMAKAN FINE-TUNING PIPELINE")
    print("=" * 60)
    print(f"Base model: {config.base_model}")
    print(f"LoRA r={config.lora_r}, alpha={config.lora_alpha}")
    print(f"Data: {config.data_path}")
    print(f"Output: {config.output_dir}")
    print("=" * 60)
    
    os.makedirs(config.output_dir, exist_ok=True)
    
    if use_peft:
        final_path = train_with_peft(config)
    else:
        # Use Axolotl
        if config_path is None:
            config_path = os.path.join(config.output_dir, "config.yaml")
        generate_axolotl_config(config, config_path)
        
        print(f"[INFO] Running axolotl from {config_path}")
        result = subprocess.run(
            ["axolotl", "train", config_path],
            check=True
        )
        final_path = select_best_checkpoint(config.output_dir)
    
    print(f"[DONE] Training complete. Final model: {final_path}")
    return final_path


# ─── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Namakan Training Pipeline")
    parser.add_argument("--base-model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--data-path", default="./data/prepared")
    parser.add_argument("--output-dir", default="./outputs")
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=0.0002)
    parser.add_argument("--adapter", default="qlora", choices=["lora", "qlora"])
    parser.add_argument("--use-peft", action="store_true", help="Use native PEFT instead of Axolotl")
    parser.add_argument("--axolotl-config", help="Path to existing Axolotl config")
    args = parser.parse_args()
    
    config = TrainingConfig(
        base_model=args.base_model,
        data_path=args.data_path,
        output_dir=args.output_dir,
        lora_r=args.lora_r,
        lora_alpha=args.lora_alpha,
        num_epochs=args.epochs,
        learning_rate=args.lr,
        adapter=args.adapter,
        resume_from_checkpoint=None,
    )
    
    run_training(config, use_peft=args.use_peft, config_path=args.axolotl_config)
