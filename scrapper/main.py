import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


USER_EMAIL = os.getenv('USER_EMAIL')
USER_PASSWORD = os.getenv('USER_PASSWORD')


def empty_shopping_cart(driver):
    open_cart_container = driver.find_element(
        By.CSS_SELECTOR, 'div.cart.generalHeader__cart')
    items_count = None

    try:
        items_count = int(open_cart_container.find_element(
            By.CSS_SELECTOR, 'sup.ant-badge-count').get_attribute('title'), 10)
    except Exception as error:
        print("not badge count found")

    if(items_count is None):
        return

    open_cart_button = open_cart_container.find_element(
        By.CLASS_NAME, 'btn--transparent')
    open_cart_button.click()

    driver.implicitly_wait(6)

    if(items_count == 1):
        cart_products = driver.find_elements(By.CLASS_NAME, 'cart__product')
        for product in cart_products:
            while(True):
                try:
                    # wait for product to be updated, maybe it's bettter to use EC here...
                    time.sleep(1)
                    driver.implicitly_wait(16)
                    product_quantity = int(product.find_element(
                        By.CLASS_NAME, 'number-spinner__spinner__value').text, 10)
                    if(product_quantity == 1):
                        remove_product_button = product.find_element(
                            By.CLASS_NAME, 'number-spinner__spinner__remove-btn')
                        remove_product_button.click()
                        driver.implicitly_wait(6)
                        break
                    else:
                        decrease_product_button = product.find_element(
                            By.CLASS_NAME, 'number-spinner__spinner__subtract-btn')
                        decrease_product_button.click()
                        driver.implicitly_wait(6)
                except Exception as error:
                    print("ERROR: ", error)
    else:
        empty_shopping_cart = driver.find_element(
            By.XPATH, '//p[text()="Vaciar carrito"]')

        empty_shopping_cart.click()

        driver.implicitly_wait(5)

        parent_element = empty_shopping_cart.find_element(By.XPATH, '..')

        confirm_action_to_empty_cart = parent_element.find_element(
            By.XPATH, '//button[text()="Sí"]')
        confirm_action_to_empty_cart.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//p[text()="No has agregado productos a tu carrito."]')))

    close_shopping_cart = driver.find_element(
        By.CSS_SELECTOR, 'button[aria-label="Close"]')
    close_shopping_cart.click()


def get_lower_cost_product(test, product_name):
    lower_cost_product = test[0]
    lower_cost = int(lower_cost_product.find_element(
        By.CLASS_NAME, 'prod--default__price__current').text.replace('$', '').replace('.', ''), 10)

    for product in test:
        current_product_cost = int(product.find_element(
            By.CLASS_NAME, 'prod--default__price__current').text.replace('$', '').replace('.', ''), 10)

        if(current_product_cost < lower_cost):
            lower_cost = current_product_cost
            lower_cost_product = product

    name = lower_cost_product.find_element(By.CLASS_NAME, 'prod__name').text
    image_url = lower_cost_product.find_element(
        By.CLASS_NAME, 'prod__image__img ').get_attribute('src')

    return {"original_product_name": product_name, "results": {"name": name, "cost": lower_cost, "image_url": image_url}}


def search(products):

    current_environment = os.getenv("ENV")
    driver = None
    if current_environment == "dev":
        os.environ['PATH'] = os.path.join(
            os.path.dirname(__file__), 'webDrivers')

        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        # options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--disable-dev-shm-usuage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROME_DRIVER_PATH"), options=chrome_options)

    driver.get("https://domicilios.tiendasd1.com")

    driver.implicitly_wait(6)

    try:
        logInPopupElement = driver.find_element(By.CLASS_NAME, "user__account")
        logInPopupElement.click()

        logInElement = driver.find_element(By.XPATH,
                                           "/html/body/div[3]/div/div/div/label[3]/span[2]/div")
        driver.implicitly_wait(6)

        logInElement.click()

        driver.implicitly_wait(6)

        email_input = driver.find_element(By.ID, "signup_email")
        password_input = driver.find_element(By.ID, "signup_password")

        email_input.send_keys(USER_EMAIL)
        email_input.send_keys(Keys.TAB)

        password_input.send_keys(USER_PASSWORD)
        password_input.send_keys(Keys.ENTER)
    except Exception as error:
        print('error ', error)
        return driver.get_screenshot_as_base64()

    try:
        shipping_button = driver.find_element(
            By.XPATH, '/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div/div/div')

        shipping_button.click()

        home_address = driver.find_element(
            By.XPATH, '/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[1]')

        home_address.click()
    except:
        print('didnt find the shippment or home address modal')

    driver.implicitly_wait(10)

    results_list = []

    # empty_shopping_cart(driver)

    for product in products:
        search_input_container = driver.find_element(
            By.CLASS_NAME, "searchInput__container")

        search_input = search_input_container.find_element(
            By.CLASS_NAME, 'ant-input')
        if search_input.get_attribute("value") != "":
            # clear_input = search_input_container.find_element(
            #     By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.ant-input-search-button')
            clear_input = driver.find_element(
                By.XPATH, '//*[@id="app"]/div/div[1]/div/div[1]/div[5]/div/span/span/span[1]/span[2]/button')
            clear_input.click()

        search_input.clear()
        search_input.send_keys(product.name)
        search_input.send_keys(Keys.ENTER)

        try:
            products = driver.find_elements(
                By.XPATH, '//span[@data-testid[contains(.,"product-card")]]')

            search_result = get_lower_cost_product(products, product.name)
        except Exception as error:
            print("product not found ", product.name)

        results_list.append(search_result)

    return results_list
    ############ add product for the final order ############
    # open_product_operator = result.find_element(By.CSS_SELECTOR, 'button')

    # open_product_operator.click()

    # add_product_operator = result.find_element(
    #     By.CLASS_NAME, 'number__spinner__spinner__add-btn')

    # add_product_operator.click()

    # add_product_operator = result.find_element(
    #     By.CLASS_NAME, 'number__spinner__spinner__add-btn')

    # add_product_operator.click()

    # add_product_operator = result.find_element(
    #     By.CLASS_NAME, 'number__spinner__spinner__add-btn')

    # add_product_operator.click()

    # time.sleep(15)
    # driver.close()
