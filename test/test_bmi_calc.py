import time
import unittest
from ddt import ddt, data, unpack
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import FirefoxOptions

opts = FirefoxOptions()
opts.add_argument("--width=800")
opts.add_argument("--height=600")
opts.add_argument('--headless')


@ddt
class BMICalcDDT(unittest.TestCase):
    def setUp(self):
        # create a new Firefox session
        self.driver = webdriver.Firefox(options=opts)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        # navigate to the BMI calculator page
        self.driver.get("https://asmbs.org/patients/bmi-calculator")

    # specify test data using @data decorator
    @data(("160", "5", "6", 25.62, "Overweight"),
          ("168", "5", "7", 26.1, "Overweight"),
          ("181", "5", "9", 26.52, "Overweight"))
    @unpack
    def test_bmi_calc(self, weight, height_feet, height_inch, bmi, category):
        driver = self.driver
        time.sleep(4)
        weight_field = driver.find_element(By.CLASS_NAME, "bmi-weight")
        weight_field.clear()
        weight_field.send_keys(weight)
        time.sleep(4)
        height_field_feet = Select(
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bmi-height-feet"]'))))
        height_field_feet.select_by_value(str(height_feet))
        time.sleep(4)
        height_field_inches = Select(
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bmi-height-inches"]'))))
        height_field_inches.select_by_value(str(height_inch))

        bmi_label = driver.find_element(By.ID, "bmi-calculated-value")
        bmi_category_label = driver.find_element(By.ID, "bmi-calculated-category")
        time.sleep(4)
        self.assertEqual(bmi, float(bmi_label.text))
        self.assertEqual(category, bmi_category_label.text)
        time.sleep(4)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
