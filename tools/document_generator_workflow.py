from jinja2 import Template


class DocumentGeneratorWorkflow:

    def __init__(self, document_input, document_output, variables, **kwargs):
        self.document_input = document_input
        self.document_output = document_output
        self.variables = variables
        self.kwargs = kwargs

    def generate(self):
        document_template = self.document_input.read()
        document_rendered = self._render_document(document_template, self.variables)
        return self.document_output.save(document_rendered, **self.kwargs)

    @staticmethod
    def _render_document(document_template, variables):
        template = Template(document_template)
        return template.render(variables)

