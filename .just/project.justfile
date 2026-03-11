
# project


# run all install-steps to full initial installation
[group: 'project']
install: create-dirs create-dirs-extra dotenv-install uv-sync-all-groups && symlink-venv-dirs


# create extra dirs
[group: 'dir-structure']
create-dirs-extra:
    mkdir -p var/airflow