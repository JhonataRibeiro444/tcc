/*
 * Comportamentos de interface que nao pertencem a nenhum formulario:
 * por enquanto, o painel de resultados da busca global.
 *
 * O HTMX cuida de buscar os resultados no servidor; o que falta e o
 * comportamento de "menu suspenso": fechar ao clicar fora, fechar com
 * Esc e reabrir quando o campo volta a ter conteudo.
 */

(function () {
  "use strict";

  function iniciar() {
    const busca = document.querySelector(".topo-busca input[name='q']");
    const resultados = document.querySelector("#busca-resultados");

    if (!busca || !resultados || busca.dataset.ligado === "1") {
      return;
    }
    busca.dataset.ligado = "1";

    const fechar = () => {
      resultados.innerHTML = "";
    };

    // Clique fora do campo e do painel fecha os resultados.
    document.addEventListener("click", (evento) => {
      if (!evento.target.closest(".topo-busca")) {
        fechar();
      }
    });

    busca.addEventListener("keydown", (evento) => {
      if (evento.key === "Escape") {
        busca.value = "";
        fechar();
        busca.blur();
      }
    });

    // Ao seguir um resultado o painel some junto com a navegacao, mas
    // se o usuario voltar pelo historico ele nao deve reaparecer.
    window.addEventListener("pageshow", fechar);
  }

  document.addEventListener("DOMContentLoaded", iniciar);
})();
