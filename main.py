from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import redis
import hashlib

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"

redis_client = redis.StrictRedis(host="redis", port=6379, db=0, password="default", decode_responses=True)

with open("documents.json", encoding="utf-8") as f:
    knowledge_base = json.load(f)

STANDARD_RESPONSES = {
    "quero marcar uma consulta": {
        "reply": "Claro! Podemos marcar uma consulta. Informe a especialidade desejada.",
        "app_rota": "agendamento"
    },
    "meus dentes estão sensíveis": {
        "reply": (
            "Sensibilidade dentária é comum. Recomendo marcar uma consulta para avaliarmos.<br>"
            '👉 <a href="https://loja.odontoprev.com.br/carrinho/bem_estar_desconto/titular" target="_blank">'
            "Veja nossos planos com desconto</a>"
        )
    },
    "qual o horário disponível?": {
        "reply": "Podemos consultar os horários disponíveis após escolher a clínica e especialidade."
    }
}

agendamento_keywords = ["consulta", "agendar", "agendamento", "marcar", "horário", "agenda"]
alerta_keywords = ["sangra", "sensível", "doces", "café", "não escovo", "planos", "fio dental", "mobilidade"]

def search_context(query, top_k=2):
    query_words = set(query.lower().split())
    return sorted(
        knowledge_base,
        key=lambda doc: len(query_words & set(doc.lower().split())),
        reverse=True
    )[:top_k]

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Mensagem ausente"}), 400

    normalized_input = user_input.lower()

    # 1. Resposta padrão direta
    if normalized_input in STANDARD_RESPONSES:
        return jsonify(STANDARD_RESPONSES[normalized_input])

    # 2. Detecção rápida para agendamento
    if any(keyword in normalized_input for keyword in agendamento_keywords):
        return jsonify({
            "reply": "Certo! Vamos iniciar o processo de agendamento. Selecione a clínica e especialidade.",
            "app_rota": "agendamento"
        })

    # 3. Verifica se já está no cache
    key = f"rag_cache:{hashlib.sha256(normalized_input.encode()).hexdigest()}"
    cached_reply = redis_client.get(key)
    if cached_reply:
        return jsonify(json.loads(cached_reply))

    # 4. Monta contexto e prompt
    context = " ".join(search_context(user_input))[:1500]
    prompt = (
        "Você é um assistente de saúde bucal. Responda com base no contexto a seguir.\n"
        f"Contexto:\n{context}\n\n"
        f"Pergunta: {user_input}\nResposta:"
    )

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()
        data = response.json()
        reply = data.get("response", "").strip()
        reply_lower = reply.lower()

        result = {"reply": reply}

        if any(p in reply_lower for p in agendamento_keywords):
            result["app_rota"] = "agendamento"

        if any(p in reply_lower for p in alerta_keywords):
            result["reply"] += (
                '<br><br>👉 <a href="https://loja.odontoprev.com.br/carrinho/bem_estar_desconto/titular" '
                'target="_blank">Conheça nossos planos com desconto</a>'
            )

        redis_client.set(key, json.dumps(result), ex=3600)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Falha ao gerar resposta", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
