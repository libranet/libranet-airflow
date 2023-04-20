# This is a comment.
# See ../makefile

.PHONY: jupyter-start ## Start jupyter-lab
jupyter-start:
	jupyter lab


.PHONY: jupyter-show-kernels ## Show list of available kernels
jupyter-show-kernels:
	jupyter kernelspec list


.PHONY: jupyter-show-paths ## Show configuration paths
jupyter-show-paths:
	jupyter --path


.PHONY: jupyter-notebooks-generate-config  ## Generate config for jupyter notebooks
jupyter-notebooks-generate-config:
	jupyter notebooks --generate-config


.PHONY: jupyter-lab-generate-config  ## Generate config for jupyter lab
jupyter-lab-generate-config:
	jupyter lab --generate-config