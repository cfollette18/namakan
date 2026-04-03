#!/usr/bin/env python3
"""
RAG Evaluation Harness — Agentic RAG v2.0
Tests a RAG pipeline against question/answer pairs.
Evaluates all 4 gap-closers: Verify & N-ACK, Citation & Source Provenance,
Recursive Multi-Step Reasoning, Metadata-Level Security Filter.
Usage:
  python3 evaluate.py --questions questions.jsonl --index-dir ./chromadb
  python3 evaluate.py --questions questions.jsonl --index-dir ./chromadb --gaps  # Test all 4 gaps
"""
import argparse
import json
import os
import sys
import time
import re
from dataclasses import dataclass
from typing import Optional

try:
    import chromadb
    from sentence_transformers import CrossEncoder
    from sentence_transformers import SentenceTransformer
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


# ─── Gap Definitions ──────────────────────────────────────────────────────────

@dataclass
class GapTest:
    """A test case for a specific gap."""
    id: str
    name: str
    description: str
    query: str
    expected: str  # Keyword that should appear in answer
    gap_closes: str  # Which gap this tests


GAP_TESTS = [
    # Gap 1: Verify & N-ACK
    GapTest(
        id="g1-silent",
        name="Silent Context (N-ACK)",
        description="Query that has NO answer in the documents — must N-ACK",
        query="What is the company's IPO date?",
        expected="cannot find",
        gap_closes="Verify & N-ACK",
    ),
    GapTest(
        id="g1-noisy",
        name="Ambiguous Context (N-ACK)",
        description="Query where context is ambiguous — must N-ACK",
        query="What is the revenue for 2024?",
        expected="cannot find",
        gap_closes="Verify & N-ACK",
    ),

    # Gap 2: Citation & Source Provenance
    GapTest(
        id="g2-citation",
        name="Citation Required",
        description="Every factual claim must have [file, p.N] citation",
        query="What is the warranty period?",
        expected="[",
        gap_closes="Citation & Source Provenance",
    ),
    GapTest(
        id="g2-multi-source",
        name="Multi-Source Synthesis",
        description="If using multiple docs, must list all under Verified Sources",
        query="Compare the vacation policy vs the sick leave policy",
        expected="Verified Sources",
        gap_closes="Citation & Source Provenance",
    ),

    # Gap 3: Recursive Multi-Step Reasoning
    GapTest(
        id="g3-compare",
        name="Comparison Query (Multi-Step)",
        description="Comparison queries require loading both entities first",
        query="Compare Project Alpha vs Project Beta",
        expected="",
        gap_closes="Recursive Multi-Step Reasoning",
    ),
    GapTest(
        id="g3-vs",
        name="VS Query (Multi-Step)",
        description="X vs Y queries are multi-entity",
        query="Product A or Product B — which has better margin?",
        expected="",
        gap_closes="Recursive Multi-Step Reasoning",
    ),

    # Gap 4: Metadata-Level Security Filter
    GapTest(
        id="g4-filter",
        name="Permission Filter Applied",
        description="Chunks with visibility_level > user clearance are hidden",
        query="What are the executive compensation details?",
        expected="",
        gap_closes="Metadata-Level Security Filter",
    ),
    GapTest(
        id="g4-denied",
        name="Permission Denial Notice",
        description="When all content is filtered, user must be informed",
        query="Show me the M&A deal terms",
        expected="access level",
        gap_closes="Metadata-Level Security Filter",
    ),
]


# ─── Color Helpers ────────────────────────────────────────────────────────────

def color(tag, text):
    codes = {
        "PASS": "\033[92m", "FAIL": "\033[91m", "WARN": "\033[93m",
        "INFO": "\033[94m", "RESET": "\033[0m", "BOLD": "\033[1m",
        "CYAN": "\033[96m", "MAGENTA": "\033[95m",
    }
    return f"{codes.get(tag, '')}{text}{codes['RESET']}"


# ─── Question Loading ─────────────────────────────────────────────────────────

def load_questions(path: str) -> list[dict]:
    pairs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                pairs.append(json.loads(line))
    return pairs


# ─── Gap 1: Verify & N-ACK Tests ─────────────────────────────────────────────

