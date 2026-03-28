#!/usr/bin/env python3
"""
Generate a client-specific Namakan LoRA training Colab notebook.
Usage: python3 generate_colab.py --client "Acme Corp" --model "Qwen/Qwen2.5-7B-Instruct" --data "acme_train.jsonl"
"""
import json, argparse, os, re

TEMPLATE = os.path.join(os.path.dirname(__file__), "namakan-lora-training-template.ipynb")

def slug(text):
    return re.sub(r'[^a-zA-Z0-9]', '-', text.lower()).strip('-')

def generate(client_name, base_model, train_data, val_data=None, gcs_bucket=None, lora_r=16):
    with open(TEMPLATE) as f:
        nb = json.load(f)

    replacements = {
        "[CLIENT NAME]": client_name,
        "[BASE MODEL]": base_model,
        "[TRAIN_DATA_FILE]": train_data,
        "[VAL_DATA_FILE]": val_data or train_data.replace("train", "val"),
        "[GCS_BUCKET_NAME]": gcs_bucket or "",
        "[CLIENT_NAME]": slug(client_name),
    }

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            for i, line in enumerate(cell["source"]):
                for old, new in replacements.items():
                    if old in line:
                        line = line.replace(old, new)
                cell["source"][i] = line
        elif cell["cell_type"] == "markdown":
            for i, line in enumerate(cell["source"]):
                for old, new in replacements.items():
                    if old in line:
                        line = line.replace(old, new)
                cell["source"][i] = line

    out_name = f"namakan-{slug(client_name)}-lora-training.ipynb"
    out_path = os.path.join(os.path.dirname(TEMPLATE), out_name)
    with open(out_path, "w") as f:
        json.dump(nb, f, indent=1)

    print(f"✅ Generated: {out_path}")
    print(f"   Client: {client_name}")
    print(f"   Model: {base_model}")
    print(f"   Data: {train_data}")
    print(f"   LoRA R: {lora_r}")
    return out_path

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--client", required=True)
    p.add_argument("--model", required=True, help="HuggingFace model name")
    p.add_argument("--train", required=True, help="Training data file (JSONL in GCS)")
    p.add_argument("--val", help="Validation data file (default: train → val)")
    p.add_argument("--bucket", help="GCS bucket name")
    p.add_argument("--r", type=int, default=16, help="LoRA rank (default: 16)")
    args = p.parse_args()

    generate(args.client, args.model, args.train, args.val, args.bucket, args.r)
