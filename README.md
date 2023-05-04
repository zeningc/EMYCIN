# EMYCIN
## Overview
This project is a python-version EMYCIN expert system. 
EMYCIN is an early expert system developed in the 1970s for the diagnosis and treatment of bacterial infections. 
It was one of the first successful applications of artificial intelligence (AI) in the medical field. EMYCIN was 
designed to assist physicians in diagnosing bacterial infections and prescribing appropriate antibiotic treatments. 
It used a set of rules based on expert knowledge to analyze patient data and make recommendations. EMYCIN paved the 
way for the development of more advanced medical expert systems and helped demonstrate the potential of AI in healthcare.  
The initial implementation of this project was based on EMYCIN, which was originally developed using Common Lisp. 
However, in order to make the code more accessible to a wider audience, the project has been rewritten in Python. 
Additionally, the code has been improved to allow for rules to be read from JSON files. This update was made in response
to the growing popularity of JSON as a configuration language.

## Inference
EMYCIN relies on three key concepts to diagnose and treat bacterial infections:
1. **Context:** This refers to a set of parameters that are relevant to a particular situation or problem. In the context of EMYCIN, this might include a patient's symptoms, medical history, and test results.

2. **Parameter:** This is a piece of data or information that is relevant to a particular problem or domain. In the context of EMYCIN, parameters might include symptoms like fever, or test results like blood cultures.

3. **Rule:** This is a statement that describes how parameters in a particular context are related. For example, a rule in EMYCIN might state that if a patient has a fever above a certain temperature and a certain type of bacteria is present in their blood culture, then they should be treated with a specific antibiotic. These rules are based on expert knowledge about how to diagnose and treat bacterial infections.

We will dig deep into the code later. To conclude, a context contains two types of parameters: initial and goal. The initial
parameters are the basic parameters that serve as the background knowledge to the problem while the goal parameters are
our target, which means that our goal is to infer the value of goal parameters.  

To calculate the different possibility of different result, a concept called certainty factor(CF) is introduced:  
Certainty factor is a method used in expert systems to quantify the degree of certainty or uncertainty associated with a particular conclusion or rule. It allows an expert system to make more informed decisions by taking into account the strength of evidence supporting a particular conclusion.

In certainty factor, each rule is assigned a numerical value between -1 and 1, which represents the degree of certainty or uncertainty associated with the rule. A value of 1 indicates complete certainty, while a value of -1 indicates complete uncertainty. A value of 0 indicates that the rule is neutral, meaning that it doesn't provide any evidence for or against the conclusion.

When multiple rules are used to reach a conclusion, their certainty factors are combined using a formula that takes into account both their strengths and weaknesses. The resulting certainty factor for the conclusion represents the degree of confidence that the expert system has in its recommendation.

Certainty factor is particularly useful in situations where there is uncertainty or ambiguity in the available data. By allowing for a more nuanced assessment of the evidence, it helps to reduce the risk of incorrect or inappropriate recommendations.

## Code Breakdown
### models.py

#### Imports
- `from typing import Any`: Import `Any` from the `typing` module, which is used for typing annotations.

#### CF Class
- This class contains constant values and calculation methods related to the certainty factor (CF).

#### Context Class
- This class represents the context and contains a dictionary of all created contexts.
- It has a `__str__` method to return a string representation of the object.
- There is a static method `get_context_by_name` that returns a context object by name.

#### Parameter Class
- This class represents a parameter and contains a dictionary of all created parameters.
- It has a `__hash__` and `__str__` method to return the hash and string representation of the object.
- There are static methods `get_parameter_by_name` and `get_value` for retrieving parameter objects and their values.

#### Statement Class
- This class represents a statement, which can be a condition or conclusion.
- It has a `meet` method to check if a statement meets a certain condition.
- There is a `__str__` method to return a string representation of the object.

#### Store Class
- This class represents a global key/value store.
- It has static methods `get_vals` and `update_cf` for getting values and updating the certainty factor.

#### Rule Class
- This class represents a rule, containing conditions, conclusions, and an associated certainty factor.
- It has a `__str__` method to return a string representation of the object.
- There are methods `applicable`, `apply`, `use_rules`, and `eval_condition` for rule evaluation and application.

#### Executor Class
- This class contains several local variables used during runtime and helper methods for execution.
- It has methods `ask`, `explain`, `set_current_rule`, `find_out`, `execute`, and `output_result` for user interaction, execution, and output of results.

#### Execution Flow
1. Define instances of `Context`, `Parameter`, and `Rule`.
2. Call `Executor.execute()` with a list of context names to execute the program.
3. Results are printed to the console and returned as a dictionary.

### run.py
This code is a configuration script for the EMYCIN (Empty MYcin) expert system shell, which is a framework for creating rule-based expert systems. The script reads a JSON file containing the expert system's structure, and then creates Context, Parameter, and Rule objects based on the information in the file.

Here's a breakdown of the code:

