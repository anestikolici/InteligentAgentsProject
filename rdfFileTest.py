from rdflib import Graph

# Load the ontology into a graph
g = Graph()
ontology_path = "draftOntology.rdf"
g.parse(ontology_path, format="xml")

# Print out basic information about the ontology
print(f"Graph has {len(g)} statements.")

# List all the subjects, predicates, and objects
print("\nTriples in the ontology:")
for subj, pred, obj in g:
    print(f"Subject: {subj}, Predicate: {pred}, Object: {obj}")

# Example: Querying all classes
query = """
    SELECT DISTINCT ?class
    WHERE {
      ?class a owl:Class .
    }
"""
qres = g.query(query)

print("\nClasses in the ontology:")
for row in qres:
    print(row)
