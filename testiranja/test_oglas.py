import re
from playwright.sync_api import Page, expect


def test_oglas(page: Page) -> None:
    page.goto("https://sandbox.playforward.dedyn.io/prijava?next=/")
    page.get_by_role("textbox", name="E-mail*").click()
    page.get_by_role("textbox", name="E-mail*").fill("test@test.test")
    page.get_by_role("textbox", name="E-mail*").press("Tab")
    page.get_by_role("textbox", name="Lozinka*").fill("sifra1234")
    page.get_by_role("button", name="Prijava", exact=True).click()
    page.get_by_role("link", name="Moji oglasi").click()
    page.get_by_role("link", name="Novi oglas").click()
    page.get_by_role("textbox", name="Naslov").click()
    page.get_by_role("textbox", name="Naslov").fill("Testna igračka")
    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Dodajte ručno ili povucite").click()
    file_chooser = fc_info.value
    file_chooser.set_files("C:\\Users\\Milan\\Desktop\\Progi TESTOVI\\test_slika.jpg")
    page.get_by_role("textbox", name="Unesite opis igračke").click()
    page.get_by_role("textbox", name="Unesite opis igračke").fill("Lijepa igračka u dobrom stanju.")
    page.locator("button").filter(has_text="Odaberite kategoriju").click()
    page.get_by_text("Kocke i konstrukcijske igračke").click()
    page.locator("button").filter(has_text="Korčula").click()
    page.get_by_text("Knin").click()
    page.locator("label").filter(has_text="Rabljeno").click()
    page.get_by_text("Osobno preuzimanje").click()
    page.get_by_role("button", name="Pregledaj i objavi oglas").click()
    page.get_by_role("button", name="Objavi").click()
    page.get_by_role("link", name="Moji oglasi").click()


    page.reload()
    element = page.get_by_role("link", name="Uredi oglas")
    element.click()


    # page.get_by_role("link", name="Uredi oglas").click()
    page.get_by_role("textbox", name="Unesite opis igračke").click()
    page.get_by_role("textbox", name="Unesite opis igračke").press("ArrowRight")
    page.get_by_role("textbox", name="Unesite opis igračke").press("ArrowRight")
    page.get_by_role("textbox", name="Unesite opis igračke").press("ArrowRight")
    page.get_by_role("textbox", name="Unesite opis igračke").press("ArrowRight")
    page.get_by_role("textbox", name="Unesite opis igračke").fill("Lijepa igračka u dobrom stanju. Izmijenjen opis.")
    page.get_by_role("textbox", name="Naslov").click()
    page.get_by_role("textbox", name="Naslov").fill("Testna igračka, promijenjen oglas")
    page.locator("button").filter(has_text="Knin").click()
    page.get_by_text("Klanjec").click()
    page.get_by_role("radio", name="Obnovljeno").click()
    page.get_by_role("button", name="Pregledaj i objavi oglas").click()
    page.get_by_role("button", name="Objavi").click()
    page.get_by_role("heading", name="Testna igračka, promijenjen").click()
    page.get_by_role("heading", name="Kocke i konstrukcijske igračke").click()
    page.get_by_role("heading", name="Obnovljeno").click()
    page.get_by_role("heading", name="Klanjec").click()
    #page.get_by_text("Lijepa igračka u dobrom").click()

    element = page.get_by_text("Testna igračka")

    # Explicitly wait until it is visible
    element.wait_for(state="attached")
    element.scroll_into_view_if_needed()
    element.wait_for(state="visible", timeout=10_000)
    # Ensure it is scrolled into view
    # page.reload()

    # Interact with it
    element.click()
    page.get_by_role("button", name="Obriši oglas").click()
    page.get_by_role("button", name="Obriši").click()
    page.get_by_role("heading", name="Još nemate oglasa").click()
    page.get_by_role("button", name="Test Testić Test Testić Donor").click()
    page.get_by_role("menuitem", name="Odjava").click()
    page.get_by_role("link", name="Idi na prijavu").click()