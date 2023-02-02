import asyncio

from playwright.async_api import Playwright, async_playwright
from playwright_recaptcha import recaptchav2
from bs4 import BeautifulSoup as bs
# import aiohttp
import re
async def run(playwright: Playwright) -> None:
    proxies={'server': 'http://pr.oxylabs.io:7777',
                'username': 'docugs',
                'password': 'Asdasd123123'}
    browser = await playwright.chromium.launch(headless=True, proxy=proxies)
    context = await browser.newContext()
    page = await context.newPage()
    page.set_default_navigation_timeout(70000)
    page.set_default_timeout(100000)
    await page.goto('https://www.accesssportsmed.com/payment-gateway/')
    await page.locator("input[name=\"x_user1\"]").dblclick()
    await page.locator("input[name=\"x_user1\"]").fill("asdasd asdasd")
    await page.locator("input[name=\"x_user2\"]").click()
    await page.locator("input[name=\"x_user2\"]").fill("32123123")
    await page.get_by_role("button", name="Pay Now").click()
    await page.get_by_label("Amount").fill("1")
    await page.get_by_text("Amount USD Submit").click()
    await page.get_by_role("button", name="Submit").click()
    await page.locator("#exact_cardholder_name").click()
    await page.locator("#exact_cardholder_name").fill("sdasdas asdsa")
    await page.locator("#x_card_num").click()
    await page.locator("#x_card_num").fill("5129722024536801")
    await page.locator("#x_exp_date").click()
    await page.locator("#x_exp_date").fill("0227")
    await page.locator("#x_card_code").click()
    await page.locator("#x_card_code").fill("000")
    await page.locator("#x_card_code").press("Tab")
    await page.locator("#cvd_presence_ind").press("Tab")
    await page.locator("#x_address").fill("dsaasd")
    await page.locator("#x_city").click()
    await page.locator("#x_city").fill("sadas")
    await page.get_by_text("Address City State/Province Alabama Alaska American Samoa Arizona Arkansas Armed").click()
    await page.locator("#x_state").select_option("California")
    await page.locator("#x_zip").click()
    await page.locator("#x_zip").fill("90001")
    await page.locator("#cc_email").click()
    await page.locator("#cc_email").fill("dsadasgsa@gmail.com")
    async with recaptchav2.AsyncSolver(page) as solver:
        try:
            isSolved = False
            token = await solver.solve_recaptcha()
            print(token) 
            if True:
                isSolved = True
            
            # return response.ok    
        except : 
            print('retrying to solve the captcha again..')
            print(page.body().text)
            isSolved = False
        finally:
            if(isSolved == True):
                return page
            else:
                print('retrying request is exceed the limits.. i will stop this process cause of error. you can try again if you want')
                isSolved = False
                return {"Is_Solved": isSolved}
        # button = await page.querySelector("button")
        # await button.click()
            
async def parse_respo(page):           
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    await page.locator('xpath=//*[@id="cc"]/form/input[3]').click() 
    async with page.expect_response(re.search("https://checkout.globalgatewaye4.firstdata.com/payment/final_receipt?merchant") is True) as response:
       
       res = response.value
       respo = res.body()
    return respo  
    
# https://checkout.globalgatewaye4.firstdata.com/payment/final_receipt?merchant=WSP-ACCES-o7E&lQDhTA&servdt5=3
    # ---------------------
    # await context.close()
    # await browser.close()

async def main(cc) -> None:
    try:
        async with async_playwright() as playwright:
            retries = 0
            limit = 5
            while retries <= limit:
                retries = retries + 1         
                page = await run(playwright)
                response = await parse_respo(page)
                if not response['False']:
                    return response
                await page.close()
            return response
    except:
        print(Exception)
        return {"error": Exception}
        

# asyncio.run(main())
