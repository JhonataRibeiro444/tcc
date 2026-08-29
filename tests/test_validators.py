from app.utils.validators import (
    apenas_digitos,
    formatar_documento,
    formatar_telefone,
    validar_cnpj,
    validar_cpf,
    validar_documento,
)


class TestCPF:
    def test_aceita_cpf_valido_com_e_sem_mascara(self):
        assert validar_cpf("529.982.247-25")
        assert validar_cpf("52998224725")

    def test_rejeita_digito_verificador_errado(self):
        assert not validar_cpf("529.982.247-26")

    def test_rejeita_sequencia_repetida(self):
        assert not validar_cpf("111.111.111-11")

    def test_rejeita_tamanho_invalido(self):
        assert not validar_cpf("1234")
        assert not validar_cpf("")
        assert not validar_cpf(None)


class TestCNPJ:
    def test_aceita_cnpj_valido_com_e_sem_mascara(self):
        assert validar_cnpj("11.222.333/0001-81")
        assert validar_cnpj("11222333000181")

    def test_rejeita_digito_verificador_errado(self):
        assert not validar_cnpj("11.222.333/0001-82")

    def test_rejeita_sequencia_repetida(self):
        assert not validar_cnpj("00000000000000")


class TestValidarDocumento:
    def test_usa_o_algoritmo_conforme_o_tipo_de_pessoa(self):
        assert validar_documento("52998224725", "F")
        assert not validar_documento("52998224725", "J")
        assert validar_documento("11222333000181", "J")
        assert not validar_documento("11222333000181", "F")

    def test_tipo_desconhecido_e_invalido(self):
        assert not validar_documento("52998224725", "X")


class TestFormatacao:
    def test_apenas_digitos_remove_pontuacao(self):
        assert apenas_digitos("529.982.247-25") == "52998224725"

    def test_formata_cpf_e_cnpj(self):
        assert formatar_documento("52998224725") == "529.982.247-25"
        assert formatar_documento("11222333000181") == "11.222.333/0001-81"

    def test_documento_fora_do_padrao_e_devolvido_como_veio(self):
        assert formatar_documento("123") == "123"

    def test_formata_telefone_fixo_e_celular(self):
        assert formatar_telefone("1130001000") == "(11) 3000-1000"
        assert formatar_telefone("11912345678") == "(11) 91234-5678"
