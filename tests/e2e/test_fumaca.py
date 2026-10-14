import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.e2e


def test_tela_de_login_abre(page):
    page.goto("/auth/login")
    expect(page.get_by_role("button", name="Entrar")).to_be_visible()
