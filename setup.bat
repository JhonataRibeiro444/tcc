@echo off
rem ===================================================================
rem  Configuracao do ambiente de desenvolvimento do CRM (Windows)
rem
rem  O que este script faz:
rem   1. localiza o Python instalado;
rem   2. cria o ambiente virtual em .\venv (se ainda nao existir);
rem   3. instala as dependencias do requirements.txt;
rem   4. cria o arquivo .env a partir do .env.example;
rem   5. cria as tabelas do banco de dados;
rem   6. opcionalmente cadastra o primeiro usuario de acesso.
rem
rem  Basta dar dois cliques neste arquivo ou executar: setup.bat
rem ===================================================================

setlocal
cd /d "%~dp0"

echo.
echo ============================================
echo   Configurando o ambiente do CRM
echo ============================================
echo.

rem ---------- 1. Localizar o Python -----------------------------------
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"

if not defined PY (
    echo [ERRO] Python nao foi encontrado no PATH.
    echo.
    echo Instale a partir de https://www.python.org/downloads/
    echo IMPORTANTE: marque a opcao "Add python.exe to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

echo [1/5] Python encontrado:
%PY% --version
echo.

rem ---------- 2. Criar o ambiente virtual -----------------------------
if exist "venv\Scripts\activate.bat" (
    echo [2/5] Ambiente virtual ja existe em .\venv - reutilizando.
) else (
    echo [2/5] Criando o ambiente virtual em .\venv ...
    %PY% -m venv venv
    if errorlevel 1 goto :erro
)
echo.

call "venv\Scripts\activate.bat"
if errorlevel 1 goto :erro

rem ---------- 3. Instalar as dependencias -----------------------------
echo [3/5] Instalando as dependencias ...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt
if errorlevel 1 goto :erro
echo.

rem ---------- 4. Arquivo de variaveis de ambiente ---------------------
if exist ".env" (
    echo [4/5] Arquivo .env ja existe - mantido como esta.
) else (
    copy ".env.example" ".env" >nul
    echo [4/5] Arquivo .env criado a partir do .env.example.
    echo       Lembre-se de trocar a SECRET_KEY antes de publicar.
)
echo.

rem ---------- 5. Banco de dados ---------------------------------------
set FLASK_APP=run.py
echo [5/5] Criando as tabelas do banco de dados ...
flask init-db
if errorlevel 1 goto :erro
echo.

rem ---------- Usuario inicial -----------------------------------------
echo ============================================
echo   Ambiente pronto.
echo ============================================
echo.

set "CRIAR="
set /p "CRIAR=Deseja cadastrar um usuario de acesso agora? (s/n) "
if /i not "%CRIAR%"=="s" goto :fim

set "UNOME="
set "UEMAIL="
set "USENHA="
set /p "UNOME=Nome completo: "
set /p "UEMAIL=E-mail: "
set /p "USENHA=Senha: "
flask criar-usuario "%UNOME%" "%UEMAIL%" "%USENHA%"

:fim
echo.
echo Para trabalhar no projeto, abra o terminal nesta pasta e execute:
echo.
echo     venv\Scripts\activate
echo     python run.py
echo.
echo A aplicacao ficara em http://127.0.0.1:5000
echo.
echo Para rodar os testes:  python -m pytest
echo.
pause
exit /b 0

:erro
echo.
echo [ERRO] A configuracao foi interrompida. Veja a mensagem acima.
echo.
pause
exit /b 1
