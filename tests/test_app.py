from playwright.sync_api import Page, expect

# we can render the homepage

def test_get_homepage(page, test_web_address):
    page.goto(f"http://{test_web_address}/")
    title = page.locator("h1:has-text('Chitter')")
    expect(title).to_be_visible()

# we need to see a list of posts on the homepage 

def test_get_posts(page, test_web_address):
    page.goto(f"http://{test_web_address}/")
    post = page.locator("ul > div > p:has-text('Username: username1')")
    expect(post).to_be_visible()