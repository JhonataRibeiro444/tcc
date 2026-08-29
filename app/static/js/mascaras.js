/*
 * Camada de apoio no navegador:
 *  - mascara de CPF/CNPJ, telefone e CEP conforme o usuario digita;
 *  - validacao do documento no cliente (o servidor revalida sempre);
 *  - preenchimento automatico do endereco a partir do CEP (API ViaCEP).
 *
 * A validacao daqui e apenas conveniencia de interface. A regra que vale
 * continua sendo a do servidor, em app/utils/validators.py.
 */

(function () {
  "use strict";

  const apenasDigitos = (valor) => (valor || "").replace(/\D/g, "");

  /* ----------------------------------------------------------- mascaras */

  function mascararCpf(valor) {
    const d = apenasDigitos(valor).slice(0, 11);
    return d
      .replace(/^(\d{3})(\d)/, "$1.$2")
      .replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3")
      .replace(/\.(\d{3})(\d{1,2})$/, ".$1-$2");
  }

  function mascararCnpj(valor) {
    const d = apenasDigitos(valor).slice(0, 14);
    return d
      .replace(/^(\d{2})(\d)/, "$1.$2")
      .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
      .replace(/\.(\d{3})(\d)/, ".$1/$2")
      .replace(/(\d{4})(\d{1,2})$/, "$1-$2");
  }

  function mascararTelefone(valor) {
    const d = apenasDigitos(valor).slice(0, 11);
    if (d.length <= 10) {
      return d.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{4})(\d{1,4})$/, "$1-$2");
    }
    return d.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{5})(\d{1,4})$/, "$1-$2");
  }

  function mascararCep(valor) {
    return apenasDigitos(valor).slice(0, 8).replace(/^(\d{5})(\d)/, "$1-$2");
  }

  /* --------------------------------------------- validacao de documento */

  function digitoVerificador(digitos, pesoInicial) {
    let soma = 0;
    let peso = pesoInicial;

    for (const caractere of digitos) {
      soma += Number(caractere) * peso;
      peso -= 1;
      if (peso < 2) {
        peso = 9;
      }
    }

    const resto = soma % 11;
    return resto < 2 ? 0 : 11 - resto;
  }

  function validarCpf(valor) {
    const d = apenasDigitos(valor);
    if (d.length !== 11 || /^(\d)\1+$/.test(d)) {
      return false;
    }

    let soma = 0;
    for (let i = 0; i < 9; i += 1) soma += Number(d[i]) * (10 - i);
    let resto = soma % 11;
    const primeiro = resto < 2 ? 0 : 11 - resto;

    soma = 0;
    for (let i = 0; i < 10; i += 1) soma += Number(d[i]) * (11 - i);
    resto = soma % 11;
    const segundo = resto < 2 ? 0 : 11 - resto;

    return d.slice(9) === `${primeiro}${segundo}`;
  }

  function validarCnpj(valor) {
    const d = apenasDigitos(valor);
    if (d.length !== 14 || /^(\d)\1+$/.test(d)) {
      return false;
    }

    const primeiro = digitoVerificador(d.slice(0, 12), 5);
    const segundo = digitoVerificador(d.slice(0, 13), 6);

    return d.slice(12) === `${primeiro}${segundo}`;
  }

  /* ------------------------------------------------------------ ligacao */

  function aplicarMascara(campo, formatador) {
    if (!campo) return;
    campo.value = formatador(campo.value);
    campo.addEventListener("input", () => {
      campo.value = formatador(campo.value);
    });
  }

  function configurarDocumento() {
    const tipo = document.querySelector("#tipo_pessoa");
    const documento = document.querySelector("#documento");
    if (!tipo || !documento) return;

    const formatar = () =>
      tipo.value === "J" ? mascararCnpj(documento.value) : mascararCpf(documento.value);

    const avaliar = () => {
      const numeros = apenasDigitos(documento.value);
      const esperado = tipo.value === "J" ? 14 : 11;

      documento.classList.remove("is-valid", "is-invalid");
      if (numeros.length === 0) return;

      const valido = tipo.value === "J" ? validarCnpj(numeros) : validarCpf(numeros);
      if (numeros.length === esperado) {
        documento.classList.add(valido ? "is-valid" : "is-invalid");
      }
    };

    documento.value = formatar();
    documento.addEventListener("input", () => {
      documento.value = formatar();
      avaliar();
    });
    tipo.addEventListener("change", () => {
      documento.value = formatar();
      avaliar();
    });
  }

  function configurarCep() {
    const cep = document.querySelector("#cep");
    if (!cep) return;

    cep.addEventListener("blur", async () => {
      const numeros = apenasDigitos(cep.value);
      if (numeros.length !== 8) return;

      try {
        const resposta = await fetch(`https://viacep.com.br/ws/${numeros}/json/`);
        if (!resposta.ok) return;

        const dados = await resposta.json();
        if (dados.erro) return;

        const preencher = (seletor, valor) => {
          const campo = document.querySelector(seletor);
          if (campo && !campo.value) campo.value = valor || "";
        };

        preencher("#logradouro", dados.logradouro);
        preencher("#bairro", dados.bairro);
        preencher("#cidade", dados.localidade);

        const uf = document.querySelector("#uf");
        if (uf && !uf.value) uf.value = dados.uf || "";

        const numero = document.querySelector("#numero");
        if (numero && !numero.value) numero.focus();
      } catch (erro) {
        // Sem conexao com o ViaCEP o usuario simplesmente digita o endereco.
        console.warn("Nao foi possivel consultar o CEP:", erro);
      }
    });
  }

  function iniciar() {
    configurarDocumento();
    configurarCep();
    aplicarMascara(document.querySelector("#telefone"), mascararTelefone);
    aplicarMascara(document.querySelector("#cep"), mascararCep);
  }

  document.addEventListener("DOMContentLoaded", iniciar);

  // O HTMX troca pedacos da pagina sem recarregar; e preciso religar os
  // comportamentos no conteudo que acabou de chegar.
  document.body.addEventListener("htmx:afterSwap", iniciar);
})();
