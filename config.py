import pathlib
from generator.config import Config

config = Config(
    root_dir=pathlib.Path().absolute(),
    src_dir="src",
    data_dir="data",
    style_dir="styles",
    template_dir="templates",
    route_path="routes.yml",
    output_dir="build"
)
