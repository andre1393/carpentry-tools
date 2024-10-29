from datetime import datetime
from tools.document_generator_workflow import DocumentGeneratorWorkflow
from tools.utils import make_string_path_compatible
from tools.document_inputs.google_drive_input import GoogleDriveInput
from tools.document_inputs.local_file_input import LocalFileInput
from tools.document_outputs.google_drive_output import GoogleDriveOutput
from tools.document_outputs.local_file_output import LocalFileOutput


async def generate_quote(params):
    document_input_instance = _get_document_input_instance(params)
    document_output_instance = _get_document_output_instance(params)

    quote_params = params.quote_params

    subtotal = 0
    for item in quote_params.items:
        item_subtotal = item.quantity * item.unit_price
        subtotal += item_subtotal
        item.total = "{:.2f}".format(item_subtotal)
        item.unit_price = "{:.2f}".format(item.unit_price)

    quote_params.in_cash_total = "{:.2f}".format(round(subtotal * (1 - quote_params.in_cash_discount_rate), 0))
    quote_params.total = "{:.2f}".format(subtotal)

    quote_includes = []
    if quote_params.include_material:
        quote_includes.append("material")
    if quote_params.include_shipping:
        quote_includes.append("frete")

    quote_params.quote_includes = (
        " e " + quote_includes[0] if len(quote_includes) == 1
        else f", {' e '.join(quote_includes)}"
    )

    workflow = DocumentGeneratorWorkflow(
        document_input_instance,
        document_output_instance,
        quote_params
    )

    result = workflow.generate()
    return result


def _get_document_input_instance(params):
    if params.doc_input.type == "google_drive":
        return GoogleDriveInput(params.doc_input.params.doc_id)
    elif params.doc_input.type == "local":
        return LocalFileInput(params.doc_input.params.base_dir, params.doc_output.params.file_name)


def _get_document_output_instance(params):
    output_file = (
        f"orcamento_{datetime.now().strftime('%d_%m_%Y')}_"
        f"{make_string_path_compatible(params.quote_params.client_name)}.pdf"
    )
    if params.doc_output.type == "google_drive":
        return GoogleDriveOutput(
            params.doc_output.params.tmp_dir,
            params.doc_output.params.file_name or output_file,
            params.doc_output.params.parent_dir_id
        )
    elif params.doc_output.type == "local":
        return LocalFileOutput(params.doc_output.params.base_dir, params.doc_output.params.file_name or output_file)
