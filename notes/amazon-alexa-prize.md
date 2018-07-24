# Slugbot

* Ask user to clarify input, but estimate utterance if asked too many times
* NLU w/ Stanford CoreNLP Toolkit
* Homegrown named entity recognizer
* Topic classifier + NPS dialogue act classifier
* 2 memory management systems (LTM & STM)

* Dialogue manager:
    * Handles basic functionality
        * repeat requests, stop requests, prompt menus, help
        * Maximize unique experiences, prioritize unexplored topics
    * Mixed initiative: learn more about the user by asking or soliciting their opinion of a contextually relevant entity
    * Important to provide and justify our own opinions
    * If an entity is detected but can't formulate direct follow-up utterance:
        1. ask the user for more information
        2. Verify the entity by asking about related synonyms
        3. search engine to try and retrieve some summary based response
        4. Else, moving on...
    * System drives content with stories
        * Entertaining experience
        * 40 narratives, 10-20 sentences that user can step through
    * Flow manager
        * Graph structure
        * Flow triggered by a given topic using keyword or expressing interest
        * 31 flows
        * Reusing successful modules is a good boostrapping technique

    * Scoring:
        * Incoherence within statement, derive .15 penalty score to the responses

# Pixie

* Primarily template-based
* Flask, StanfordNLP, AIML, Profanity, DynamoDB, boto3
* Computational graph
