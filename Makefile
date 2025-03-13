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


# Predic
run_pred_model:
	python -c 'from econocast.interface.main import pred; pred(24)'

run_api:
	uvicorn econocast.api.fast:app --reload
