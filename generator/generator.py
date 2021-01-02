from generator.config import Config
import os
import yaml
import shutil
import minify_html
import jinja2
import sass
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Generator:
    def __init__(self, config: Config):
        self.config = config
        template_path = os.path.join(
            config.root_dir, config.src_dir, config.template_dir)
        self.templateLoader = jinja2.FileSystemLoader(searchpath=template_path)
        self.templateEnv = jinja2.Environment(loader=self.templateLoader)

    def render_html(self, data):
        template = self.templateEnv.get_template(data["file"])
        if "page_data" not in data:
            data["page_data"] = dict()
        html = minify_html.minify(template.render(data["page_data"]))
        return html

    def save_html(self, filename: str, html: str):
        output_file_path = os.path.join(self.config.root_dir,
                                        self.config.output_dir, filename)
        with open(output_file_path, "w") as output_file:
            output_file.write(html)

    def dump_html(self, data, filename: str):
        html = self.render_html(data)
        self.save_html(filename, html)

    def generate(self):
        route_path = os.path.join(self.config.root_dir,
                                  self.config.src_dir,
                                  self.config.route_path)
        data_dir = os.path.join(self.config.root_dir,
                                 self.config.src_dir,
                                 self.config.data_dir)
        output_dir = os.path.join(self.config.root_dir,
                                  self.config.output_dir)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        shutil.copytree(
            os.path.join(self.config.root_dir, "assets"),
            os.path.join(self.config.root_dir, output_dir, "assets")
        )

        style_dir = os.path.join(self.config.root_dir, self.config.src_dir, self.config.style_dir)
        output_style_dir = os.path.join(output_dir, "css")
        os.makedirs(output_style_dir)
        sass.compile(dirname=(style_dir, output_style_dir), output_style="compressed")

        with open(route_path, "r") as route_file:
            routes = yaml.load(route_file, Loader=Loader)
            for route, data in routes["routes"].items():
                print(route, data)
                if data["type"] == "simple":
                    self.dump_html(data, data["file"])
                    if "index" in data and data["index"]:
                        self.dump_html(data, "index.html")
                elif data["type"] == "data_yaml":
                    with open(os.path.join(data_dir, data["data"])) as data_file:
                        page_data = yaml.load(data_file, Loader=Loader)
                        data["page_data"] = page_data
                        self.dump_html(data, data["file"])
