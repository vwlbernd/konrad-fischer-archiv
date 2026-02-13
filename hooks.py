import os
import shutil
from mkdocs.config import Config

def on_post_build(config: Config):
    # Pfad zum Quellordner (außen)
    site_medien_dir = os.path.join(config['site_dir'], 'medien')
    source_medien_dir = os.path.join(os.path.dirname(config.config_file_path), 'medien')