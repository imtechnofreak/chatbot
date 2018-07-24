all: train-nlu train-conversation run

run:
	python -m rasa_core.run -d models/dialogue -u models/nlu/current

train-nlu:
	python -m rasa_nlu.train -c nlu_model_config.json --fixed_model_name current

train-conversation:
	python -m rasa_core.train -s data/stories.md -d domain.yml -o models/dialogue --epochs 300

