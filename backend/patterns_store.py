import os
import glob
from typing import List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from utils.embedding import get_embeddings_ollama


class PatternStore:
    def __init__(self, patterns_dir: str = None):
        # Resolve absolute path to /patterns directory
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
        self.embeddings = None

        self._load_patterns()

    def _load_patterns(self):
        """Load ALL markdown patterns recursively."""
        files = glob.glob(
            os.path.join(self.patterns_dir, "**", "*.md"),
            recursive=True
        )

        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            # Keep relative path for clarity (category/domain)
            rel_name = os.path.relpath(path, self.patterns_dir)

            self.pattern_texts.append(text)
            self.pattern_names.append(rel_name)

        print(
            f"✅ Loaded {len(self.pattern_texts)} patterns from {self.patterns_dir}"
        )

    def _ensure_embeddings(self):
        """Generate embeddings ONLY when needed (lazy loading)."""
        if self.embeddings is None:
            print("📥 Generating embeddings from Ollama (first-time)...")
            self.embeddings = get_embeddings_ollama(self.pattern_texts)

    def query(
        self,
        requirement_text: str,
        top_k: int = 2
    ) -> List[Tuple[str, str, float]]:

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
            zip(self.pattern_names, self.pattern_texts, sims),
            key=lambda x: x[2],
            reverse=True,
        )

        results = []
        for name, text, score in ranked[:top_k]:
            category = name.split(os.sep)[0]  # core / domain / capability
            results.append((name, text, score, category))

        return results



# Singleton instance
pattern_store = PatternStore()
