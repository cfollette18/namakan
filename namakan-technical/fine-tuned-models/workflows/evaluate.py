#!/usr/bin/env python3
"""
Evaluation Harness — Fine-Tuned Models Pipeline
Runs a benchmark test suite against a deployed model to verify quality.
Usage: python3 evaluate.py --adapter ./adapters/acme/final --test-data ./data/val.jsonl
"""
import argparse
import json
import math
import os
import sys
import time
import re

classcolors = {
    "PASS": "\033[92m",
    "FAIL": "\033[91m",
    "WARN": "\033[93m",
    "INFO": "\033[94m",
    "RESET": "\033[0m"
}

def color(tag, text):
    return f"{classcolors.get(tag, '')}{text}{classcolors['RESET']}"

def load_test_data(path):
    """Load JSONL test data."""
    examples = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                examples.append(json.loads(line))
    return examples

def normalize(text):
    """Basic text normalization for comparison."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def exact_match(pred, ref):
    """Exact string match."""
    return normalize(pred) == normalize(ref)

def contains_match(pred, ref):
    """Check if prediction contains the reference answer."""
    return normalize(ref) in normalize(pred)

def keyword_coverage(pred, ref):
    """What fraction of reference keywords appear in prediction."""
    ref_words = set(normalize(ref).split())
    pred_words = set(normalize(pred).split())
    if not ref_words:
        return 1.0
    overlap = ref_words & pred_words
    return len(overlap) / len(ref_words)

def rouge_l_sim(pred, ref):
    """Simplified ROUGE-L (LCS-based)."""
    pred_ngrams = normalize(pred).split()
    ref_ngrams = normalize(ref).split()
    if not pred_ngrams or not ref_ngrams:
        return 0.0
    
    m, n = len(pred_ngrams), len(ref_ngrams)
    # LCS DP
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pred_ngrams[i-1] == ref_ngrams[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    lcs = dp[m][n]
    precision = lcs / m if m else 0
    recall = lcs / n if n else 0
    if precision + recall == 0:
        return 0.0
    f1 = 2 * precision * recall / (precision + recall)
    return f1

def perplexity_score(loss):
    """Convert loss to perplexity."""
    return math.exp(loss) if loss and loss < 100 else float('inf')

def run_inference(prompt, model_path, method="ollama", base_url="http://localhost:11434"):
    """
    Run inference against the model.
    Supports: ollama, openai, huggingface
    """
    if method == "ollama":
        import urllib.request
        payload = {
            "model": "namakan-finetuned",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 256}
        }
        req = urllib.request.Request(
            f"{base_url}/api/generate",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result.get("response", "").strip()
    
    elif method == "openai":
        # Use OpenAI-compatible endpoint
        import urllib.request
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "local-model",
            "temperature": 0.1,
            "max_tokens": 256
        }
        req = urllib.request.Request(
            f"{base_url}/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY','')}"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"].strip()
    
    else:
        raise ValueError(f"Unknown method: {method}")

def evaluate_test_suite(test_data, model_path, method="ollama", verbose=True):
    """Run the full evaluation suite."""
    results = {
        "total": len(test_data),
        "exact_match": 0,
        "contains_match": 0,
        "keyword_coverage_total": 0.0,
        "rouge_l_total": 0.0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "latencies": [],
        "details": []
    }
    
    for i, example in enumerate(test_data):
        instruction = example.get("instruction", example.get("input", ""))
        expected = example.get("output", example.get("reference", ""))
        example_id = example.get("id", f"test-{i}")
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"  Test {i+1}/{len(test_data)}: {example_id}")
            print(f"  Input: {instruction[:80]}{'...' if len(instruction) > 80 else ''}")
        
        start = time.time()
        try:
            prediction = run_inference(instruction, model_path, method)
            latency = time.time() - start
            results["latencies"].append(latency)
        except Exception as e:
            if verbose:
                print(f"  {color('FAIL', 'ERROR')} inference failed: {e}")
            results["errors"] += 1
            results["details"].append({"id": example_id, "status": "error", "error": str(e)})
            continue
        
        # Metrics
        em = exact_match(prediction, expected)
        cm = contains_match(prediction, expected)
        kc = keyword_coverage(prediction, expected)
        rl = rouge_l_sim(prediction, expected)
        
        results["exact_match"] += int(em)
        results["contains_match"] += int(cm)
        results["keyword_coverage_total"] += kc
        results["rouge_l_total"] += rl
        
        passed = cm and kc >= 0.5
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        detail = {
            "id": example_id,
            "status": "passed" if passed else "failed",
            "latency": round(latency, 2),
            "exact_match": em,
            "contains_match": cm,
            "keyword_coverage": round(kc, 3),
            "rouge_l": round(rl, 3),
            "input": instruction[:200],
            "expected": expected[:200],
            "prediction": prediction[:200]
        }
        results["details"].append(detail)
        
        if verbose:
            status = color("PASS", "✓ PASS") if passed else color("FAIL", "✗ FAIL")
            print(f"  {status} | EM: {em} | CM: {cm} | KC: {kc:.2f} | ROUGE-L: {rl:.2f} | Latency: {latency:.1f}s")
            if not cm:
                print(f"  {color('WARN', '  Expected:')} {expected[:100]}")
                print(f"  {color('INFO', '  Got:')} {prediction[:100]}")
    
    # Compute aggregates
    n = results["total"] - results["errors"]
    results["exact_match_rate"] = results["exact_match"] / n if n else 0
    results["contains_match_rate"] = results["contains_match"] / n if n else 0
    results["avg_keyword_coverage"] = results["keyword_coverage_total"] / n if n else 0
    results["avg_rouge_l"] = results["rouge_l_total"] / n if n else 0
    results["avg_latency"] = sum(results["latencies"]) / len(results["latencies"]) if results["latencies"] else 0
    results["p95_latency"] = sorted(results["latencies"])[int(len(results["latencies"]) * 0.95)] if results["latencies"] else 0
    results["pass_rate"] = results["passed"] / n if n else 0
    
    return results

def print_report(results, output_path=None):
    """Print evaluation report."""
    n = results["total"] - results["errors"]
    pass_threshold = 0.8
    
    print(f"\n{'='*60}")
    print(f"  EVALUATION REPORT")
    print(f"{'='*60}")
    print(f"\n  Total tests:   {results['total']}")
    print(f"  Passed:       {results['passed']} ({results['pass_rate']:.1%})")
    print(f"  Failed:       {results['failed']}")
    print(f"  Errors:       {results['errors']}")
    print(f"\n  {color('INFO', 'Metrics:')}")
    print(f"    Exact Match Rate:     {results['exact_match_rate']:.1%}")
    print(f"    Contains Match Rate: {results['contains_match_rate']:.1%}")
    print(f"    Avg Keyword Cover:    {results['avg_keyword_coverage']:.1%}")
    print(f"    Avg ROUGE-L:         {results['avg_rouge_l']:.2f}")
    print(f"\n  {color('INFO', 'Performance:')}")
    print(f"    Avg Latency:         {results['avg_latency']:.1f}s")
    print(f"    P95 Latency:         {results['p95_latency']:.1f}s")
    
    overall_pass = results["pass_rate"] >= pass_threshold and results["avg_keyword_coverage"] >= 0.6
    
    print(f"\n  {color('INFO', 'Verdict:')} ", end="")
    if overall_pass:
        print(color("PASS", f"✓ Model meets quality threshold ({pass_threshold:.0%} pass rate)"))
    else:
        print(color("FAIL", f"✗ Model does NOT meet threshold"))
        print(f"\n  {color('WARN', 'Recommendations:')}")
        if results["pass_rate"] < pass_threshold:
            print(f"    - Pass rate ({results['pass_rate']:.1%}) below threshold ({pass_threshold:.0%})")
            print(f"    - Consider more training epochs or better training data")
        if results["avg_keyword_coverage"] < 0.6:
            print(f"    - Keyword coverage ({results['avg_keyword_coverage']:.1%}) too low")
            print(f"    - Model may be missing key domain vocabulary")
    
    print(f"\n{'='*60}")
    
    if output_path:
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n  Full report saved to: {output_path}")
    
    return overall_pass

def main():
    parser = argparse.ArgumentParser(description="Namakan Fine-Tuned Model Evaluation")
    parser.add_argument("--adapter", default="./adapters/final", help="Path to trained adapter")
    parser.add_argument("--test-data", default="./data/val.jsonl", help="Test data (JSONL)")
    parser.add_argument("--method", default="ollama", choices=["ollama", "openai", "huggingface"], help="Inference method")
    parser.add_argument("--base-url", default="http://localhost:11434", help="API base URL")
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--quiet", action="store_true", help="Only print summary")
    args = parser.parse_args()
    
    if not os.path.exists(args.test_data):
        print(f"ERROR: Test data not found: {args.test_data}")
        print("Create a test set with: python3 workflows/evaluation_pipeline.py --mode split")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"  NAMAKAN — Model Evaluation Harness")
    print(f"{'='*60}")
    print(f"  Adapter:   {args.adapter}")
    print(f"  Test data: {args.test_data}")
    print(f"  Method:    {args.method}")
    
    test_data = load_test_data(args.test_data)
    print(f"  Loaded {len(test_data)} test examples\n")
    
    results = evaluate_test_suite(test_data, args.adapter, args.method, verbose=not args.quiet)
    passed = print_report(results, args.output)
    
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
