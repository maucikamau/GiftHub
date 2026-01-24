import re
from playwright.sync_api import Page, expect


def test_rubni(page: Page) -> None:
    page.goto("https://sandbox.playforward.dedyn.io/prijava?next=/")
    page.get_by_role("textbox", name="E-mail*").click()
    page.get_by_role("textbox", name="E-mail*").fill("dz1v4n@gmail.com")
    page.get_by_role("textbox", name="E-mail*").press("Tab")
    page.get_by_role("textbox", name="Lozinka*").fill("sifra1234")
    page.get_by_role("button", name="Prijava", exact=True).click()
    page.get_by_role("link", name="Razgovori").click()
    page.get_by_role("button", name="test11 test11 test").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="Plati").click()
    page1 = page1_info.value
    page1.get_by_role("textbox", name="Email").click()
    with page.expect_popup() as page2_info:
        page.get_by_role("button", name="Plati").click()
    page2 = page2_info.value
    page.get_by_role("button", name="test test test test Udruga").click()
    page.get_by_role("menuitem", name="Odjava").click()
    page.get_by_role("link", name="Idi na prijavu").click()
