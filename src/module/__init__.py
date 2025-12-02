def try_load_arg_file(args, arg):
	from logging import warning
	from pathlib import Path

	key = arg.replace("-", "_")
	if args[key] != None:
		filePath = Path(args[key])
		if not filePath.is_file():
			warning("--" + arg + " file does not exist: " + args[key])
			args[key] = None

def init():
	from .core.io.qtio import QtIOBackend
	from .core.io.image import Image
	from . import gui
	
	from logging import DEBUG, basicConfig, FileHandler, root
	basicConfig(level=DEBUG)

	from argparse import ArgumentParser, BooleanOptionalAction

	parser = ArgumentParser()
	parser.add_argument('--logfile', help='Writes errors and information to the specified file.', metavar="LOG_FILE")
	parser.add_argument('--config', help='Uses the specified app config path instead of the installation config path.', metavar="CONFIG_FILE")
	parser.add_argument('--preset', help='Load a specific json preset.', metavar="PRESET_FILE")
	parser.add_argument('--export-vmt', help='Sets VMT export path, immediately exports, and closes the app (if successful).', metavar="VMT_FILE")
	args = parser.parse_args()

	if args.logfile != None:
		from .core.config import root_path
		root.addHandler(FileHandler(root_path / args.logfile))

	# TODO: Better way to list these...
	for key in ["config", "preset"]:
		try_load_arg_file(args.__dict__, key)

	Image.set_backend(QtIOBackend)
	gui.start_gui(args)
