"""Deterministic paragraph retrieval with source attribution; no external services."""
import math
import re
from collections import Counter


def tokens(text):
    return re.findall(r"\w+", text.casefold())


def search(documents, query, limit=5):
    """Rank overlapping 100-word windows using smoothed TF-IDF cosine similarity."""
    terms = set(tokens(query))
    if not terms:
        return []
    chunks = []
    for document in documents:
        words = document['text'].split()
        for start in range(0, len(words), 80):
            excerpt = ' '.join(words[start:start + 100])
            chunks.append((document['name'], start + 1, excerpt, Counter(tokens(excerpt))))
    if not chunks:
        return []
    vocabulary = set().union(*(set(c[3]) for c in chunks))
    idf = {t: math.log((1 + len(chunks)) / (1 + sum(t in c[3] for c in chunks))) + 1 for t in vocabulary}
    qvec = {t: idf[t] for t in terms if t in idf}
    qnorm = math.sqrt(sum(v*v for v in qvec.values()))
    if not qnorm:
        return []
    results = []
    for name, start, excerpt, counts in chunks:
        vector = {t: (1 + math.log(n)) * idf[t] for t, n in counts.items()}
        norm = math.sqrt(sum(v*v for v in vector.values()))
        score = sum(vector.get(t, 0)*v for t, v in qvec.items()) / (norm*qnorm)
        if score > 0:
            results.append(dict(source=name, word=start, excerpt=excerpt, score=round(score, 4)))
    return sorted(results, key=lambda r: -r['score'])[:limit]
