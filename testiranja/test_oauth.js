const puppeteer = require('puppeteer'); // v23.0.0 or later

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const timeout = 5000;
    page.setDefaultTimeout(timeout);

    {
        const targetPage = page;
        await targetPage.setViewport({
            width: 1075,
            height: 919
        })
    }
    {
        const targetPage = page;
        await targetPage.goto('https://sandbox.playforward.dedyn.io/prijava');
    }
    {
        const targetPage = page;
        const promises = [];
        const startWaitingForEvents = () => {
            promises.push(targetPage.waitForNavigation());
        }
        await puppeteer.Locator.race([
            targetPage.locator('::-p-aria(Prijava s Google računom)'),
            targetPage.locator('div > button'),
            targetPage.locator('::-p-xpath(//*[@id=\\"app\\"]/div/div/div/div[2]/div/div/div/button)'),
            targetPage.locator(':scope >>> div > button'),
            targetPage.locator('::-p-text(Prijava s Google)')
        ])
            .setTimeout(timeout)
            .on('action', () => startWaitingForEvents())
            .click({
              offset: {
                x: 391.5,
                y: 37.25,
              },
            });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        const promises = [];
        const startWaitingForEvents = () => {
            promises.push(targetPage.waitForNavigation());
        }
        await puppeteer.Locator.race([
            targetPage.locator('li:nth-of-type(2) div.pGzURd'),
            targetPage.locator('::-p-xpath(//*[@id=\\"yDmH0d\\"]/c-wiz/main/div[2]/div/div/div[1]/span/section/div/div/div/div/ul/li[2]/div/div[1]/div/div[2]/div[1])'),
            targetPage.locator(':scope >>> li:nth-of-type(2) div.pGzURd')
        ])
            .setTimeout(timeout)
            .on('action', () => startWaitingForEvents())
            .click({
              offset: {
                x: 24.5,
                y: 16.5,
              },
            });
        await Promise.all(promises);
    }
    {
        const targetPage = page;
        await puppeteer.Locator.race([
            targetPage.locator('p.text-highlighted'),
            targetPage.locator('::-p-xpath(//*[@id=\\"reka-dropdown-menu-trigger-v-0\\"]/div/div/p[1])'),
            targetPage.locator(':scope >>> p.text-highlighted'),
            targetPage.locator('::-p-text(Ivan Džepina)')
        ])
            .setTimeout(timeout)
            .click({
              offset: {
                x: 72,
                y: 9,
              },
            });
    }
    {
        const targetPage = page;
        await puppeteer.Locator.race([
            targetPage.locator('a:nth-of-type(2) > span.flex-1 > span'),
            targetPage.locator('::-p-xpath(//*[@id=\\"reka-dropdown-menu-content-v-1\\"]/div/div/a[2]/span[1]/span)'),
            targetPage.locator(':scope >>> a:nth-of-type(2) > span.flex-1 > span'),
            targetPage.locator('::-p-text(Odjava)')
        ])
            .setTimeout(timeout)
            .click({
              offset: {
                x: 43,
                y: 11,
              },
            });
    }
    {
        const targetPage = page;
        await puppeteer.Locator.race([
            targetPage.locator('::-p-aria(Idi na prijavu) >>>> ::-p-aria([role=\\"image\\"])'),
            targetPage.locator('svg'),
            targetPage.locator('::-p-xpath(//*[@id=\\"app\\"]/div/div[4]/div/div/div/a/svg)'),
            targetPage.locator(':scope >>> svg')
        ])
            .setTimeout(timeout)
            .click({
              offset: {
                x: 12.984375,
                y: 21.5,
              },
            });
    }

    await browser.close();

})().catch(err => {
    console.error(err);
    process.exit(1);
});