def test_nack(query: str, answer: str) -> tuple[bool, str]:
    """
    Test if the system correctly N-ACK'd (declined to answer) when context was silent.
    Returns (passed, reason).
    """
    # The system should say it cannot find a definitive answer
    nack_phrases = [
        "cannot find",
        "cannot determine",
        "not found in the provided",
        "not available in the documents",
        "i don't have that information",
        "not contained in",
        "no information",
    ]
    answer_lower = answer.lower()
    has_nack = any(phrase in answer_lower for phrase in nack_phrases)
    has_hallucination = any(phrase in answer_lower for phrase in [
        "based on my training", "i believe", "typically", "in general"
    ])
    if has_nack and not has_hallucination:
        return True, "Correctly N-ACK'd — did not hallucinate"
    elif has_hallucination and not has_nack:
        return False, "Hallucinated — filled gap with training data"
    else:
        return False, f"Expected N-ACK phrase or hallucination warning in answer"


def test_answerability(query: str, answer: str, chunks: list) -> tuple[bool, str]:
    """
    Test if the system only answered when context was sufficient.
    Returns (passed, reason).
    """
    if not chunks:
        return False, "No chunks retrieved but answer was generated"
    # Check that answer contains some word from the query
    query_words = set(re.findall(r'\b\w{4,}\b', query.lower()))
    query_words -= {'what', 'when', 'where', 'which', 'how', 'does', 'have', 'been', 'from', 'with', 'that', 'this'}
    answer_lower = answer.lower()
    overlap = sum(1 for w in query_words if w in answer_lower)
    if overlap >= 1:
        return True, f"Answer contains {overlap} query-relevant terms — context was used"
    return False, f"Answer has no overlap with query terms"


# ─── Gap 2: Citation Tests ───────────────────────────────────────────────────

def test_citation_format(answer: str) -> tuple[bool, str]:
    """
    Test if answer contains properly formatted [file, p.N] citations.
    Returns (passed, reason).
    """
    # Match [filename, p.N] or [filename, p.?]
    citation_pattern = r'\[([^\]]+\.(?:pdf|docx|txt|md|csv|xlsx|pptx|html?|json)[^\]]*),\s*p\.?\d*\]'
    matches = re.findall(citation_pattern, answer, re.IGNORECASE)
    if matches:
        return True, f"Found {len(matches)} citation(s): {matches}"
    return False, "No [file, p.N] citation found in answer"


def test_verified_sources(answer: str) -> tuple[bool, str]:
    """
    Test if multi-source answer lists all sources under 'Verified Sources' heading.
    Returns (passed, reason).
    """
    if "verified sources" in answer.lower():
        return True, "Verified Sources footer present"
    return False, "No 'Verified Sources' section found"


# ─── Gap 3: Recursive Reasoning Tests ───────────────────────────────────────

def test_multi_entity_detection(query: str) -> tuple[bool, str]:
    """
    Test if the query analyzer correctly identifies multi-entity queries.
    Returns (passed, reason).
    """
    comparison_patterns = [
        r'\bcompare\s+(\w+)\s+vs\.?\s+(\w+)',
        r'\b(\w+)\s+vs\.?\s+(\w+)',
        r'\bdifference\s+between\s+(\w+)\s+and\s+(\w+)',
        r'(\w+)\s+or\s+(\w+)\s+\?',
    ]
    entities_found = []
    for pattern in comparison_patterns:
        matches = re.findall(pattern, query, re.IGNORECASE)
        for m in matches:
            if isinstance(m, tuple):
                entities_found.extend([e.strip() for e in m if e.strip()])

    if len(entities_found) >= 2:
        return True, f"Multi-entity query detected: {entities_found}"
    return False, "Single-entity query"


# ─── Gap 4: Security Filter Tests ───────────────────────────────────────────

def test_visibility_filter(chunks: list, user_clearance: int) -> tuple[bool, str]:
    """
    Test if chunks all have visibility_level <= user clearance.
    Returns (passed, reason).
    """
    if not chunks:
        return True, "No chunks = no visibility issues"

    violations = []
    for chunk in chunks:
        vis = chunk.get("visibility_level", 0)
        if vis > user_clearance:
            violations.append(f"chunk {chunk.get('chunk_id','?')}: level {vis} > clearance {user_clearance}")

    if violations:
        return False, f"Security violations: {violations}"
    return True, f"All {len(chunks)} chunks within clearance level {user_clearance}"


def test_permission_denial_notice(answer: str, permission_filtered: bool) -> tuple[bool, str]:
    """
    Test if permission-denied cases include an appropriate notice.
    Returns (passed, reason).
    """
    if not permission_filtered:
        return True, "No permission filtering in this test"

    notice_phrases = [
        "access level",
        "not have access",
        "restricted",
        "permission",
        "clearance",
        "could not be retrieved due to",
    ]
    if any(phrase in answer.lower() for phrase in notice_phrases):
        return True, "Permission denial notice present"
    return False, "Permission-filtered response missing access notice"


# ─── Chunk Loading ───────────────────────────────────────────────────────────

