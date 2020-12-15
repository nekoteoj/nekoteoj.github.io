from dataclasses import dataclass

@dataclass
class Config:
    root_dir: str
    src_dir: str
    data_dir: str
    style_dir: str
    template_dir: str
    route_path: str
    output_dir: str
