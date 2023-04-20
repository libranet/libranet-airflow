# This is a comment.
# See ../makefile


.PHONY: twine-upload  ## Upload packages
twine-upload:
	twine upload var/wheels/*.whl --skip-existing --verbose