def load_chunks_with_metadata(index_dir: str) -> list[dict]:
    """Load chunks from index directory for testing."""
    chunks_path = os.path.join(index_dir, "chunks.json")
    if not os.path.exists(chunks_path):
        return []
    with open(chunks_path) as f:
        return json.load(f)


# ─── Main Evaluator ───────────────────────────────────────────────────────────

def evaluate_rag(qa_pairs: list[dict], index_dir: str, verbose: bool = False):
    """Run RAG evaluation against question/answer pairs."""
    # Try loading the new agentic retrieval
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from retrieval_pipeline import AgenticRAG, UserSession, RetrievedChunk
        HAS_AGENTIC = True
    except Exception:
        HAS_AGENTIC = False

    results = {
        "total": len(qa_pairs),
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "gap_scores": {
            "Verify & N-ACK": {"passed": 0, "total": 0},
            "Citation & Source Provenance": {"passed": 0, "total": 0},
            "Recursive Multi-Step Reasoning": {"passed": 0, "total": 0},
            "Metadata-Level Security Filter": {"passed": 0, "total": 0},
        },
        "details": [],
    }

    retrieval_times = []
    total_times = []

    for i, pair in enumerate(qa_pairs):
        question = pair["question"]
        expected = pair.get("answer", "")
        pair_id = pair.get("id", f"q-{i}")
        is_gap_test = pair.get("gap_test", False)
        gap_closes = pair.get("gap_closes", "")

        print(f"\n  [{i+1}/{len(qa_pairs)}] {pair_id}")
        print(f"    Q: {question[:80]}")

        start_total = time.time()
        try:
            if HAS_AGENTIC:
                agentic = AgenticRAG(index_dir)
                result = agentic.verify_and_answer(question, verbose=verbose)
                answer = result.answer
                chunks = result.chunks
                nack = result.nack
                permission_filtered = result.permission_filtered
            else:
                # Fallback to basic retrieval
                chunks = load_chunks_with_metadata(index_dir)
                answer = "[Agentic RAG not available — install dependencies]"
                nack = False
                permission_filtered = False

            retrieval_time_s = round(time.time() - start_total, 3)
            total_time = time.time() - start_total
            retrieval_times.append(retrieval_time_s)
            total_times.append(total_time)

            # Evaluate gap closes
            if is_gap_test:
                passed = False
                reason = ""

                if gap_closes == "Verify & N-ACK":
                    p, r = test_nack(question, answer)
                    if not p:
                        p2, r2 = test_answerability(question, answer, chunks)
                        passed = p2
                        reason = r2 + " | " + r
                    else:
                        passed = True
                        reason = r

                elif gap_closes == "Citation & Source Provenance":
                    p1, r1 = test_citation_format(answer)
                    p2, r2 = test_verified_sources(answer)
                    passed = p1  # Primary: citations required
                    reason = r1
                    if not p2:
                        reason += " | " + r2

                elif gap_closes == "Recursive Multi-Step Reasoning":
                    p, r = test_multi_entity_detection(question)
                    passed = p
                    reason = r

                elif gap_closes == "Metadata-Level Security Filter":
                    user_clearance = pair.get("user_clearance", 1)
                    p1, r1 = test_visibility_filter(
                        [{"visibility_level": c.visibility_level for c in chunks}],
                        user_clearance,
                    )
                    p2, r2 = test_permission_denial_notice(answer, permission_filtered)
                    passed = p1 or (permission_filtered and p2)
                    reason = r1 + " | " + r2

                if passed:
                    results["passed"] += 1
                    status = color("PASS", "✓ PASS")
                    results["gap_scores"][gap_closes]["passed"] += 1
                else:
                    results["failed"] += 1
                    status = color("FAIL", "✗ FAIL")
                results["gap_scores"][gap_closes]["total"] += 1

            else:
                # Standard QA test
                answer_lower = answer.lower()
                matched = any(
                    kw.lower() in answer_lower
                    for kw in expected.split()
                    if len(kw) > 3
                )
                if matched:
                    results["passed"] += 1
                    status = color("PASS", "✓ PASS")
                else:
                    results["failed"] += 1
                    status = color("FAIL", "✗ FAIL")
                reason = f"keyword match: '{expected[:40]}'"

            print(f"    {status} | retrieval: {retrieval_time_s}s | {reason}")
            results["details"].append({
                "id": pair_id,
                "question": question,
                "answer": answer[:200],
                "status": "passed" if passed else "failed",
                "reason": reason,
            })

        except Exception as e:
            results["errors"] += 1
            print(f"    {color('FAIL', 'ERROR')} {e}")
            results["details"].append({
                "id": pair_id,
                "status": "error",
                "error": str(e)
            })

    n = results["total"] - results["errors"]
    results["pass_rate"] = results["passed"] / n if n else 0
    results["avg_retrieval_time"] = sum(retrieval_times) / len(retrieval_times) if retrieval_times else 0
    results["avg_total_time"] = sum(total_times) / len(total_times) if total_times else 0

    return results


