from dotenv import load_dotenv
from Database.ORM_Models.criteria_models import CriteriaInDB
import pymupdf

load_dotenv()

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    temp = doc.pages()
    return "\n".join([page.get_text("text") for page in doc]) # type: ignore

def input_formatter(arr: list[CriteriaInDB]) -> str:
    final_output = ""
    for ele in arr:
        temp_str = f"{ele.criteria_name} = {ele.criteria_value}"
        final_output+=temp_str+"\n"
    return final_output
