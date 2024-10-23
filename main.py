from dialog_manager import DialogManager
import dialog_manager

scenario1 = """In the morning, Harry eats bread for breakfast since its good for his health. 
He then bikes to his university to go to a lecture. 
When his lecture was over he went back home to prepare his lunch. 
He wanted to make pancakes, but had no mayonnaise in hi spantry. 
So instead he made spaghetti Bolognese, this will help his exercise because it contains carbs the most. 
Because Harry recently decided he wanted to work on his health, he drank a soda with his lunch. 
He didn't want any beer, since that would have an effect on his liver, raising a the potential for a liver disease. 
Then Harry went rowing where he got an injury, to treat it he took antibiotics. """

scenario2 = """Today it's Alice's birthday. 
When she is downstairs, her mother follows a cake recipe, where she is boiling and baking, garnishing it. 
Alice eats a piece of cake with her family. 
Alice unfortunately gets salmonella from the cake and as a result, she starts vomiting and has a leg ache."""

scenario3 = """Emily drinks a lot of beer. 
When she rides her bike home, she falls and breaks a bone. 
The fractured bone is treated by a massage therapy. 
She also suffers from a pulled muscle, for this also a massage therapy is used. 
Afterwards she buys milk for the toastie she is going to make. 
Because she often consumes a lot of beer, she gets a liver disease. 
As a result of the liver disease she can't go running."""

if __name__ == "__main__":
    dialog_manager = DialogManager()

    # Extract facts from the scenario1
    dialog_manager.extract_facts(scenario=scenario1)
    print(dialog_manager.facts)

    # Extract facts from the scenario2
    dialog_manager.extract_facts(scenario=scenario2)
    print(dialog_manager.facts)

    # # Extract facts from the scenario3
    dialog_manager.extract_facts(scenario=scenario3)
    print(dialog_manager.facts)

    # Make queries from the facts
    dialog_manager.make_queries()
    print(dialog_manager.queries)

    # all keywords from extractor
    print(dialog_manager.extractor.keywords_dict)
