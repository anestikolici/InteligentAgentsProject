import re


class Extractor:
    def __init__(self, ontology):
        self.keywords_dict = {}
        self.extract_keywords(ontology)

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

            # If the keyword is a tuple, it means that the keyword has a class,
            # otherwise its a property
            keywords_to_match = [
                self.format_keyword(item) for item in self.keywords_dict
            ]

            pattern = r"\b(?:{})\b".format("|".join(map(re.escape, keywords_to_match)))

            matched_keywords = re.findall(
                pattern,
                singular_sentence,
                re.IGNORECASE,
            )

            # For each matched keyword, add the corresponding tuple (keyword, class/property)
            for matched in matched_keywords:
                for key, value in self.keywords_dict.items():
                    if key.lower() == matched.lower():
                        sentence_facts["keywords"].append({key: value})

            extracted_sentence_facts.append(sentence_facts)

        return extracted_sentence_facts

    def extract_keywords(self, ontology) -> None:
        """Class, Property and, Instance names from the ontology are used to extract the
        keywords that will be used for pattern matching."""

        self.add_keywords(ontology.individuals)
        self.add_keywords(ontology.classes)
        self.add_keywords(ontology.properties)

    def add_keywords(self, ontology_module) -> None:
        """Add the different names as keywords, module_instance is either a class,
        property or instance"""
        for module_instance in ontology_module():
            # Get the name of the module_instance (class, property, or instance)
            name = module_instance.name

            # Collect all parent classes (is_a may include multiple parents)
            instance_classes = [parent.name for parent in module_instance.is_a]

            # Add the keyword as a key in the dictionary, with its parent classes as values
            # Add the keyword as a tuple if there are multiple parent classes. This logic
            # is used for the combination_exists function of QueryMaker
            if len(instance_classes) == 1:
                self.keywords_dict[name] = instance_classes[0]
            else:
                self.keywords_dict[name] = tuple(instance_classes)

    def format_keyword(self, keyword: str) -> str:
        return re.sub(r"([a-z])([A-Z])", r"\1 \2", keyword).lower()
