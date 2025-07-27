tool:
	@uv tool uninstall thinky
	@uv cache clean && uv cache prune
	@uv tool install -e .
