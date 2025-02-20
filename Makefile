.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y econocast || :
	@pip install -e .

# Prueba
run_load_data:
	python -c 'from econocast.ml_logic.data import load_data; load_data()'

# Preprocesamiento
run_preprocess_data:
	python -c 'from econocast.interface.main import preprocess; preprocess()'

# Entrenamiento
run_train_model:
	python -c 'from econocast.interface.main import train; train()'

# Evaluacion
run_evaluate_model:
	python -c 'from econocast.interface.main import evaluate; evaluate()'

# Predic
run_pred_model:
	python -c 'from econocast.interface.main import pred; pred()'

run_api:
	uvicorn econocast.api.fast:app --reload
