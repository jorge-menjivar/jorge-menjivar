from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))


def render_template(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)


def create_banner(action: str, timestamp: str) -> None:
    svg_str = render_template(
        "quantum-banner.svg.jinja",
        action=action,
        architecture="8→8→7→4",
        entanglement="HIGH",
        consciousness="ONLINE",
        timestamp=timestamp,
    )

    with open("assets/quantum-banner.svg", "w") as file:
        file.write(svg_str)
