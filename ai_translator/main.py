import sys
import os
import uvicorn

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator
from fastapi import FastAPI

app = FastAPI()

pdf_file_path = None
file_format = None
api_key = None


def init():
    config_loader = ConfigLoader("config.yaml")
    config = config_loader.load_config()
    global api_key
    api_key = config['OpenAIModel']['openai_api_key']
    global pdf_file_path
    pdf_file_path = config['common']['book']


init()


@app.get("/translator")
def translator_pdf(source_doc_path: str, model_type: str, target_language: str, file_format: str, model: str):
    llm_model = None
    if model_type is not None and model_type == "OpenAIModel":
        llm_model = OpenAIModel(api_key=api_key, model=model)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(llm_model)
    translator.translate_pdf(source_doc_path, file_format, target_language=target_language)

    return {"successful": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # 默认加载config.yaml配置
