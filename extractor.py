import re


class Extractor:
    def __init__(self, ontology):
        self.keywords = self.extract_keywords(ontology)

    def extract_facts(self, scenario: str) -> list:
        """Extract the keywords for each sentence from the scenario. This will be used
        as a preparation for creating queries."""
        extracted_sentence_facts = []
        sentences = scenario.split(". ")

        for sentence in sentences:
            # Remove the plural form of the keyword
            # Example: so that we correclty pick pancake instead of pancakes
            singular_sentence = re.sub(r"\b(\w+)s\b", r"\1", sentence)

            sentence_facts = {
                "sentence": sentence,
                "keywords": [],
            }

            # Pattern to match keywords
            pattern = r"\b(?:{})\b".format("|".join(map(re.escape, self.keywords)))

            keywords = re.findall(
                pattern,
                singular_sentence,
                re.IGNORECASE,
            )

            if keywords:
                sentence_facts["keywords"].extend(keywords)

            extracted_sentence_facts.append(sentence_facts)

        return extracted_sentence_facts

    def extract_keywords(self, ontology) -> list:
        """Class, Property and, Instance names from the ontology are used to extract the
        keywords that will be used for pattern matching."""
        keywords = []

        self.add_keywords(keywords, ontology.individuals)
        self.add_keywords(keywords, ontology.classes)
        self.add_keywords(keywords, ontology.properties)

        # Priotize longer keywords
        # Example: so that we correclty pick spaghetti bolognese instead of spaghetti
        keywords = sorted(keywords, key=len, reverse=True)
        return keywords

    def add_keywords(self, keywords: list, ontology_module) -> None:
        """Add the different names as keywords, module_instance is either a class,
        property or instance"""
        for module_instance in ontology_module():
            # Get the name of the property
            name = module_instance.name

            # Convert camel case or Pascal case to separate words
            formatted_name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)

            keywords.append(formatted_name.lower())
