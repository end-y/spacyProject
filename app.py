from spacy import load
from flask import Flask, request, jsonify
from urllib.parse import unquote
nlp = load("en_core_web_sm")
app = Flask(__name__)


@app.route('/')
def getIndex():
    return jsonify({"Message": "Welcome"})


@app.route("/text/<text>")
def getText(text):
    if not text.isspace():
        text = unquote(text)
        doc = nlp(text)
        result_dict = {}
        for token in doc:
            if token.pos_ not in result_dict:
                result_dict[token.pos_] = [token.text.lower()]
            else:
                result_dict[token.pos_].append(token.text.lower())
        for d in result_dict:
            result_dict[d] = list(set(result_dict[d]))

        result_dict[
            "CITE"] = "Honnibal, M., Montani, I., Van Landeghem, S., & Boyd, A. (2020). spaCy: Industrial-strength " \
                      "Natural Language Processing in Python. https://doi.org/10.5281/zenodo.1212303 "

        return jsonify({'data': result_dict}), 200
    else:
        return jsonify({'data': "error"}), 500

@app.route("/root/<word>")
def getRoot(word):
    if not word.isspace():
        doc = nlp(word)
        return jsonify({"data": doc[0].lemma_}), 200


if __name__ == '__main__':
    app.run(debug=False)