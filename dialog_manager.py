from extractor import Extractor
from query_maker import QueryMaker
from ranker import Ranker

from owlready2 import get_ontology, sync_reasoner


class DialogManager:
    def __init__(self):
        # initialize system
        self.run_system: bool = True
        self.system_output: str = "Hello, how can I help you?"

        # intialize ontology
        self.ontology = get_ontology("draftOntology.rdf").load()
        with self.ontology:
            sync_reasoner(infer_property_values=True)

        # initialize modules
        self.extractor = Extractor(self.ontology)
        self.query_maker = QueryMaker()
        self.ranker = Ranker()

        # initialize data
        self.facts: list = []
        self.queries: list = []
        self.results_ontology: dict = {}
        self.results_chat_gpt: dict = {}

    def run(self):
        while self.run_system:
            print("system: ", self.system_output)
            user_input = input("user: ")

            if not user_input:
                self.system_output = (
                    "I didn't catch that. Could you please say something?"
                )
                continue

            self.extract_facts(user_input)
            self.make_queries()
            self.query_ontology()
            self.query_chat_gpt()
            self.compare_results()
            self.rank_results()
            self.make_output()

    def extract_facts(self, scenario: str):
        self.facts = self.extractor.extract_facts(scenario)

    def make_queries(self):
        self.queries = self.query_maker.make_queries(self.facts)

    def query_ontology(self):
        return NotImplemented

    def query_chat_gpt(self):
        return NotImplemented

    def compare_results(self):
        return NotImplemented

    def rank_results(self):
        return NotImplemented

    def make_output(self):
        return NotImplemented
