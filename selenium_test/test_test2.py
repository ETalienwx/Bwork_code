import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestUntitled():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_untitled(self):
    self.driver.get("http://dev-videostudio.bilibili.com/studio/before-effects")
    self.driver.set_window_size(1920, 1080)
    self.driver.find_element(By.CSS_SELECTOR, ".add_plus > img").click()
    self.driver.find_element(By.CSS_SELECTOR, ".alert-info").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(3)").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".empty-track-block")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".empty-track-block")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.CSS_SELECTOR, ".empty-track-block")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.CSS_SELECTOR, ".main-container").click()
    self.driver.find_element(By.CSS_SELECTOR, ".black-btn").click()
    self.driver.find_element(By.CSS_SELECTOR, ".alert-info").click()
    self.driver.find_element(By.CSS_SELECTOR, "label").click()
    self.driver.find_element(By.CSS_SELECTOR, ".alert-info").click()
  
