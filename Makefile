.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y econocast || :
	@pip install -e .

run_api:
	uvicorn econocast.api.fast:app --reload
