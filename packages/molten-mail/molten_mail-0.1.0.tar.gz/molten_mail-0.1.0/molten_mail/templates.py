from inspect import Parameter
from typing import Any

try:
    import jinja2
except ImportError:  # pragma: no cover
    raise ImportError("'jinja2' missing. Run 'pip install jinja2'.")


class MailTemplates:
    """Renders jinja2 templates for use in html email bodies.

    Unlike the molten.contrib.templates this object does not return a
    molten Response object, but a rendered string of the provided template.
    """

    __slots__ = ["environment"]

    def __init__(self, path: str) -> None:
        self.environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path))

    def render(self, template_name: str, **context: Any) -> str:
        """Find a template and render it.

        Parameters:
          template_name: The name of the template to render.
          **context: Bindings passed to the template.
        """
        template = self.environment.get_template(template_name)
        rendered_template = template.render(**context)
        return rendered_template


class MailTemplatesComponent:
    """A component that builds a jinja2 template renderer for email templates.

    Parameters:
      path: The path to a folder containing your templates.
    """

    __slots__ = ["path"]

    is_cacheable = True
    is_singleton = True

    def __init__(self, path: str) -> None:
        self.path = path

    def can_handle_parameter(self, parameter: Parameter) -> bool:
        return parameter.annotation is MailTemplates

    def resolve(self) -> MailTemplates:
        return MailTemplates(self.path)
