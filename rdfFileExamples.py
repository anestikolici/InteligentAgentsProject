from owlready2 import get_ontology, sync_reasoner

ontology = get_ontology("draftOntology.rdf").load()
with ontology:
    sync_reasoner(infer_property_values=True)

# extract classes, properties and instances from the ontology
for c in ontology.classes():
    print("Class: ", c)
    for i in c.instances():
        print("Instance: ", i)

print("Properties:")
for p in ontology.properties():
    print(p)


# Query example 1
# Question: Is bread a healthy breakfast?
Bread = ontology.search_one(iri="*Bread")

print()
print("Result: ", ontology.search(iri=Bread.iri, isHealthy=[True]))

# Query example 1
# Question: Do you need milk to create a toastie?
Toastie = ontology.search_one(iri="*Toastie")
Milk = ontology.search_one(iri="*Milk")
Bread = ontology.search_one(iri="*Bread")
hasIngredient = ontology.search_one(iri="*hasIngredient")

print()
print("Result: ", ontology.search(iri=Toastie.iri, hasIngredient=Milk))


# Query example 3
# Question: Beer can cause liver disease?
Beer = ontology.search_one(iri="*Beer")
LiverDisease = ontology.search_one(iri="*LiverDisease")

print()
print("Result: ", ontology.search(iri=Beer.iri, canCauseDisease=LiverDisease))

# Query example 4
# Question: Can a cake cause salmonella?
Cake = ontology.search_one(iri="*Cake")
Salmonella = ontology.search_one(iri="*Salmonella")

results = []

for ingredient in Cake.hasIngredient:
    if hasattr(ingredient, "canCauseDisease"):
        if Salmonella in ingredient.canCauseDisease:
            results.append(ingredient)

print("Result: ", results)
