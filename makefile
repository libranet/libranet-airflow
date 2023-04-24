# This is a comment.
# Important: You *must* indent using <TAB>s, not spaces.
#
# For more information, please see
#   - https://www.gnu.org/software/make/manual/make.html
#
# General syntax:
#   targets : prerequisites; recipes
#   <TAB>recipe
#
# - Commands starting with
#     "-" are ignoring their exit-code.
#     "@" do not echo the command itself.
#
# - make starts a new shell process for each recipe line.
#   Thus shell variables, even exported environment variables, cannot propagate upwards.
#   Therefore better concatenate your multiline-commands with ";\" into a single line.

PROJECT_NAME='libranet-airflow'

# include re-usable makefiles
-include .make/*.mk


.PHONY: install  ## full initial installation
install: create-dirs create-dirs-extra dotenv-install poetry-install pip-upgrade symlink-venv-dirs symlinks-extra


.PHONY: create-dirs-extra ## initialize dir-structure, create dirs & symlinks
create-dirs-extra:
	mkdir -p var/airflow
	mkdir -p var/airflow/dags
	mkdir -p var/airflow/plugins


.PHONY: symlinks-extra ## extra usability symlinks
symlinks-extra:
	- cd bin && ln -sf ipython ip && cd -
	- cd etc && ln -sf ../var/airflow/airflow.cfg airflow.cfg && cd -
	- cd var/log && ln -sf ../airflow/logs airflow && cd -
