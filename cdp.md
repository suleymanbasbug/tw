<!-- SeleniumBase Docs -->

## [<img src="https://seleniumbase.github.io/img/logo6.png" title="SeleniumBase" width="32">](https://github.com/seleniumbase/SeleniumBase/) CDP Mode 🐙

🐙 <b translate="no">SeleniumBase</b> <b translate="no">CDP Mode</b> (Chrome Devtools Protocol Mode) is a special mode inside of <b><a href="https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/uc_mode.md" translate="no"><span translate="no">SeleniumBase UC Mode</span></a></b> that lets bots appear human while controlling the browser with the <b translate="no">CDP-Driver</b>. Although regular <b translate="no">UC Mode</b> can't perform <span translate="no">WebDriver</span> actions while the <code>driver</code> is disconnected from the browser, the <b translate="no">CDP-Driver</b> can.

--------

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=Mr90iQmNsKM"><img src="https://github.com/user-attachments/assets/91e7ff7b-d155-4ba9-b17b-b097825fcf42" title="SeleniumBase on YouTube" width="320" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=Mr90iQmNsKM">Watch the CDP Mode tutorial on YouTube! ▶️</a></b>)</p>

--------

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=vt2zsdiNh3U"><img src="https://github.com/user-attachments/assets/82ab2715-727e-4d09-9314-b8905795dc43" title="SeleniumBase on YouTube" width="320" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=vt2zsdiNh3U">Watch "Hacking websites with CDP" on YouTube! ▶️</a></b>)</p>

--------

<!-- YouTube View --><a href="https://www.youtube.com/watch?v=gEZhTfaIxHQ"><img src="https://github.com/user-attachments/assets/656977e1-5d66-4d1c-9eec-0aaa41f6522f" title="SeleniumBase on YouTube" width="320" /></a>
<p>(<b><a href="https://www.youtube.com/watch?v=gEZhTfaIxHQ">Watch "Web-Scraping with GitHub Actions" on YouTube! ▶️</a></b>)</p>

--------

