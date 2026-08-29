#!/usr/bin/env bash
# ===================================================================
#  Configuracao do ambiente de desenvolvimento do CRM (Linux / macOS)
#  Uso:  bash setup.sh
# ===================================================================

set -e
cd "$(dirname "$0")"

echo
echo "============================================"
echo "  Configurando o ambiente do CRM"
echo "============================================"
echo

if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    PY=python
else
    echo "[ERRO] Python nao encontrado. Instale o Python 3.10 ou superior."
    exit 1
fi

echo "[1/5] Python encontrado: $($PY --version)"
echo

if [ -d "venv" ]; then
    echo "[2/5] Ambiente virtual ja existe em ./venv - reutilizando."
else
    echo "[2/5] Criando o ambiente virtual em ./venv ..."
    $PY -m venv venv
fi
echo

# shellcheck disable=SC1091
source venv/bin/activate

echo "[3/5] Instalando as dependencias ..."
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt
echo

if [ -f ".env" ]; then
    echo "[4/5] Arquivo .env ja existe - mantido como esta."
else
    cp .env.example .env
    echo "[4/5] Arquivo .env criado a partir do .env.example."
fi
echo

export FLASK_APP=run.py
echo "[5/5] Criando as tabelas do banco de dados ..."
flask init-db
echo

echo "============================================"
echo "  Ambiente pronto."
echo "============================================"
echo
read -r -p "Deseja cadastrar um usuario de acesso agora? (s/n) " CRIAR

if [ "$CRIAR" = "s" ] || [ "$CRIAR" = "S" ]; then
    read -r -p "Nome completo: " UNOME
    read -r -p "E-mail: " UEMAIL
    read -r -s -p "Senha: " USENHA
    echo
    flask criar-usuario "$UNOME" "$UEMAIL" "$USENHA"
fi

echo
echo "Para trabalhar no projeto:"
echo
echo "    source venv/bin/activate"
echo "    python run.py"
echo
echo "A aplicacao ficara em http://127.0.0.1:5000"
echo "Para rodar os testes:  python -m pytest"
echo
