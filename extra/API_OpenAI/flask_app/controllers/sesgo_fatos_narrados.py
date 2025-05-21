## Coding Dojo - Python Bootcamp Jan 2025
## Roberto Alvarez, 2025

from flask import render_template, request, redirect, session, flash
from functools import wraps
from flask_app.models.usuario import Usuario
from flask_app.utils.decoradores import login_required
import openai
import os
import pprint
import json  # ✅ Needed for parsing arguments
from flask import Blueprint

sesgo_fatos = Blueprint('sesgo_fatos', __name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI"))

@sesgo_fatos.route('/sesgo')
@login_required
def sesgo_index():
    return render_template("/sesgo/sesgo.html", nome=session['nome'])


@sesgo_fatos.route('/avaliar_sesgo', methods=['POST'])
@login_required
def avaliar_sesgo():
    texto = request.form['texto']

    multi_axis_bias_schema = [
        {
            "type": "function",
            "function": {
                "name": "score_bias",
                "description": "Scores a text across multiple ideological axes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "economic": {
                            "type": "object",
                            "properties": {
                                "score": { "type": "number" },
                                "label": { "type": "string" },
                                "confidence": { "type": "number" },
                                "features": {
                                    "type": "array",
                                    "items": { "type": "string" }
                                }
                            },
                            "required": ["score", "label", "confidence", "features"]
                        },
                        "cultural": {
                            "type": "object",
                            "properties": {
                                "score": { "type": "number" },
                                "label": { "type": "string" },
                                "confidence": { "type": "number" },
                                "features": {
                                    "type": "array",
                                    "items": { "type": "string" }
                                }
                            },
                            "required": ["score", "label", "confidence", "features"]
                        },
                        "institutional": {
                            "type": "object",
                            "properties": {
                                "score": { "type": "number" },
                                "label": { "type": "string" },
                                "confidence": { "type": "number" },
                                "features": {
                                    "type": "array",
                                    "items": { "type": "string" }
                                }
                            },
                            "required": ["score", "label", "confidence", "features"]
                        },
                        "summary": {
                            "type": "string"
                        }
                    },
                    "required": ["economic", "cultural", "institutional", "summary"]
                }
            }
        }
    ]

    prompt = f"""
    You are a media analyst evaluating ideological bias along three axes:
    
    - Economic: left (-1) to right (+1)
    - Cultural: progressive (-1) to conservative (+1)
    - Institutional: anti-elite (-1) to pro-establishment (+1)

    Use the function tool 'score_bias' to return, for each axis:
    - score (float from -1 to 1)
    - label (e.g., 'left', 'center-right', etc.)
    - confidence (0 to 1)
    - list of key words or expressions indicating that axis' bias

    Also return a summary explanation combining all observations.

    Text:
    \"\"\"
    {texto}
    \"\"\"
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        tools=multi_axis_bias_schema,
        tool_choice={"type": "function", "function": {"name": "score_bias"}}
    )

    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        flash("O modelo não retornou uma chamada de função. Tente novamente com outro texto.")
        session['bias_result'] = {}
        return redirect("/mostrar_sesgo")

    try:
        bias_json_string = tool_calls[0].function.arguments
        bias_data = json.loads(bias_json_string)
        session['bias_result'] = bias_data
    except Exception as e:
        print("Erro ao interpretar o resultado de viés:", e)
        flash("Erro ao processar os dados do modelo.")
        session['bias_result'] = {}

    return redirect("/mostrar_sesgo")


@sesgo_fatos.route('/mostrar_sesgo')
@login_required
def mostrar_sesgo():
    return render_template("/sesgo/sesgo.html", nome=session['nome'], bias_result=session.get('bias_result', {}))
