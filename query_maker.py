class QueryMaker:
    def __init__(self, ontology):
        self.ontology = ontology

        # order is sometimes important, because we might take a recipe as a food first
        self.is_healthy_pattern = ["Food", "Health"]
        self.is_healthy_meal_pattern = ["Food", "MealType", "Health"]
        self.food_pattern = ["Recipe", "Food"]
        self.is_recipe_pattern = ["Food", "Recipe"]
        self.nutrient_pattern = ["Food", "Nutrient"]
        self.injury_treatment_pattern = ["Physical", "Health", "Medicine"]
        self.non_cooking_pattern = ["Food", "NonCooking"]
        self.cooking_pattern = ["Food", "CookingMethod"]
        self.disease_food_pattern = ["Food", "Disease"]
        self.disease_symptom_pattern = ["Disease", "Symptom"]
        self.disease_pain_pattern = ["Disease", "Pain"]
        self.treat_injury_pattern = ["Injury", "Treatment"]
        self.disease_effect_physical_pattern = ["Disease", "Physical"]
        self.disese_effect_body_part_pattern = ["Disease", "BodyPart"]

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

            # is recipe query
            is_recipe = self.combination_exists(keywords, self.is_recipe_pattern)
            if is_recipe:
                food = self.value_of_key("Food", is_recipe)
                query = self.generate_is_recipe(food)
                queries.append(query)

            # has nutrient query
            has_nutrient = self.combination_exists(keywords, self.nutrient_pattern)
            if has_nutrient:
                food = self.value_of_key("Food", has_nutrient)
                nutrient = self.value_of_key("Nutrient", has_nutrient)
                query = self.generate_has_nutrient(food, nutrient)
                queries.append(query)

            # has cooking method
            has_cooking_method = self.combination_exists(keywords, self.cooking_pattern)
            if has_cooking_method:
                food = self.value_of_key("Food", has_cooking_method)
                method = self.value_of_key("CookingMethod", has_cooking_method)
                query = self.generate_can_be_prepared(food, method)
                queries.append(query)

            # has non cooking method
            has_non_cooking_method = self.combination_exists(
                keywords, self.non_cooking_pattern
            )
            if has_non_cooking_method:
                food = self.value_of_key("Food", has_non_cooking_method)
                method = self.value_of_key("NonCooking", has_non_cooking_method)
                query = self.generate_can_be_prepared(food, method)
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

            # disease food query
            disease_food = self.combination_exists(keywords, self.disease_food_pattern)
            if disease_food:
                food = self.value_of_key("Food", disease_food)
                disease = self.value_of_key("Disease", disease_food)
                query = self.generate_disease_food(food, disease)
                queries.append(query)

            # disease symptom query
            disease_symptom = self.combination_exists(
                keywords, self.disease_symptom_pattern
            )
            if disease_symptom:
                disease = self.value_of_key("Disease", disease_symptom)
                symptom = self.value_of_key("Symptom", disease_symptom)
                query = self.generate_disease_symptom(disease, symptom)
                queries.append(query)

            # disease pain query
            disease_pain = self.combination_exists(keywords, self.disease_pain_pattern)
            if disease_pain:
                disease = self.value_of_key("Disease", disease_pain)
                pain = self.value_of_key("Pain", disease_pain)
                query = self.generate_disease_symptom(disease, pain)
                queries.append(query)

            # treat injury query
            treat_injury = self.combination_exists(keywords, self.treat_injury_pattern)
            if treat_injury:
                injury = self.value_of_key("Injury", treat_injury)
                treatment = self.value_of_key("Treatment", treat_injury)
                query = self.generate_treat_injury(injury, treatment)
                queries.append(query)

            # disease effect physical query
            disease_effect_physical = self.combination_exists(
                keywords, self.disease_effect_physical_pattern
            )
            if disease_effect_physical:
                disease = self.value_of_key("Disease", disease_effect_physical)
                physical = self.value_of_key("Physical", disease_effect_physical)
                query = self.generate_disease_effect(disease, physical)
                queries.append(query)

            # disease effect body part query
            disease_effect_body_part = self.combination_exists(
                keywords, self.disese_effect_body_part_pattern
            )
            if disease_effect_body_part:
                disease = self.value_of_key("Disease", disease_effect_body_part)
                body_part = self.value_of_key("BodyPart", disease_effect_body_part)
                query = self.generate_disease_effect(disease, body_part)
                queries.append(query)

        return queries

    def combination_exists(self, keys: list, combinations: list) -> list:
        """In this function we check if the combination of categories exists in the
        keywords. To make sure that not the same item is used twice, we use a stack"""

        keywords: list = keys.copy()
        matched_keywords = []

        # TODO: remove these print statments for testing
        # print()
        # print("Check combinations: ", combinations)
        # print("Keywords start: ", keywords)

        # Check for each item in the combination if it exists in the keywords
        for pattern in combinations:
            # print("Pattern: ", pattern)
            for item in keywords:
                # print("Item: ", item)
                if self.pattern_in_values(pattern, item) or pattern in item.keys():
                    matched_keywords.append({pattern: self.get_key_name(item)})
                    keywords.remove(item)
                    # print("Keywords: ", keywords)
                    break
        if matched_keywords.__len__() == combinations.__len__():
            return matched_keywords

        return []

    def generate_is_healthy(self, food: str):
        Food = self.ontology.search_one(iri=f"*{food}")
        return {
            "Question": f"Is {food} healthy?",
            "DL Query": "{" f"{food}" "} and isHealthy value True",
            "Result": f"{self.ontology.search(iri=Food.iri, isHealthy=True)}",
        }

    def generate_is_healthy_meal(self, food: str, meal: str):
        Food = self.ontology.search_one(iri=f"*{food}")
        Meal = self.ontology.search_one(iri=f"*{meal}")
        return {
            "Question": f"Is {food} a healthy {meal}?",
            "DL Query": "{"
            f"{food}"
            "}"
            f" and isHealthy value True and hasMealType value {meal}",
            "Result": f"{self.ontology.search(iri=Food.iri, isHealthy=True, hasMealType=Meal)}",
        }

    def generate_is_recipe(self, food: str):
        Food = self.ontology.search_one(iri=f"*{food}")
        return {
            "Question": f"Is {food} a Recipe?",
            "DL Query": "{" f"{food}" "} and Recipe",
            "Result": f"{[Food] if self.ontology.Recipe in Food.is_a else []}",
        }

    def generate_has_ingredient(self, recipe: str, food: str):
        Recipe = self.ontology.search_one(iri=f"*{recipe}")
        Food = self.ontology.search_one(iri=f"*{food}")
        return {
            "Question": f"Can you make {recipe} with {food}?",
            "DL Query": "{" f"{recipe}" "}" f" and hasIngredient value {food}",
            "Result": f"{self.ontology.search(iri=Recipe.iri, hasIngredient=Food)}",
        }

    def generate_has_nutrient(self, food: str, nutrient: str):
        Nutrient = self.ontology.search_one(iri=f"*{nutrient}")
        Food = self.ontology.search_one(iri=f"*{food}")
        return {
            "Question": f"Is {nutrient} the main nutrient of {food}?",
            "DL Query": "{"
            f"{nutrient}"
            "}"
            f" and inverse hasMainNutrient value {food}",
            "Result": f"{self.ontology.search(iri=Food.iri, hasMainNutrient=Nutrient)}",
        }

    def generate_can_cause_and_can_treat(self, sport: str, injury: str, treatment: str):
        Sport = self.ontology.search_one(iri=f"*{sport}")
        Injury = self.ontology.search_one(iri=f"*{injury}")
        Treatment = self.ontology.search_one(iri=f"*{treatment}")
        return {
            "Question": f"Can {sport} cause an {injury} that can be treated by {treatment}?",
            "DL Query": f"inverse canCauseInjury value {sport} and treatedBy value {treatment}",
            "Result": f"{self.ontology.search(iri=Sport.iri, canCauseInjury=Injury, treatedBy=Treatment)}",
        }

    def generate_can_be_prepared(self, food: str, method: str):
        Food = self.ontology.search_one(iri=f"*{food}")
        Method = self.ontology.search_one(iri=f"*{method}")
        return {
            "Question": f"Is {method} a preparation method for {food}?",
            "DL Query": "{" f"{food}" "}" f" and hasPreparationMethod value {method}",
            "Result": f"{self.ontology.search(iri=Food.iri, hasPreparationMethod=Method)}",
        }

    def generate_disease_food(self, food: str, disease: str):
        Food = self.ontology.search_one(iri=f"*{food}")
        Disease = self.ontology.search_one(iri=f"*{disease}")

        results = self.ontology.search(iri=Food.iri, canCauseDisease=Disease)

        # Check all ingredients of the food if they can cause the disease
        for ingredient in Food.hasIngredient:
            if hasattr(ingredient, "canCauseDisease"):
                if Disease in ingredient.canCauseDisease:
                    results.append(ingredient)

        return {
            "Question": f"Can {food} cause {disease}?",
            "DL Query": f"{food} and canCause value {disease} and inverse contains value {food} and canCause value {disease}",
            "Result": results,
        }

    def generate_disease_symptom(self, disease: str, symptom: str):
        Disease = self.ontology.search_one(iri=f"*{disease}")
        Symptom = self.ontology.search_one(iri=f"*{symptom}")
        return {
            "Question": f"Does {disease} have {symptom} as a symptom?",
            "DL Query": "{" f"{symptom}" "}" f" and inverse hasSymptom value {disease}",
            "Result": f"{self.ontology.search(iri=Disease.iri, hasSymptom=Symptom)}",
        }

    def generate_treat_injury(self, injury: str, treatment: str):
        Injury = self.ontology.search_one(iri=f"*{injury}")
        Treatment = self.ontology.search_one(iri=f"*{treatment}")
        return {
            "Question": f"Can a {treatment} treat a {injury}?",
            "DL Query": "{" f"{treatment}" "}" f" and treats value {injury}",
            "Result": f"{self.ontology.search(iri=Treatment.iri, treats=Injury)}",
        }

    def generate_disease_effect(self, disease: str, affected: str):
        Disease = self.ontology.search_one(iri=f"*{disease}")
        Affected = self.ontology.search_one(iri=f"*{affected}")
        return {
            "Question": f"Can {disease} have an effect on {affected}?",
            "DL Query": f"inverse usesBodyPart value {affected} and inverse hasEffectOn value {disease}",
            "Result": f"{self.ontology.search(iri=Disease.iri, hasEffectOn=Affected)}",
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
