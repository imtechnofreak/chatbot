## repeat
* greet
  - action_greeting
  - slot{"username": "Michael"}
  - utter_greet
  - utter_ask_first_time
* repeat
  - action_repeat

## start
* greet
  - action_greeting
  - slot{"username": "John"}
  - utter_greet
  - utter_ask_first_time
* affirm
  - utter_tutorial
  - utter_question_start
> check_topic

## no tutorial
* greet
  - action_greeting
  - slot{"username": "Michael"}
  - utter_greet
  - utter_ask_first_time
* deny
  - utter_ack
  - utter_question_start
> check_topic

## family
> check_topic
* topic_start{"topic": "family"}
  - utter_topic_confirm
  - action_family
  - utter_ask_who
* family_who{"PERSON": "Emma"}
  - utter_ack_person
  - utter_friends_questions
* friend_info
  - utter_interested

## story
> check_topic
* topic_start{"topic": "storytelling"}
  - utter_topic_confirm
  - action_storytelling

## weather
> check_topic
* topic_start{"topic": "weather"}
  - utter_topic_confirm
  - action_weather
> weather_inform

## weather conversation
> weather_inform
  - slot{"city": "Montreal"}
  - slot{"temperature": "5"}
  - utter_weather_info
* weather_comment
  - utter_weather_comment
* affirm
  - utter_agree


## Generated Story -8331058932264295610
* greet
  - action_greeting
  - slot{"username": "Michael"}
  - utter_greet
  - utter_ask_first_time
* deny
    - utter_ack
    - utter_question_start
* topic_start{"topic": "weather"}
    - slot{"topic": "weather"}
    - utter_topic_confirm
    - action_weather
    - slot{"city": "Waterloo", "temperature": "-4"}
    - utter_weather_info