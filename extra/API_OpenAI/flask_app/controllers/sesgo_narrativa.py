## Coding Dojo - Python Bootcamp Jan 2025
## Roberto Alvarez, 2025

from flask import render_template, request, redirect, session, flash
from functools import wraps
from flask_app.models.usuario import Usuario
from flask_app.utils.decoradores import login_required
import openai
import os
import json
from flask import Blueprint

sesgo_narrativa = Blueprint('sesgo_narrativa', __name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI"))

@sesgo_narrativa.route('/sesgo_narrativa')
@login_required
def sesgo_narrativa_index():
    return render_template("/sesgo/sesgo_narrativa.html", nome=session['nome'])


@sesgo_narrativa.route('/avaliar_sesgo_narrativa', methods=['POST'])
@login_required
def avaliar_sesgo_narrativa():
    texto = request.form['texto']

    narrative_bias_schema = [
        {
            "type": "function",
            "function": {
                "name": "score_bias",
                "description": "Evaluates the narrative bias of the author across multiple ideological axes.",
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
    You are a media bias analyst tasked with evaluating the ideological **narrative bias** of a text. You are not evaluating the bias of the events or people being described, but rather the bias of the **author or narrator** based on how the content is presented.

    Your goal is to determine **how the author frames**, critiques, endorses, or reacts to the events, quotes, and policies mentioned.

    Focus on the following aspects:

    1. **Tone and Language**
        - Detect emotionally charged, sarcastic, ironic, or dismissive tone.
        - Look for adjectives or adverbs that signal approval or disapproval.

    2. **Framing and Commentary**
        - Note when the author praises, criticizes, or questions people or policies.
        - Distinguish between quoted content and how the author introduces or interprets the quote.

    3. **Selectivity and Omission**
        - Evaluate whether the author presents a one-sided perspective.
        - Identify ideological alignment based on what is emphasized or omitted.

    4. **Attribution of Intent**
        - Flag phrases that assign motives or moral judgment to political actors.

    Return a bias evaluation across **three ideological axes**, based on the author's narrative stance:

    - **Economic** (left ↔ right)
    - **Cultural** (progressive ↔ conservative)
    - **Institutional** (anti-elite ↔ pro-establishment)

    For each axis, return:
    - `score`: a float from -1 (strongly left/progressive/anti-elite) to 1 (strongly right/conservative/pro-establishment)
    - `label`: a qualitative label (e.g., "left", "center-right")
    - `confidence`: between 0 and 1
    - `features`: a list of key phrases or expressions that indicate bias

    Also return a `summary` that explains the author's overall **narrative position**, explicitly clarifying whether the author **supports or critiques** the ideas and actions described.

    You must **distinguish between the bias of the narrator and the bias of the people they quote or describe**.

    Text:
    \"\"\"
    {texto}
    \"\"\"
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        tools=narrative_bias_schema,
        tool_choice={"type": "function", "function": {"name": "score_bias"}}
    )

    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        flash("O modelo não retornou uma chamada de função. Tente novamente com outro texto.")
        session['bias_result'] = {}
        return redirect("/mostrar_sesgo_narrativa")

    try:
        bias_json_string = tool_calls[0].function.arguments
        bias_data = json.loads(bias_json_string)
        session['bias_result'] = bias_data
    except Exception as e:
        print("Erro ao interpretar o resultado de viés narrativo:", e)
        flash("Erro ao processar os dados do modelo.")
        session['bias_result'] = {}

    return redirect("/mostrar_sesgo_narrativa")


@sesgo_narrativa.route('/mostrar_sesgo_narrativa')
@login_required
def mostrar_sesgo_narrativa():
    return render_template("/sesgo/sesgo_narrativa.html", nome=session['nome'], bias_result=session.get('bias_result', {}))
