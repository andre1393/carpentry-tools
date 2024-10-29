import unicodedata
from weasyprint import HTML


def html_to_pdf(content, file_name) -> None:
    HTML(string=content).write_pdf(file_name)


def make_string_path_compatible(value: str) -> str:
    return unicodedata\
            .normalize("NFKD", value)\
            .encode("ASCII", "ignore")\
            .decode("ascii")\
            .replace("-", "_")\
            .replace(" ", "_")\
            .lower()
