import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils.cfg import (
    extract_post_meta,
    get_configs
)


raw_configs = get_configs()


def generate_webpage():
    """Generate HTML content for the webpage using Jinja2 templates."""
    configs = extract_post_meta(raw_configs)
    templates_path = os.path.join(os.path.dirname(__file__), 'templates')
    
    env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template("index.html")
    return template.render(**configs)