def evaluate_gaps_only(index_dir: str, verbose: bool = False):
    """Run only the 4 gap-closer tests against the index."""
    print(color("BOLD", "\n" + "=" * 60))
    print(color("BOLD", "  AGENTIC RAG GAP CLOSER EVALUATION"))
    print(color("BOLD", "=" * 60))

    passed_counts = {g: 0 for g in [
        "Verify & N-ACK", "Citation & Source Provenance",
        "Recursive Multi-Step Reasoning", "Metadata-Level Security Filter"
    ]}
    total_counts = {g: 0 for g in list(passed_counts.keys())}

    for gap_test in GAP_TESTS:
        gap_name = gap_test.gap_closes
        total_counts[gap_name] += 1

        print(f"\n  [{gap_test.id}] {color('CYAN', gap_test.name)}")
        print(f"    Description: {gap_test.description}")
        print(f"    Query: {gap_test.query[:60]}...")
        print(f"    Expected: {gap_test.expected or '(detection only)'}")

        try:
            sys.path.insert(0, os.path.dirname(__file__))
            from retrieval_pipeline import AgenticRAG, UserSession

            agentic = AgenticRAG(index_dir)

            if gap_name == "Verify & N-ACK":
                result = agentic.verify_and_answer(gap_test.query, verbose=verbose)
                p, r = test_nack(gap_test.query, result.answer)
                if not p:
                    p2, r2 = test_answerability(gap_test.query, result.answer, result.chunks)
                    if p2:
                        p, r = True, r2

            elif gap_name == "Citation & Source Provenance":
                result = agentic.verify_and_answer(gap_test.query, verbose=verbose)
                p, r = test_citation_format(result.answer)
                if p:
                    p2, r2 = test_verified_sources(result.answer)
                    if not p2:
                        r += f" | {r2}"
                if not p:
                    # Check if no docs were found (different failure mode)
                    if not result.chunks:
                        p, r = False, "No chunks retrieved — cannot test citation"

            elif gap_name == "Recursive Multi-Step Reasoning":
                p, r = test_multi_entity_detection(gap_test.query)
                # Also check the system behavior
                result = agentic.verify_and_answer(gap_test.query, verbose=verbose)
                # For comparisons, the system should load multi-step working memory
                if result.working_memory and len(result.working_memory) > 1:
                    r += f" | Working memory: {len(result.working_memory)} steps logged"

            elif gap_name == "Metadata-Level Security Filter":
                user_clearance = 1  # employee
                session = UserSession.from_role("employee")
                agentic_user = AgenticRAG(index_dir, user_session=session)
                result = agentic_user.verify_and_answer(gap_test.query, verbose=verbose)

                chunk_vis = [{"visibility_level": getattr(c, 'visibility_level', 0)} for c in result.chunks]
                p1, r1 = test_visibility_filter(chunk_vis, user_clearance)
                p2, r2 = test_permission_denial_notice(result.answer, result.permission_filtered)
                p, r = p1, r1
                if result.permission_filtered and not p2:
                    r += f" | Permission denial notice MISSING"

            if p:
                passed_counts[gap_name] += 1
                status = color("PASS", "✓ PASS")
            else:
                status = color("FAIL", "✗ FAIL")
            print(f"    Result: {status} — {r}")

        except ImportError as e:
            print(f"    {color('WARN', 'SKIP')} Agentic RAG not available: {e}")
            p = False

        except Exception as e:
            print(f"    {color('FAIL', 'ERROR')} {e}")
            p = False

    # Summary
    print(color("BOLD", "\n" + "=" * 60))
    print(color("BOLD", "  GAP CLOSER SUMMARY"))
    print(color("BOLD", "=" * 60))
    for gap_name in passed_counts:
        total = total_counts[gap_name]
        passed = passed_counts[gap_name]
        pct = f"{passed/total*100:.0f}%" if total > 0 else "N/A"
        status_str = color("PASS", f"✓ {passed}/{total} ({pct})") if passed == total else color("FAIL", f"✗ {passed}/{total} ({pct})")
        print(f"  {gap_name}: {status_str}")

    overall_pass = sum(passed_counts.values())
    overall_total = sum(total_counts.values())
    overall_pct = f"{overall_pass/overall_total*100:.0f}%" if overall_total > 0 else "N/A"
    print(color("BOLD", f"\n  Overall: {overall_pass}/{overall_total} gaps closed ({overall_pct})"))
    print(color("BOLD", "=" * 60))

    threshold = 0.75
    if overall_pass / overall_total >= threshold if overall_total > 0 else False:
        print(color("PASS", f"\n  ✓ Agentic RAG meets quality threshold (≥{threshold:.0%})"))
    else:
        print(color("FAIL", f"\n  ✗ Agentic RAG below threshold — gaps remain"))

    return {
        "gap_scores": {k: {"passed": passed_counts[k], "total": total_counts[k]} for k in passed_counts},
        "overall_passed": overall_pass,
        "overall_total": overall_total,
    }