1. **Import required libraries:**
   - `json`: for parsing and loading JSON data.
   - `argparse`: for parsing command-line arguments.
   - `os.path`: for checking file existence.
   - `models`: import custom classes for Context, Parameter, Rule, and Executor.

2. `create_objects(json_data)`: This function initializes the expert system by creating Context, Parameter, and Rule objects using the data from the JSON file.

3. `get_all_context(json_str)`: This function extracts all the context names from the JSON string and returns a list of them.

4. `config_args(json_dict, arg_tuple)`: This function takes a dictionary from the JSON file and a tuple of keys, filters the dictionary to only include the keys in the tuple, and returns a new dictionary.

5. `create_parameter(parameters)`: This function creates Parameter objects using the provided list of dictionaries that represent parameters.

6. `create_context(contexts)`: This function creates Context objects using the provided list of dictionaries that represent contexts.

7. `create_rule(rules)`: This function creates Rule objects using the provided list of dictionaries that represent rules.

8. `create_parser()`: This function sets up an ArgumentParser object for parsing command-line arguments. It specifies a single argument, "--config", which represents the path to the JSON file.

9. **Main section:**
   - Calls `create_parser()` to set up an ArgumentParser object.
   - Parses command-line arguments using `parser.parse_args()`.
   - Checks if the configuration file exists, and exits the program if it does not.
   - Reads the contents of the JSON file and stores it in a string.
   - Calls `create_objects(json_str)` to create the expert system objects.
   - Calls `Executor.execute(get_all_context(json_str))` to execute the expert system.
### organism.json
Rule definition file:
```json
{
  "contexts": [
    {
      "name": "patient",
      "initial_data": [
        "name",
        "sex",
        "age"
      ]
    },
    {
      "name": "culture",
      "initial_data": [
        "site",
        "days-old"
      ]
    },
    {
      "name": "organism",
      "goals": [
        "identity"
      ]
    }
  ],
  "parameters": [
    {
      "name": "name",
      "ctx_name": "patient",
      "param_type": "str",
      "ask_first": true
    },
    {
      "name": "sex",
      "ctx_name": "patient",
      "allowed_values": [
        "M",
        "F"
      ],
      "ask_first": true
    },
    {
      "name": "age",
      "ctx_name": "patient",
      "param_type": "int",
      "ask_first": true
    },
    {
      "name": "burn",
      "ctx_name": "patient",
      "allowed_values": [
        "no",
        "mild",
        "serious"
      ],
      "ask_first": true
    },
    {
      "name": "compromised-host",
      "ctx_name": "patient",
      "allowed_values": [
        "True",
        "False"
      ],
      "param_type": "str"
    },
    {
      "name": "site",
      "ctx_name": "culture",
      "allowed_values": [
        "blood"
      ],
      "ask_first": true
    },
    {
      "name": "days-old",
      "ctx_name": "culture",
      "param_type": "int",
      "ask_first": true
    },
    {
      "name": "identity",
      "ctx_name": "organism",
      "allowed_values": [
        "pseudomonas",
        "klebsiella",
        "enterobacteriaceae",
        "staphylococcus",
        "bacteroides",
        "streptococcus"
      ],
      "ask_first": true
    },
    {
      "name": "gram",
      "ctx_name": "organism",
      "allowed_values": [
        "acid-fast",
        "pos",
        "neg"
      ],
      "ask_first": true
    },
    {
      "name": "morphology",
      "ctx_name": "organism",
      "allowed_values": [
        "rod",
        "coccus"
      ]
    },
    {
      "name": "aerobicity",
      "ctx_name": "organism",
      "allowed_values": [
        "aerobic",
        "anaerobic"
      ]
    },
    {
      "name": "growth-conformation",
      "ctx_name": "organism",
      "allowed_values": [
        "chains",
        "pairs",
        "clumps"
      ]
    }
  ],
  "rules": [
    {
      "conditions": [
        [
          "site",
          "culture",
          "=",
          "blood"
        ],
        [
          "gram",
          "organism",
          "=",
          "neg"
        ],
        [
          "morphology",
          "organism",
          "=",
          "rod"
        ],
        [
          "burn",
          "patient",
          "=",
          "serious"
        ]
      ],
      "conclusions": [
        [
          "identity",
          "organism",
          "=",
          "pseudomonas"
        ]
      ],
      "cf": 0.4
    },
    {
      "conditions": [
        [
          "gram",
          "organism",
          "=",
          "pos"
        ],
        [
          "morphology",
          "organism",
          "=",
          "coccus"
        ],
        [
          "growth-conformation",
          "organism",
          "=",
          "clumps"
        ]
      ],
      "conclusions": [
        [
          "identity",
          "organism",
          "=",
          "staphylococcus"
        ]
      ],
      "cf": 0.7
    },
    {
      "conditions": [
        [
          "site",
          "culture",
          "=",
          "blood"
        ],
        [
          "gram",
          "organism",
          "=",
          "neg"
        ],
        [
          "morphology",
          "organism",
          "=",
          "rod"
        ],
        [
          "aerobicity",
          "organism",
          "=",
          "anaerobic"
        ]
      ],
      "conclusions": [
        [
          "identity",
          "organism",
          "=",
          "bacteroides"
        ]
      ],
      "cf": 0.9
    },
    {
      "conditions": [
        [
          "gram",
          "organism",
          "=",
          "neg"
        ],
        [
          "morphology",
          "organism",
          "=",
          "rod"
        ],
        [
          "compromised-host",
          "patient",
          "=",
          "true"
        ]
      ],
      "conclusions": [
        [
          "identity",
          "organism",
          "=",
          "pseudomonas"
        ]
      ],
      "cf": 0.6
    },
    {
      "conditions": [
        [
          "gram",
          "organism",
          "=",
          "neg"
        ],
        [
          "morphology",
          "organism",
          "=",
          "rod"
        ],
        [
          "aerobicity",
          "organism",
          "=",
          "aerobic"
        ]
      ],
      "conclusions": [
        [
          "identity",
          "organism",
          "=",
          "enterobacteriaceae"
        ]
      ],
      "cf": 0.8
    },
    {
      "conditions": [
        [
          "gram",
          "organism",
          "=",
          "pos"
        ],
        [
          "morphology",
          "organism",
          "=",
          "coccus"
        ],
        [
          "growth-conformation",
          "organism",
          "=",
          "chains"
        ]
      ],
      "conclusions": [
        [
          "identity",
          "organism",
          "=",
          "streptococcus"
        ]
      ],
      "cf": 0.7
    }
  ]
}
```
### animal.json
Another rule that is designed to recognize if an animal is tiger or lion. 

