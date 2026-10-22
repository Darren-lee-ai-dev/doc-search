import unittest
from search import search


class SearchTests(unittest.TestCase):
    def test_relevant_document(self):
        docs = [
            {"name": "security", "text": "Protect API keys."},
            {"name": "food", "text": "Apples and bananas."},
        ]
        results = search(docs, "API keys")
        self.assertEqual(results[0]["source"], "security")

    def test_no_match(self):
        docs = [{"name": "notes", "text": "Apples"}]
        self.assertEqual(search(docs, "zebra"), [])

    def test_empty_documents(self):
        self.assertEqual(search([], "hello"), [])

    def test_case_insensitive(self):
        docs = [{"name": "notes", "text": "API keys"}]
        self.assertEqual(len(search(docs, "api")), 1)


if __name__ == "__main__":
    unittest.main()
