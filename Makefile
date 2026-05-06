.PHONY: validate validate-regis

validate: validate-regis

validate-regis:
	python3 tools/validate_regis_protocol_pack.py