## Transcript
### Determine Organism
```shell
/usr/bin/python3 /Users/zeningc/Desktop/Project/EMYCIN/run.py
Loading context, parameter, and rules from ./organism.json...
Loading done successfully
Ready to load the json...
Json loaded successfully
Ready to create contexts...
Contexts created successfully
Ready to create parameters...
Parameters created successfully
Ready to create rules...
Parameters created successfully
Executing begins, type HELP for help
What is the name of patient? alex
What is the sex of patient? ?
the allowed values of sex are ['M', 'F']
What is the sex of patient? M
What is the age of patient? 22
What is the site of culture? blood
What is the days-old of culture? 3
What is the identity of organism? unknown
What is the gram of organism? why
Why is the value of gram being asked for?
It is known that:
site culture = blood
Therefore, 
RULE 0: IF site culture = blood AND
	gram organism = neg AND
	morphology organism = rod AND
	burn patient = serious THEN
 (0.4)
 identity organism = pseudomonas

What is the gram of organism? ?
the allowed values of gram are ['acid-fast', 'pos', 'neg']
What is the gram of organism? neg
What is the morphology of organism? rod
What is the burn of patient? serious
What is the aerobicity of organism? ?
the allowed values of aerobicity are ['aerobic', 'anaerobic']
What is the aerobicity of organism? aerobic
What is the compromised-host of patient? true
Findings for organism:
identity: enterobacteriaceae 0.8, pseudomonas 0.76

Process finished with exit code 0
```
### Determine Animal
```shell
/usr/bin/python3 /Users/zeningc/Desktop/Project/EMYCIN/run.py --config ./animal.json
Loading context, parameter, and rules from ./animal.json...
Loading done successfully
Ready to load the json...
Json loaded successfully
Ready to create contexts...
Contexts created successfully
Ready to create parameters...
Parameters created successfully
Ready to create rules...
Parameters created successfully
Executing begins, type HELP for help
What is the size of animal? ?
the allowed values of size are ['large', 'medium']
What is the size of animal? large
What is the color of animal? ?
the allowed values of color are ['orange', 'yellow']
What is the color of animal? orange
What is the stripes of animal? why
Why is the value of stripes being asked for?
stripes is one of the initial parameters.
What is the stripes of animal? ?
the allowed values of stripes are ['yes', 'no']
What is the stripes of animal? yes
What is the mane of animal? why
Why is the value of mane being asked for?
mane is one of the initial parameters.
What is the mane of animal? true
Invalid response. Type ? to see legal ones.
What is the mane of animal? ?
the allowed values of mane are ['yes', 'no']
What is the mane of animal? yes
Findings for identification:
identity: tiger 0.8

Process finished with exit code 0
```

## Reference
[1]. Shortliffe, E. H., Davis, R., Axline, S. G., Buchanan, B. G., Green, C. C., Cohen, S. N., & Jacobsen, S. J. (1975). Computer-based consultation in clinical therapeutics: explanation and rule acquisition capabilities of the MYCIN system. Computers and biomedical research, 8(4), 303-320.  
[2]. Norvig, P. (1992). Paradigms of artificial intelligence programming: case studies in Common Lisp. Morgan Kaufmann.  
[3] [EMYCIN](https://dhconnelly.com/paip-python/docs/paip/emycin.html#:~:text=Emycin%20is%20an%20expert%20system,non%2Dexpert%20users%20solve%20problems.)