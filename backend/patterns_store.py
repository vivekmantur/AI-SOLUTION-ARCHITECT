import os
import glob
import re
from typing import List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from utils.embedding import get_embeddings_ollama


class PatternStore:
    def __init__(self, patterns_dir: str = None):
        if patterns_dir is None:
            patterns_dir = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),  # backend/
                    "..",                        # project root
                    "patterns"                   # patterns/
                )
            )

        self.patterns_dir = patterns_dir
        self.pattern_texts: List[str] = []
        self.pattern_names: List[str] = []
        self.pattern_meta: List[dict] = []
        self.embeddings = None

        self._load_patterns()

    # --------------------------------------------------
    # Load patterns
    # --------------------------------------------------
    def _load_patterns(self):
        files = glob.glob(
            os.path.join(self.patterns_dir, "*.md"),
            recursive=False
        )

        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            meta = self._extract_meta(text)

            self.pattern_texts.append(text)
            self.pattern_names.append(os.path.basename(path))
            self.pattern_meta.append(meta)

        print(
            f"✅ Loaded {len(self.pattern_texts)} patterns from {self.patterns_dir}"
        )

    # --------------------------------------------------
    # META extraction
    # --------------------------------------------------
    def _extract_meta(self, text: str) -> dict:
        """
        Extracts META block fields safely.
        """
        meta = {
            "pattern_id": None,
            "category": "unified",
            "domain": None,
        }

        meta_block = re.search(
            r"## META(.*?)---",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        if not meta_block:
            return meta

        block = meta_block.group(1)

        for line in block.splitlines():
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()

        return meta

    # --------------------------------------------------
    # Embeddings (lazy)
    # --------------------------------------------------
    def _ensure_embeddings(self):
        if self.embeddings is None:
            print("📥 Generating embeddings from Ollama (first-time)...")
            self.embeddings = get_embeddings_ollama(self.pattern_texts)

    # --------------------------------------------------
    # Query patterns
    # --------------------------------------------------
    def query(
        self,
        requirement_text: str,
        top_k: int = 2
    ) -> List[Tuple[str, str, float, str]]:

        if not self.pattern_texts:
            print("⚠️ No patterns loaded — skipping pattern matching")
            return []

        self._ensure_embeddings()

        augmented_query = f"""
System requirements:
{requirement_text}

Infer:
- platform domain
- architecture style
- scalability and availability
- data and integration patterns
"""

        query_emb = get_embeddings_ollama([augmented_query])
        sims = cosine_similarity(query_emb, self.embeddings)[0]

        ranked = sorted(
            zip(self.pattern_names, self.pattern_texts, sims, self.pattern_meta),
            key=lambda x: x[2],
            reverse=True,
        )

        results = []
        for name, text, score, meta in ranked[:top_k]:
            category = meta.get("category", "unified")
            results.append((name, text, score, category))

        return results


# Singleton
pattern_store = PatternStore()