👤 <b translate="no">UC Mode</b> avoids bot-detection by first disconnecting WebDriver from the browser at strategic times, calling special <code>PyAutoGUI</code> methods to bypass CAPTCHAs (as needed), and finally reconnecting the <code>driver</code> afterwards so that WebDriver actions can be performed again. Although this approach works for bypassing simple CAPTCHAs, more flexibility is needed for bypassing bot-detection on websites with advanced protection. (That's where <b translate="no">CDP Mode</b> comes in.)

🐙 <b translate="no">CDP Mode</b> is based on <a href="https://github.com/HyperionGray/python-chrome-devtools-protocol" translate="no">python-cdp</a>, <a href="https://github.com/HyperionGray/trio-chrome-devtools-protocol" translate="no">trio-cdp</a>, and <a href="https://github.com/ultrafunkamsterdam/nodriver" translate="no">nodriver</a>. <code>trio-cdp</code> is an early implementation of <code>python-cdp</code>, and <code>nodriver</code> is a modern implementation of <code>python-cdp</code>. (Refactored <code>Python-CDP</code> code is imported from <a href="https://github.com/mdmintz/MyCDP" translate="no">MyCDP</a>.)

🐙 <b translate="no">CDP Mode</b> includes multiple updates to the above, such as:

* Sync methods. (Using `async`/`await` is not necessary!)
* The ability to use WebDriver and CDP-Driver together.
* Backwards compatibility for existing UC Mode scripts.
* More configuration options when launching browsers.
* More methods. (And bug-fixes for existing methods.)
* `PyAutoGUI` integration for advanced stealth abilities.
* Faster response time for support. (Eg. [Discord Chat](https://discord.gg/EdhQTn3EyE))

--------

### 🐙 <b translate="no">CDP Mode</b> Usage:

* **`sb.activate_cdp_mode(url)`**

> (Call that from a **UC Mode** script)

That disconnects WebDriver from Chrome (which prevents detection), and gives you access to `sb.cdp` methods (which don't trigger anti-bot checks).

Simple example from [SeleniumBase/examples/cdp_mode/raw_gitlab.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_gitlab.py):

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale="en") as sb:
    url = "https://gitlab.com/users/sign_in"
    sb.activate_cdp_mode(url)
    sb.sleep(2.2)
    sb.uc_gui_click_captcha()
```

<img src="https://seleniumbase.github.io/other/cf_sec.jpg" title="SeleniumBase" width="332"> <img src="https://seleniumbase.github.io/other/gitlab_bypass.png" title="SeleniumBase" width="288">

(If the CAPTCHA wasn't bypassed automatically when going to the URL, then `sb.uc_gui_click_captcha()` gets the job done with a mouse click from [PyAutoGUI](https://github.com/asweigart/pyautogui).)

ℹ️ Note that `PyAutoGUI` is an optional dependency. If calling a method that uses it when not already installed, then `SeleniumBase` installs `PyAutoGUI` at run-time.

--------

You can also use `sb.cdp.gui_click_element(selector)` to click on elements using `PyAutoGUI`. (This is useful when clicking inside `#shadow-root`.) Example:

```python
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    url = "www.planetminecraft.com/account/sign_in/"
    sb.activate_cdp_mode(url)
    sb.sleep(2)
    sb.cdp.gui_click_element("#turnstile-widget div")
    sb.wait_for_element_absent("input[disabled]")
    sb.sleep(2)
```

<img src="https://seleniumbase.github.io/other/planet_mc.png" title="SeleniumBase" width="480">

When using `sb.cdp.gui_click_element(selector)` on CF Turnstiles, use the parent `selector` that appears **above** the `#shadow-root` element:
Eg. `sb.cdp.gui_click_element("#turnstile-widget div")`

<img src="https://seleniumbase.github.io/other/above_shadow.png" title="SeleniumBase" width="480">

In most cases, `sb.uc_gui_click_captcha()` is good enough for CF Turnstiles without needing `sb.cdp.gui_click_element(selector)`. (See [SeleniumBase/examples/cdp_mode/raw_planetmc.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_planetmc.py))

--------

### 🐙 Here are a few common `sb.cdp` methods:

* `sb.cdp.click(selector)`  (Uses the CDP API to click)
* `sb.cdp.click_if_visible(selector)`  (Click if visible)
* `sb.cdp.gui_click_element(selector)`  (Uses `PyAutoGUI`)
* `sb.cdp.type(selector, text)`  (Type text into a selector)
* `sb.cdp.press_keys(selector, text)`  (Human-speed `type`)
* `sb.cdp.select_all(selector)`  (Returns matching elements)
* `sb.cdp.get_text(selector)`  (Returns the element's text)

Methods that start with `sb.cdp.gui` use `PyAutoGUI` for interaction.

To use WebDriver methods again, call:

* **`sb.reconnect()`** or **`sb.connect()`**

(Note that reconnecting allows anti-bots to detect you, so only reconnect if it is safe to do so.)

To disconnect again, call:

* **`sb.disconnect()`**

While disconnected, if you accidentally call a WebDriver method, then <b translate="no">SeleniumBase</b> will attempt to use the <b translate="no">CDP Mode</b> version of that method (if available). For example, if you accidentally call `sb.click(selector)` instead of `sb.cdp.click(selector)`, then your WebDriver call will automatically be redirected to the <b translate="no">CDP Mode</b> version. Not all WebDriver methods have a matching <b translate="no">CDP Mode</b> method. In that scenario, calling a WebDriver method while disconnected could raise an error, or make WebDriver automatically reconnect first.

To find out if WebDriver is connected or disconnected, call:

* **`sb.is_connected()`**

<b>Note:</b> When <b translate="no">CDP Mode</b> is initialized from <b translate="no">UC Mode</b>, the WebDriver is disconnected from the browser. (The stealthy <b translate="no">CDP-Driver</b> takes over.)

--------

### 🐙 <b translate="no">CDP Mode</b> examples ([SeleniumBase/examples/cdp_mode](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode))

<p><div /></p>

<div></div>
<details>
<summary> ▶️ 🔖 <b>Example 1: (Pokemon site using Incapsula/Imperva protection with invisible reCAPTCHA)</b></summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.pokemon.com/us"
    sb.activate_cdp_mode(url)
    sb.sleep(3.2)
    sb.cdp.click("button#onetrust-accept-btn-handler")
    sb.sleep(1.2)
    sb.cdp.click("a span.icon_pokeball")
    sb.sleep(2.5)
    sb.cdp.click('b:contains("Show Advanced Search")')
    sb.sleep(2.5)
    sb.cdp.click('span[data-type="type"][data-value="electric"]')
    sb.sleep(0.5)
    sb.scroll_into_view("a#advSearch")
    sb.sleep(0.5)
    sb.cdp.click("a#advSearch")
    sb.sleep(1.2)
    sb.cdp.click('img[src*="img/pokedex/detail/025.png"]')
    sb.cdp.assert_text("Pikachu", 'div[class*="title"]')
    sb.cdp.assert_element('img[alt="Pikachu"]')
    sb.cdp.scroll_into_view("div.pokemon-ability-info")
    sb.sleep(1.2)
    sb.cdp.flash('div[class*="title"]')
    sb.cdp.flash('img[alt="Pikachu"]')
    sb.cdp.flash("div.pokemon-ability-info")
    name = sb.cdp.get_text("label.styled-select")
    info = sb.cdp.get_text("div.version-descriptions p.active")
    print("*** %s: ***\n* %s" % (name, info))
    sb.sleep(2)
    sb.cdp.highlight_overlay("div.pokemon-ability-info")
    sb.sleep(2)
    sb.cdp.open("https://events.pokemon.com/EventLocator/")
    sb.sleep(3)
    sb.cdp.click('button span:contains("Premier Events")')
    sb.sleep(1)
    events = sb.cdp.select_all('div[class="event-info"]')
    print("*** Upcoming Premier Events for Pokémon: ***")
    for event in events:
        print("* " + event.text)
    sb.sleep(2)
```

</details>

> [SeleniumBase/examples/cdp_mode/raw_pokemon.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_pokemon.py)


<div></div>
<details>
<summary> ▶️ 🔖 <b>Example 2: (Hyatt site using Kasada protection)</b></summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.hyatt.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible('button[aria-label="Close"]')
    sb.cdp.click_if_visible("#onetrust-reject-all-handler")
    sb.sleep(2)
    location = "Anaheim, CA, USA"
    sb.cdp.type('input[data-id="location"]', location)
    sb.cdp.click("button.quickbookSearchFormButton")
    sb.sleep(5)
    card_info = 'div[data-booking-status="BOOKABLE"] [class*="HotelCard_info"]'
    hotels = sb.cdp.select_all(card_info)
    print("Hyatt Hotels in %s:" % location)
    print("(" + sb.cdp.get_text("ul.b-color_text-white") + ")")
    if len(hotels) == 0:
        print("No availability over the selected dates!")
    for hotel in hotels:
        info = hotel.text.strip()
        if "Avg/Night" in info and not info.startswith("Rates from"):
            name = info.split("  (")[0].split(" + ")[0].split(" Award Cat")[0]
            name = name.split(" Rates from :")[0]
            price = "?"
            if "Rates from : " in info:
                price = info.split("Rates from : ")[1].split(" Avg/Night")[0]
            print("* %s => %s" % (name, price))
```

</details>

> [SeleniumBase/examples/cdp_mode/raw_hyatt.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_hyatt.py)


<div></div>
<details>
<summary> ▶️ 🔖 <b>Example 3: (BestWestern site using DataDome protection)</b></summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", ad_block=True) as sb:
    url = "https://www.bestwestern.com/en_US.html"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible(".onetrust-close-btn-handler")
    sb.sleep(1)
    sb.cdp.click("input#destination-input")
    sb.sleep(2)
    location = "Palm Springs, CA, USA"
    sb.cdp.press_keys("input#destination-input", location)
    sb.sleep(1)
    sb.cdp.click("ul#google-suggestions li")
    sb.sleep(1)
    sb.cdp.click("button#btn-modify-stay-update")
    sb.sleep(4)
    sb.cdp.click("label#available-label")
    sb.sleep(2.5)
    print("Best Western Hotels in %s:" % location)
    summary_details = sb.cdp.get_text("#summary-details-column")
    dates = summary_details.split("DESTINATION")[-1]
    dates = dates.split(" CHECK-OUT")[0].strip() + " CHECK-OUT"
    dates = dates.replace("  ", " ")
    print("(Dates: %s)" % dates)
    flip_cards = sb.cdp.select_all(".flipCard")
    for i, flip_card in enumerate(flip_cards):
        hotel = flip_card.query_selector(".hotelName")
        price = flip_card.query_selector(".priceSection")
        if hotel and price:
            print("* %s: %s => %s" % (
                i + 1, hotel.text.strip(), price.text.strip())
            )
```

</details>

> [SeleniumBase/examples/cdp_mode/raw_bestwestern.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_bestwestern.py)


<div></div>
<details>
<summary> ▶️ 🔖 <b>Example 4: (Walmart site using Akamai protection with PerimeterX)</b></summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://www.walmart.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click_if_visible('[data-automation-id*="close-mark"]')
    sb.sleep(0.3)
    sb.cdp.mouse_click('input[aria-label="Search"]')
    sb.sleep(1.2)
    search = "Settlers of Catan Board Game"
    required_text = "Catan"
    sb.cdp.press_keys('input[aria-label="Search"]', search + "\n")
    sb.sleep(3.8)
    if sb.is_element_visible("#px-captcha"):
        sb.cdp.gui_click_and_hold("#px-captcha", 12)
        sb.sleep(3.2)
        if sb.is_element_visible("#px-captcha"):
            sb.cdp.gui_click_and_hold("#px-captcha", 12)
            sb.sleep(3.2)
    sb.cdp.remove_elements('[data-testid="skyline-ad"]')
    print('*** Walmart Search for "%s":' % search)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    items = sb.cdp.find_elements('div[data-testid="list-view"]')
    for item in items:
        if required_text in item.text:
            description = item.querySelector(
                '[data-automation-id="product-title"]'
            )
            if description and description.text not in unique_item_text:
                unique_item_text.append(description.text)
                print("* " + description.text)
                price = item.querySelector(
                    '[data-automation-id="product-price"]'
                )
                if price:
                    price_text = price.text
                    price_text = price_text.split("current price Now ")[-1]
                    price_text = price_text.split("current price ")[-1]
                    price_text = price_text.split(" ")[0]
                    print("  (" + price_text + ")")
```

</details>

> [SeleniumBase/examples/cdp_mode/raw_walmart.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_walmart.py)


<div></div>
<details>
<summary> ▶️ 🔖 <b>Example 5: (Nike site using Shape Security)</b></summary>

```python
from seleniumbase import SB

with SB(uc=True, test=True, locale="en", pls="none") as sb:
    url = "https://www.nike.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.click('div[data-testid="user-tools-container"]')
    sb.sleep(1.5)
    search = "Nike Air Force 1"
    sb.cdp.press_keys('input[type="search"]', search)
    sb.sleep(4)
    elements = sb.cdp.select_all('ul[data-testid*="products"] figure .details')
    if elements:
        print('**** Found results for "%s": ****' % search)
    for element in elements:
        print("* " + element.text)
    sb.sleep(2)
```

</details>

> [SeleniumBase/examples/cdp_mode/raw_nike.py](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/cdp_mode/raw_nike.py)

<p><div /></p>

(<b>Note:</b> Extra <code translate="no">sb.sleep()</code> calls have been added to prevent bot-detection because some sites will flag you as a bot if you perform actions too quickly.)

(<b>Note:</b> Some sites may IP-block you for 36 hours or more if they catch you using regular <span translate="no">Selenium WebDriver</span>. Be extra careful when creating and/or modifying automation scripts that run on them.)

--------

### 🐙 <b translate="no">CDP Mode</b> API / Methods

```python
sb.cdp.get(url, **kwargs)
sb.cdp.open(url, **kwargs)
sb.cdp.reload(ignore_cache=True, script_to_evaluate_on_load=None)
sb.cdp.refresh(*args, **kwargs)
sb.cdp.get_event_loop()
sb.cdp.add_handler(event, handler)
sb.cdp.find_element(selector, best_match=False, timeout=None)
sb.cdp.find(selector, best_match=False, timeout=None)
sb.cdp.locator(selector, best_match=False, timeout=None)
sb.cdp.find_element_by_text(text, tag_name=None, timeout=None)
sb.cdp.find_all(selector, timeout=None)
sb.cdp.find_elements_by_text(text, tag_name=None)
sb.cdp.select(selector, timeout=None)
sb.cdp.select_all(selector, timeout=None)
sb.cdp.find_elements(selector, timeout=None)
sb.cdp.find_visible_elements(selector, timeout=None)
sb.cdp.click(selector, timeout=None)
sb.cdp.click_if_visible(selector)
sb.cdp.click_visible_elements(selector, limit=0)
sb.cdp.click_nth_element(selector, number)
sb.cdp.click_nth_visible_element(selector, number)
sb.cdp.click_link(link_text)
sb.cdp.go_back()
sb.cdp.go_forward()
sb.cdp.get_navigation_history()
sb.cdp.tile_windows(windows=None, max_columns=0)
sb.cdp.grant_permissions(permissions, origin=None)
sb.cdp.grant_all_permissions()
sb.cdp.reset_permissions()
sb.cdp.get_all_cookies(*args, **kwargs)
sb.cdp.set_all_cookies(*args, **kwargs)
sb.cdp.save_cookies(*args, **kwargs)
sb.cdp.load_cookies(*args, **kwargs)
sb.cdp.clear_cookies()
sb.cdp.sleep(seconds)
sb.cdp.bring_active_window_to_front()
sb.cdp.bring_to_front()
sb.cdp.get_active_element()
sb.cdp.get_active_element_css()
sb.cdp.click_active_element()
sb.cdp.mouse_click(selector, timeout=None)
sb.cdp.nested_click(parent_selector, selector)
sb.cdp.get_nested_element(parent_selector, selector)
sb.cdp.select_option_by_text(dropdown_selector, option)
sb.cdp.select_option_by_index(dropdown_selector, option)
sb.cdp.select_option_by_value(dropdown_selector, option)
sb.cdp.flash(selector, duration=1, color="44CC88", pause=0)
sb.cdp.highlight(selector)
sb.cdp.focus(selector)
sb.cdp.highlight_overlay(selector)
sb.cdp.get_parent(element)
sb.cdp.remove_element(selector)
sb.cdp.remove_from_dom(selector)
sb.cdp.remove_elements(selector)
sb.cdp.send_keys(selector, text, timeout=None)
sb.cdp.press_keys(selector, text, timeout=None)
sb.cdp.type(selector, text, timeout=None)
sb.cdp.set_value(selector, text, timeout=None)
sb.cdp.clear_input(selector, timeout=None)
sb.cdp.clear(selector, timeout=None)
sb.cdp.submit(selector)
sb.cdp.evaluate(expression)
sb.cdp.js_dumps(obj_name)
sb.cdp.maximize()
sb.cdp.minimize()
sb.cdp.medimize()
sb.cdp.set_window_rect(x, y, width, height)
sb.cdp.reset_window_size()
sb.cdp.open_new_window(url=None, switch_to=True)
sb.cdp.switch_to_window(window)
sb.cdp.switch_to_newest_window()
sb.cdp.open_new_tab(url=None, switch_to=True)
sb.cdp.switch_to_tab(tab)
sb.cdp.switch_to_newest_tab()
sb.cdp.close_active_tab()
sb.cdp.get_active_tab()
sb.cdp.get_tabs()
sb.cdp.get_window()
sb.cdp.get_text(selector)
sb.cdp.get_title()
sb.cdp.get_current_url()
sb.cdp.get_origin()
sb.cdp.get_page_source()
sb.cdp.get_user_agent()
sb.cdp.get_cookie_string()
sb.cdp.get_locale_code()
sb.cdp.get_local_storage_item(key)
sb.cdp.get_session_storage_item(key)
sb.cdp.get_screen_rect()
sb.cdp.get_window_rect()
sb.cdp.get_window_size()
sb.cdp.get_window_position()
sb.cdp.get_element_rect(selector, timeout=None)
sb.cdp.get_element_size(selector, timeout=None)
sb.cdp.get_element_position(selector, timeout=None)
sb.cdp.get_gui_element_rect(selector, timeout=None)
sb.cdp.get_gui_element_center(selector, timeout=None)
sb.cdp.get_document()
sb.cdp.get_flattened_document()
sb.cdp.get_element_attributes(selector)
sb.cdp.get_element_attribute(selector, attribute)
sb.cdp.get_attribute(selector, attribute)
sb.cdp.get_element_html(selector)
sb.cdp.get_mfa_code(totp_key=None)
sb.cdp.enter_mfa_code(selector, totp_key=None, timeout=None)
sb.cdp.set_locale(locale)
sb.cdp.set_local_storage_item(key, value)
sb.cdp.set_session_storage_item(key, value)
sb.cdp.set_attributes(selector, attribute, value)
sb.cdp.is_attribute_present(selector, attribute, value=None)
sb.cdp.is_online()
sb.cdp.gui_press_key(key)
sb.cdp.gui_press_keys(keys)
sb.cdp.gui_write(text)
sb.cdp.gui_click_x_y(x, y, timeframe=0.25)
sb.cdp.gui_click_element(selector, timeframe=0.25)
sb.cdp.gui_click_captcha()
sb.cdp.gui_drag_drop_points(x1, y1, x2, y2, timeframe=0.35)
sb.cdp.gui_drag_and_drop(drag_selector, drop_selector, timeframe=0.35)
sb.cdp.gui_click_and_hold(selector, timeframe=0.35)
sb.cdp.gui_hover_x_y(x, y)
sb.cdp.gui_hover_element(selector)
sb.cdp.gui_hover_and_click(hover_selector, click_selector)
sb.cdp.internalize_links()
sb.cdp.is_checked(selector)
sb.cdp.is_selected(selector)
sb.cdp.check_if_unchecked(selector)
sb.cdp.select_if_unselected(selector)
sb.cdp.uncheck_if_checked(selector)
sb.cdp.unselect_if_selected(selector)
sb.cdp.is_element_present(selector)
sb.cdp.is_element_visible(selector)
sb.cdp.is_text_visible(text, selector="body")
sb.cdp.is_exact_text_visible(text, selector="body")
sb.cdp.wait_for_text(text, selector="body", timeout=None)
sb.cdp.wait_for_text_not_visible(text, selector="body", timeout=None)
sb.cdp.wait_for_element_visible(selector, timeout=None)
sb.cdp.wait_for_element(selector, timeout=None)
sb.cdp.wait_for_element_not_visible(selector, timeout=None)
sb.cdp.wait_for_element_absent(selector, timeout=None)
sb.cdp.wait_for_any_of_elements_visible(*args, **kwargs)
sb.cdp.wait_for_any_of_elements_present(*args, **kwargs)
sb.cdp.assert_any_of_elements_visible(*args, **kwargs)
sb.cdp.assert_any_of_elements_present(*args, **kwargs)
sb.cdp.assert_element(selector, timeout=None)
sb.cdp.assert_element_visible(selector, timeout=None)
sb.cdp.assert_element_present(selector, timeout=None)
sb.cdp.assert_element_absent(selector, timeout=None)
sb.cdp.assert_element_not_visible(selector, timeout=None)
sb.cdp.assert_element_attribute(selector, attribute, value=None)
sb.cdp.assert_title(title)
sb.cdp.assert_title_contains(substring)
sb.cdp.assert_url(url)
sb.cdp.assert_url_contains(substring)
sb.cdp.assert_text(text, selector="html", timeout=None)
sb.cdp.assert_exact_text(text, selector="html", timeout=None)
sb.cdp.assert_text_not_visible(text, selector="body", timeout=None)
sb.cdp.assert_true()
sb.cdp.assert_false()
sb.cdp.assert_equal(first, second)
sb.cdp.assert_not_equal(first, second)
sb.cdp.assert_in(first, second)
sb.cdp.assert_not_in(first, second)
sb.cdp.scroll_into_view(selector)
sb.cdp.scroll_to_y(y)
sb.cdp.scroll_to_top()
sb.cdp.scroll_to_bottom()
sb.cdp.scroll_up(amount=25)
sb.cdp.scroll_down(amount=25)
sb.cdp.save_screenshot(name, folder=None, selector=None)
sb.cdp.print_to_pdf(name, folder=None)
sb.cdp.save_as_pdf(name, folder=None)
```

ℹ️ When available, calling `sb.METHOD()` redirects to `sb.cdp.METHOD()` because regular SB methods automatically call their CDP Mode counterparts to maintain stealth when CDP Mode is active.

--------

### 🐙 <b translate="no">Pure CDP Mode</b> (<code translate="no">sb_cdp</code>)

<b translate="no">Pure CDP Mode</b> doesn't use WebDriver for anything. The browser is launched using CDP, and all browser actions are performed using CDP (or <code>PyAutoGUI</code>). Initialization:

```python
from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(url=None, **kwargs)
```

<b translate="no">Pure CDP Mode</b> includes all methods from regular CDP Mode, except that they're called directly from <code>sb</code> instead of <code>sb.cdp</code>. Eg: <code>sb.gui_click_captcha()</code>. To quit a CDP-launched browser, use `sb.driver.stop()`.

Basic example from [SeleniumBase/examples/cdp_mode/raw_cdp_turnstile.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_cdp_turnstile.py):

```python
from seleniumbase import sb_cdp

url = "https://seleniumbase.io/apps/turnstile"
sb = sb_cdp.Chrome(url)
sb.gui_click_captcha()
sb.sleep(2)
sb.driver.stop()
```

Another example: ([SeleniumBase/examples/cdp_mode/raw_cdp_methods.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/cdp_mode/raw_cdp_methods.py))

```python
from seleniumbase import sb_cdp

url = "https://seleniumbase.io/demo_page"
sb = sb_cdp.Chrome(url)
sb.press_keys("input", "Text")
sb.highlight("button")
sb.type("textarea", "Here are some words")
sb.click("button")
sb.set_value("input#mySlider", "100")
sb.click_visible_elements("input.checkBoxClassB")
sb.select_option_by_text("#mySelect", "Set to 75%")
sb.gui_hover_and_click("#myDropdown", "#dropOption2")
sb.gui_click_element("#checkBox1")
sb.gui_drag_and_drop("img#logo", "div#drop2")
sb.nested_click("iframe#myFrame3", ".fBox")
sb.sleep(2)
sb.driver.stop()
```

ℹ️ Even if you don't call `sb.driver.stop()`, the browser still quits after the script goes out-of-scope.

--------

### 🐙 <b translate="no">CDP Mode</b> WebElement API / Methods

After finding an element in CDP Mode, you can access `WebElement` methods:

(Eg. After `element = sb.find_element(selector)`)

```python
element.clear_input()
element.click()
element.flash(duration=0.5, color="EE4488")
element.focus()
element.gui_click(timeframe=0.25)
element.highlight_overlay()
element.mouse_click()
element.mouse_drag(destination)
element.mouse_move()
element.press_keys(text)
element.query_selector(selector)
element.querySelector(selector)
element.query_selector_all(selector)
element.querySelectorAll(selector)
element.remove_from_dom()
element.save_screenshot(*args, **kwargs)
element.save_to_dom()
element.scroll_into_view()
element.select_option()
element.send_file(*file_paths)
element.send_keys(text)
element.set_text(value)
element.type(text)
element.get_position()
element.get_html()
element.get_js_attributes()
element.get_attribute(attribute)
element.get_parent()
```

--------

<img src="https://seleniumbase.github.io/cdn/img/sb_text_f.png" alt="SeleniumBase" title="SeleniumBase" align="center" width="335">

<div><a href="https://github.com/seleniumbase/SeleniumBase"><img src="https://seleniumbase.github.io/cdn/img/sb_logo_gs.png" alt="SeleniumBase" title="SeleniumBase" width="335" /></a></div>