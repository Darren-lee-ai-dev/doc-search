import unittest
from search import search

class SearchTests(unittest.TestCase):
    def test_relevant_source_ranks_first(self):
        docs=[{'name':'a','text':'Protect API keys using environment variables.'},{'name':'b','text':'Bananas and apples are fruit.'}]
        self.assertEqual(search(docs,'API keys')[0]['source'],'a')
    def test_no_match(self):
        self.assertEqual(search([{'name':'a','text':'apples'}],'zebra'),[])
    def test_empty(self):
        self.assertEqual(search([], 'hello'),[])
        self.assertEqual(search([{'name':'a','text':''}], 'hello'),[])
    def test_case_and_punctuation(self):
        self.assertEqual(len(search([{'name':'a','text':'API keys!'}],'api')),1)
    def test_later_chunk(self):
        result=search([{'name':'long','text':' '.join(['apple']*160+['zebra']*20)}],'zebra')
        self.assertGreater(result[0]['word'],1)
    def test_limit(self):
        self.assertEqual(len(search([{'name':str(i),'text':'apple'} for i in range(10)],'apple')),5)

if __name__=='__main__': unittest.main()
