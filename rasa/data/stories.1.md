## happy path               <!-- name of the story - just for debugging -->
* greet              
  - utter_greet
* mood_great               <!-- user utterance, in format _intent[entities] -->
  - utter_happy

## sad path 1               <!-- this is already the start of the next story -->
* greet
  - utter_greet             <!-- action of the bot to execute -->
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## say ner
* ner
  - utter_interested

## weather start
* start
  - utter_greet
  - utter_tutorial
* weather_start
  - utter_topic_confirm
* affirm
  - utter_ack

## weather comment
* start
  - utter_greet
  - utter_tutorial
* weather_start
  - utter_topic_confirm
* weather_comment
  - utter_agree

## weather change topic
* start
  - utter_greet
  - utter_tutorial
* weather_start
  - utter_topic_confirm
* topic_change
  - utter_topic_change

## suicide
* suicide
  - utter_prevention