class QueryMaker:
    def __init__(self, ontology):
        self.ontology = ontology
        # order of the categories in the patterns is important,
        self.is_healthy_pattern = ["Health", "Food"]
        self.is_healthy_meal_pattern = ["Food", "MealType", "Health"]
        self.food_pattern = ["Recipe", "Food"]
        self.injury_treatment_pattern = ["Physical", "Health", "Medicine"]

    def make_queries(self, facts: list) -> list:
        queries = []

        for fact in facts:
            sentence = fact["sentence"]
            keywords = fact["keywords"]

            # is healthy query
            is_healthy = self.combination_exists(keywords, self.is_healthy_pattern)
            if is_healthy:
                food = self.value_of_key("Food", is_healthy)
                query = self.generate_is_healthy(food)
                queries.append(query)

            # is healthy meal query
            is_healthy_meal = self.combination_exists(
                keywords, self.is_healthy_meal_pattern
            )
            if is_healthy_meal:
                food = self.value_of_key("Food", is_healthy_meal)
                meal = self.value_of_key("MealType", is_healthy_meal)
                query = self.generate_is_healthy_meal(food, meal)
                queries.append(query)

            # has ingredient query
            has_ingredients = self.combination_exists(keywords, self.food_pattern)
            if has_ingredients:
                recipe = self.value_of_key("Recipe", has_ingredients)
                food = self.value_of_key("Food", has_ingredients)
                query = self.generate_has_ingredient(recipe, food)
                queries.append(query)

            # can cause and can treat query
            can_cause_and_treat = self.combination_exists(
                keywords, self.injury_treatment_pattern
            )
            if can_cause_and_treat:
                sport = self.value_of_key("Physical", can_cause_and_treat)
                injury = self.value_of_key("Health", can_cause_and_treat)
                treatment = self.value_of_key("Medicine", can_cause_and_treat)
                query = self.generate_can_cause_and_can_treat(sport, injury, treatment)
                queries.append(query)

        return queries

    def combination_exists(self, keys: list, combinations: list) -> list:
        """In this function we check if the combination of categories exists in the
        keywords. To make sure that not the same item is used twice, we use a stack"""

        keywords: list = keys.copy()
        matched_keywords = []

        # result with removing things from stack
        print()
        print("Combinations: ", combinations)
        print("Keywords: ", keywords)
        for pattern in combinations:
            print("Checking pattern: ", pattern)
            for item in keywords:
                print("Checking item: ", item)
                if self.pattern_in_values(pattern, item) or pattern in item.keys():
                    print("Pattern matched: ", pattern)
                    print(self.get_key_name(item))
                    matched_keywords.append({pattern: self.get_key_name(item)})
                    keywords.remove(item)
                    print("Added to Matched Keywords: ", matched_keywords)
                    break
        if matched_keywords.__len__() == combinations.__len__():
            print("Matched Keywords: ", matched_keywords)
            return matched_keywords
        print("Matched Keywords: ", [])
        return []

    def generate_is_healthy(self, food: str):
        Food = self.ontology.search_one(iri=f"*{food}")
        return {
            f"Question: Is {food} healthy?",
            f"DL Query: {food} and isHealthy value True",
            f"Result: {self.ontology.search(iri=Food.iri, isHealthy=True)}",
        }

    def generate_is_healthy_meal(self, food: str, meal: str):
        Food = self.ontology.search_one(iri=f"*{food}")
        Meal = self.ontology.search_one(iri=f"*{meal}")
        return {
            f"Question: Is {food} a healthy {meal}?",
            f"DL Query: {food} and isHealthy value True and hasMealType value {meal}",
            f"Result: {self.ontology.search(iri=Food.iri, isHealthy=True, hasMealType=Meal)}",
        }

    def generate_has_ingredient(self, recipe: str, food: str):
        Recipe = self.ontology.search_one(iri=f"*{recipe}")
        Food = self.ontology.search_one(iri=f"*{food}")
        return {
            f"Question: Can you make {recipe} without {food}?",
            f"DL Query: {recipe} and hasIngredient value {food}",
            f"Result: {self.ontology.search(iri=Recipe.iri, hasIngredient=Food)}",
        }

    def generate_can_cause_and_can_treat(self, sport: str, injury: str, treatment: str):
        Sport = self.ontology.search_one(iri=f"*{sport}")
        Injury = self.ontology.search_one(iri=f"*{injury}")
        Treatment = self.ontology.search_one(iri=f"*{treatment}")
        return {
            f"Can {sport} cause an {injury} that can be treated by {treatment}?",
            f"DL Query: inverse canCauseInjury value {sport} and treatedBy value {treatment}",
            f"Result: {self.ontology.search(iri=Sport.iri, canCauseInjury=Injury, treatedBy=Treatment)}",
        }

    def get_key_name(self, keyword: dict) -> str:
        return list(keyword.keys())[0]

    def pattern_in_values(self, pattern: str, item: dict) -> bool:
        """Check if the pattern exicts in the values of the item.
        These values can be a tuple, so we need to check if the pattern is in the tuple."""
        return any(
            pattern in value if isinstance(value, tuple) else pattern == value
            for value in item.values()
        )

    def value_of_key(self, key: str, keywords: list) -> str:
        """Returns the value of the key in the keywords list. Empty str should be returned.
        Since these keywords have been checked in the combination_exists function."""
        for keyword in keywords:
            if key in keyword.keys():
                return keyword[key]

        return "NOT FOUND IN KEYWORDS"
