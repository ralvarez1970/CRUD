## Coding Dojo - Python Bootcamp Jan 2025
## Roberto Alvarez, 2025

from flask import render_template, request, redirect, session, flash
from flask_app.utils.decoradores import login_required
from flask_app.utils.openai_helper import call_openai_with_tool
from datetime import date
from flask import Blueprint

extracoes = Blueprint('extracoes', __name__)

@extracoes.route('/extracoes')
@login_required
def executar_extracoes():
    return render_template("/extracoes/extracoes.html", nome=session['nome'])


@extracoes.route('/extrair_fatos', methods=['POST'])
@login_required
def extrair():
    texto = request.form['texto']

    # 🧠 Tool/function schema for fact extraction
    fact_extraction_schema = [
        {
            "type": "function",
            "function": {
                "name": "extract_facts",
                "description": "Extract factual statements from a news article",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "facts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "statement": {"type": "string"},
                                    "source": {"type": "string"},
                                    "confidence": {
                                        "type": "number",
                                        "minimum": 0,
                                        "maximum": 1
                                    },
                                    "data_elements": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "description": "The type of data (e.g., date, number, percentage, statistic, currency)"
                                                },
                                                "value": {
                                                    "type": "string",
                                                    "description": "The extracted value as a string"
                                                },
                                                "context": {
                                                    "type": "string",
                                                    "description": "Brief context around this data point"
                                                }
                                            },
                                            "required": ["type", "value"]
                                        }
                                    }
                                },
                                "required": ["statement"]
                            }
                        }
                    },
                    "required": ["facts"]
                }
            }
        }
    ]

    # Prompt construction
    prompt = f"""
You are a fact extraction engine. Use the tool 'extract_facts' to extract all factual claims from the text below.

For each fact, return:
- A short atomic statement
- The source (if mentioned, otherwise use an empty string)
- A confidence score (between 0.0 and 1.0)
- A list of key data elements related to that fact, if any

Each data element should include:
- type: the kind of data (e.g., date, number, percentage, currency, statistic)
- value: the actual value as it appears in the text
- context: a short phrase describing what this value refers to

Text:
\"\"\"
{texto}
\"\"\"
"""

    # Call the centralized OpenAI helper
    result = call_openai_with_tool(prompt, fact_extraction_schema, "extract_facts")

    if "error" in result:
        flash("Erro ao processar os dados do modelo.")
        session['fatos_extraidos'] = []
        return redirect("/mostrar_extracao")

    session['fatos_extraidos'] = result["result"].get("facts", [])
    return redirect("/mostrar_extracao")


@extracoes.route('/mostrar_extracao')
@login_required
def mostrar_extracao():
    return render_template(
        "/extracoes/extracoes.html",
        nome=session['nome'],
        fatos_extraidos=session.get('fatos_extraidos', [])
    )
