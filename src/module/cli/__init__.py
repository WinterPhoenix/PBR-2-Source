from ..version import __version__
import logging as log

from ..core.config import AppConfig, load_config
from ..core.preset import Preset
from ..gui.backend import CoreBackend

from traceback import format_exc

def start_cli(args):
	print("PBR-2-Source v" + __version__ + " (CLI)\n")

	if args.preset == None:
		log.error("--preset must be specified when using --cli!")
		return

	if args.export_vmt == None:
		log.error("--export-path must be specified when using --cli!")
		return

	log.info("Attempting to load preset: " + args.preset)
	preset = Preset.load(args.preset)

	config = load_config(False, pathOverride=args.config)

	export(config, preset, args.export_vmt)

# Stripped down version of gui.MainWindow.export
# TODO: Unfinished (gui.backend needs to be separated from gui module)
## AttributeError: type object 'Image' has no attribute 'backend'
def export(config: AppConfig, preset: Preset, exportVMTPath: str, noCache=True):
	backend = CoreBackend()
	backend.game = preset.game
	backend.mode = preset.mode
	backend.normalType = preset.normalType
	backend.scaleTarget = preset.scaleTarget
	backend.load_preset(preset)
	backend.pick_vmt(exportVMTPath)

	overwriteVmts = config.overwriteVmts

	try:
		log.info('Creating material...')
		material = backend.make_material(noCache=noCache)

		def log_callback(msg: str|None, percent: int|None):
			log.info(f'Export ({percent}%): {msg}')

		backend.export(material, log_callback, overwrite_vmt=overwriteVmts)

		if config.hijackMode:
			backend.send_engine_command(f'mat_reloadmaterial {backend.name}')

	except Exception as e:
		if isinstance(e, InterruptedError):
			log.info('The export was cancelled by the user.')
		else:
			log.warning(f'The export failed!\n\n{format_exc()}')
