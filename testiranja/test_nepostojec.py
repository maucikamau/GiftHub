import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://sandbox.playforward.dedyn.io/prijava?next=/")
    page.get_by_role("textbox", name="E-mail*").click()
    page.get_by_role("textbox", name="E-mail*").fill("dz1v4n@gmail.com")
    page.get_by_role("textbox", name="E-mail*").press("Tab")
    page.get_by_role("textbox", name="Lozinka*").fill("sifra1234")
    page.get_by_role("button", name="Prijava", exact=True).click()
    page.get_by_role("link", name="Moje kampanje").click()
    page.get_by_role("link", name="Nova kampanja").click()
    page.get_by_role("textbox", name="Naslov").click()
    page.get_by_role("textbox", name="Naslov").fill("test kampanja")
    page.get_by_role("button", name="Dodajte ručno ili povucite").click()
    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Dodajte ručno ili povucite").click()
    file_chooser = fc_info.value
    file_chooser.set_files("C:\\Users\\Milan\\Desktop\\Progi TESTOVI\\test_slika.jpg")
    page.get_by_role("textbox", name="Opis kampanje").click()
    page.get_by_role("textbox", name="Opis kampanje").fill("test ")
    page.get_by_role("textbox", name="Datum završetka kampanje").fill("2027-07-07")
    page.get_by_role("button", name="Show popup").click()
    page.get_by_text("Biograd na Moru").click()
    page.get_by_role("textbox", name="Naziv igračke").click()
    page.get_by_role("textbox", name="Naziv igračke").fill("abc")
    page.get_by_role("button", name="Dodaj igračku").click()
    page.locator("#v-273").click()
    page.locator("#v-273").fill("abc")
    page.get_by_role("button", name="Dodaj igračku").click()
    page.get_by_text("Ova igračka je već dodana").click()
    page.get_by_role("button", name="Pregledaj i objavi kampanju").click()
    page.get_by_text("Ova igračka je već dodana").click()
    page.get_by_role("button", name="test test test test Udruga").click()
    page.get_by_role("menuitem", name="Odjava").click()
    page.get_by_role("link", name="Idi na prijavu").click()