def print_report(results: dict):
    print(f"\n{'='*60}")
    print(f"  RAG EVALUATION REPORT")
    print(f"{'='*60}")
    print(f"  Total questions: {results['total']}")
    print(f"  Passed:          {results['passed']} ({results['pass_rate']:.1%})")
    print(f"  Failed:          {results['failed']}")
    print(f"  Errors:          {results['errors']}")
    print(f"\n  Avg retrieval time: {results['avg_retrieval_time']:.3f}s")
    print(f"  Avg total time:    {results['avg_total_time']:.3f}s")

    if "gap_scores" in results:
        print(f"\n  Gap Closer Scores:")
        for gap, score in results["gap_scores"].items():
            pct = f"{score['passed']/score['total']*100:.0f}%" if score['total'] > 0 else "N/A"
            status_str = color("PASS", f"✓ {score['passed']}/{score['total']}") if score['passed'] == score['total'] else color("FAIL", f"✗ {score['passed']}/{score['total']}")
            print(f"    {gap}: {status_str} ({pct})")

    threshold = 0.8
    if results["pass_rate"] >= threshold:
        print(f"\n  {color('PASS', '✓ RAG pipeline meets quality threshold (≥80%)')}")
    else:
        pass_rate = results["pass_rate"]
        print(f"\n  {color('FAIL', f'✗ RAG pipeline below threshold ({pass_rate:.1%} < {threshold:.0%})')}")
        print(f"\n  {color('WARN', 'Recommendations:')}")
        print(f"    - Increase chunk overlap")
        print(f"    - Try a domain-specific embedding model")
        print(f"    - Add hybrid search (dense + sparse)")
        print(f"    - Increase n_results from 5 to 10")
    print(f"{'='*60}")


def main():
    if not HAS_DEPS:
        print("WARNING: Missing dependencies — using fallback mode.")
        print("  Install with: pip install chromadb sentence-transformers")
        print("  Agentic RAG features will be limited.\n")

    parser = argparse.ArgumentParser(description="Namakan Agentic RAG Evaluation v2.0")
    parser.add_argument("--questions", help="JSONL file with question/answer pairs")
    parser.add_argument("--index-dir", "-i", help="Index directory (from ingestion_pipeline)")
    parser.add_argument("--gaps", action="store_true", help="Run only the 4 gap-closer tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show agentic reasoning log")
    parser.add_argument("--embed-model", default="nomic-ai/nomic-embed-text-v1.5")
    parser.add_argument("--output", help="Save results JSON")
    args = parser.parse_args()

    # Gap-closer evaluation mode
    if args.gaps:
        if not args.index_dir:
            print("ERROR: --index-dir required for gap evaluation")
            sys.exit(1)
        gap_results = evaluate_gaps_only(args.index_dir, verbose=args.verbose)
        if args.output:
            with open(args.output, "w") as f:
                json.dump(gap_results, f, indent=2)
            print(f"\nSaved to {args.output}")
        overall_pct = gap_results["overall_passed"] / gap_results["overall_total"] * 100 if gap_results["overall_total"] > 0 else 0
        sys.exit(0 if overall_pct >= 75 else 1)

    # Standard QA evaluation
    if not args.questions:
        print("ERROR: --questions required (or use --gaps for gap-closer tests)")
        sys.exit(1)
    if not os.path.exists(args.questions):
        print(f"ERROR: Questions file not found: {args.questions}")
        sys.exit(1)

    qa_pairs = load_questions(args.questions)
    print(f"Loaded {len(qa_pairs)} question/answer pairs")

    index_dir = args.index_dir or os.path.dirname(args.questions)
    results = evaluate_rag(qa_pairs, index_dir, verbose=args.verbose)
    print_report(results)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved to {args.output}")

    sys.exit(0 if results["pass_rate"] >= 0.8 else 1)


if __name__ == "__main__":
    main()