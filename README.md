# Doc Search

A local document retrieval tool with a browser interface, source attribution, and no third-party Python dependencies. Built with AI assistance as a portfolio project.

## Features
- Load up to 10 UTF-8 text or Markdown files, or try the built-in sample notes.
- Rank overlapping passages with TF-IDF cosine similarity.
- Show original excerpts, filenames, and starting word positions.
- Process text in memory without saving uploads or calling external APIs.
- Handle empty queries, unmatched terms, and oversized requests.

## Run
Requires Python 3.10 or newer. From this directory:

```sh
python app.py
```

On Windows you can use `py app.py`; on macOS/Linux, `python3 app.py`.
Open http://127.0.0.1:8000 and click **Load sample notes**, then **Search documents**.
Stop the server with Ctrl+C.

## Test
```sh
python -m unittest discover -s tests -v
```

## How it works
Browser files → local JSON request → overlapping 100-word windows → smoothed TF-IDF → cosine ranking → top five source excerpts.

The query uses unique case-folded terms. Documents use logarithmic term frequency. Windows overlap by 20 words. Only positive-score matches appear. Ties retain document/window order.

## Limits
This is lexical retrieval, not an LLM or semantic search. It does not answer questions, understand synonyms, or parse PDF/Word files. Scores are similarity values, not confidence. English-like word segmentation works best. The standard-library server is for local development only; do not expose it publicly. No persistent index, authentication, or multi-user support is provided.

## Files
- `search.py`: ranking engine
- `app.py`: local HTTP server and validation
- `index.html`: browser interface
- `tests/`: retrieval tests
- `.github/workflows/tests.yml`: automated tests on pushes and pull requests

## Possible next improvements
- Add document filtering and exact-phrase search.
- Measure retrieval quality against a small labeled question set.
- Add PDF extraction with clear handling of scanned files.
- Compare this baseline with an embedding-based retriever.

These are future ideas, not implemented features.
