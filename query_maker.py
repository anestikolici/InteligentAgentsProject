class QueryMaker:
    def __init__(self, ontology):
        self.ontology = ontology
        # order of the categories in the patterns is important,
        self.is_healthy_pattern = ["NonAlcoholicDrink", "Health"]
        self.is_healthy_meal_pattern = ["Food", "MealType", "Health"]
        self.food_pattern = [("Food", "Recipe"), ("Recipe", "Food"), "Food"]
        self.injury_treatment_pattern = ["Physical", "Health", "Medicine"]

    def make_queries(self, facts: list) -> list:
        queries = []

        for fact in facts:
            sentence = fact["sentence"]
            keywords = fact["keywords"]

            # is healthy query
            is_healthy = self.combination_exists(keywords, self.is_healthy_pattern)
            if is_healthy:
                query = self.generate_is_healthy(is_healthy[0])
                queries.append(query)

            # is healthy meal query
            is_healthy_meal = self.combination_exists(
                keywords, self.is_healthy_meal_pattern
            )
            if is_healthy_meal:
                query = self.generate_is_healthy_meal(
                    is_healthy_meal[0], is_healthy_meal[1]
                )
                queries.append(query)

            # has ingredient query
            has_ingredients = self.combination_exists(keywords, self.food_pattern)
            if has_ingredients:
                query = self.generate_has_ingredient(
                    has_ingredients[0], has_ingredients[1]
                )
                queries.append(query)

            # can cause and can treat query
            can_cause_and_treat = self.combination_exists(
                keywords, self.injury_treatment_pattern
            )
            if can_cause_and_treat:
                query = self.generate_can_cause_and_can_treat(
                    can_cause_and_treat[0],
                    can_cause_and_treat[1],
                    can_cause_and_treat[2],
                )
                queries.append(query)

        return queries

    def combination_exists(self, keywords: list, combinations: list) -> list:
        """In this function, we check if the exact combination of categories exists in the
        keywords. If it does, we return the keywords that match the combination."""

        # Get all keyword values, if the value is "Thing" we take the key as the value
        # since its not descriptive enough for pattern matching
        keyword_values = []
        for keyword in keywords:
            for value in keyword.values():
                if value == "Thing":
                    keyword_values.append(self.get_key_name(keyword))
                else:
                    keyword_values.append(value)

        # Get all keyword keys
        keyword_keys = []
        for keyword in keywords:
            keyword_keys.append(self.get_key_name(keyword))

        result = []
        for pattern in combinations:
            if pattern in keyword_values:
                result.append(keyword_keys[keyword_values.index(pattern)])
            else:
                return []

        # remove duplicates without changing order
        result = list(dict.fromkeys(result))
        return result

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
