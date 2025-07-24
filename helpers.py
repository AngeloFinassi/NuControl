#import requests
from flask import redirect, render_template, session
from functools import wraps
import pandas as pd

def apology(message, protocol):
    #render message as as apology to user
    def escape(s):
        #Escape special characters.
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s
    
    return render_template("apology.html", error_message=message, protocol=protocol)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def read_file(file, filename, return_filetype=False):
    import os

    #Detect if the path is a string
    file_was_path = False
    if isinstance(file, str) and os.path.exists(file):
        file = open(file, "rb")
        file_was_path = True

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith(".tsv"):
            df = pd.read_csv(file, sep="\t")
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file, engine="openpyxl")
        elif filename.endswith(".xls"):
            df = pd.read_excel(file, engine="xlrd")
        elif filename.endswith(".json"):
            df = pd.read_json(file)
        else:
            return (None, None) if return_filetype else None

        df.columns = [
        col.strip()
           .lower()
           .replace(" ", "_")
           .replace("ç", "c")
           .replace("ã", "a")
           .replace("á", "a")
           .replace("â", "a")
           .replace("é", "e")
           .replace("ê", "e")
           .replace("í", "i")
           .replace("ó", "o")
           .replace("õ", "o")
           .replace("ô", "o")
           .replace("ú", "u")
           .replace("ü", "u")
        for col in df.columns
    ]

    except Exception as e:
        print(f"[read_file] Error to read '{filename}': {e}")
        return (None, None) if return_filetype else None

    finally:
        if file_was_path and file:
            file.close()
    return df



def categorize_dataframe(df):
    category = {
    'alimentacao': [
        'mercado', 'supermercado', 'padaria', 'restaurante', 'lanchonete', 'ifood',
        'bar', 'cafeteria', 'comida', 'bebida', 'açougue', 'sacolão', 'hortifruti',
        'pizza', 'burguer', 'fast food', 'mc donald', 'habib', 'kfc', 'bob’s'
    ],

    'moradia': [
        'aluguel', 'condominio', 'energia', 'luz', 'água', 'telefone fixo',
        'internet', 'gás', 'vivo fibra', 'claro net', 'tim live', 'copasa', 'cemig',
        'iptu', 'reparos', 'manutenção'
    ],

    'transporte': [
        'uber', '99', 'ônibus', 'metrô', 'passagem', 'bilhete único',
        'combustível', 'gasolina', 'etanol', 'estacionamento', 'pedágio',
        'carro', 'manutenção carro', 'oficina', 'cnh', 'detran'
    ],

    'lazer': [
        'cinema', 'netflix', 'spotify', 'show', 'eventos', 'viagem',
        'airbnb', 'booking', 'ingresso', 'jogos', 'steam', 'game', 'apple music',
        'parque', 'bares', 'festas'
    ],

    'educacao': [
        'faculdade', 'curso', 'apostila', 'ensino', 'mensalidade',
        'matrícula', 'material escolar', 'plataforma', 'udemy', 'alura',
        'ebook', 'curso online', 'prova', 'aula'
    ],

    'saude': [
        'farmácia', 'remédio', 'consulta', 'hospital', 'plano de saúde',
        'exame', 'laboratório', 'dentista', 'oftalmo', 'psicólogo', 'medicamento',
        'vacina', 'posto de saúde'
    ],

    'servicos': [
        'assinatura', 'plano', 'serviço', 'manutenção', 'consultoria', 'advogado',
        'engenheiro', 'freela', 'corte cabelo', 'barbeiro', 'salão', 'estética',
        'pet shop', 'lava jato', 'limpeza', 'Compra no débito', 'Compra no crédito'
    ],

    'vestuario': [
        'roupa', 'calçado', 'tênis', 'sandália', 'camisa', 'blusa', 'loja de roupa',
        'c&a', 'renner', 'riachuelo', 'zara', 'sapato', 'acessório', 'óculos', 'relógio'
    ],

    'tecnologia': [
        'celular', 'notebook', 'eletrônico', 'informática', 'fone', 'teclado',
        'mouse', 'monitor', 'software', 'aplicativo', 'hardware', 'pc', 'gadget'
    ],

    'salario_entrada': [
        'salario', 'pagamento', 'transferencia recebida', 'pix recebido',
        'depósito', 'rendimento', 'remuneração', 'pro labore', 'reembolso'
    ],

    'investimentos': [
        'tesouro', 'cdb', 'fundo', 'ações', 'renda fixa', 'renda variável',
        'cripto', 'bitcoin', 'poupança', 'investimento', 'broker', 'corretora'
    ],

    'impostos_taxas': [
        'imposto', 'irpf', 'taxa', 'encargo', 'darf', 'tarifa',
        'juros', 'anuidade', 'cartão de crédito', 'fatura'
    ],

    'outros': [
        'diverso', 'outro', 'não identificado', 'desconhecido'
    ]
}
    #Serch for a category based on some 'keys' words.
    def find_category(desc: str) -> str:
        desc = str(desc).lower()
        for cat, keywords in category.items():
            if any(k in desc for k in keywords):
                return cat
        return "outros"

    #garante que a coluna esteja numérica
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)

    df["categoria"] = df["descricao"].apply(find_category)

    category_totals = (
        df.assign(valor_abs=df["valor"].abs()).groupby("categoria")["valor_abs"].sum().round(2).sort_values(ascending=False).to_dict()
    )
    return df, category_totals
