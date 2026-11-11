import re
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer


class KnowledgeIndex:
    def __init__(self, knowledge_dir: Path, dimensions: int = 384) -> None:
        self.vectorizer = HashingVectorizer(
            n_features=dimensions,
            alternate_sign=False,
            norm="l2",
            ngram_range=(1, 2),
            stop_words="english",
        )
        self.sections = self._load(knowledge_dir)
        self.matrix = self.vectorizer.transform([item["text"] for item in self.sections])

    @staticmethod
    def _load(knowledge_dir: Path) -> list[dict[str, str]]:
        sections: list[dict[str, str]] = []
        for path in sorted(knowledge_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            body = text.split("---", 2)[-1].strip()
            title_match = re.search(r"(?m)^#\s+(.+)$", body)
            title = title_match.group(1) if title_match else path.stem
            for section in re.split(r"(?m)^##\s+", body):
                heading, _, content = section.strip().partition("\n")
                if content.strip():
                    sections.append(
                        {
                            "source": f"data/knowledge/{path.name}",
                            "title": title,
                            "section": heading.strip("# "),
                            "text": content.strip(),
                        }
                    )
        return sections

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_vector = self.vectorizer.transform([query])
        scores = np.asarray((self.matrix @ query_vector.T).toarray()).ravel()
        indexes = scores.argsort()[::-1][:top_k]
        return [{**self.sections[index], "relevance": float(scores[index])} for index in indexes]
