# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:12:13 2021

@author: yaron
"""
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import cv2

class youTubeController():
    #initialiser gets username and password(default is my new google accoun)
    #sets the driver
    def __init__(self, username="",
                       password= "" ):
        self.username= username
        self.password= password
        '''
        if chromdriver is not in your path. Please enter its location here in the brackets
        '''
        self.driver = webdriver.Chrome()
        
    #opens youstube and signs in with the username and password 
    #provided with the initialiser
    def openYoutube(self, maxWindow = True):

        try:self.driver.get("https://www.youtube.com/feed/library")
        except: print ("cannot find page")
        try:self.driver.set_window_size(640,720)
        except: print ("cannot set size")

        #login button
        try:
            login = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a/tp-yt-paper-button"))
                )
        except: print ("cannot find login button")
        else:
            login.click()
            print("login clicked")
            
            #email
            try:    user = WebDriverWait(self.driver, 2).until(
                         EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")))

            except: print("cannot fint username input")
            else:
                user.send_keys(self.username)
                user.send_keys(Keys.RETURN)
                #password
                try:        passW = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")))
                except: print('cannot find password input')
                else:
                    time.sleep(1)
                    passW.send_keys(self.password)
                    passW.send_keys(Keys.RETURN)
                    
        if maxWindow:self.driver.maximize_window()

    #click voice search button 
    # we need to check how to give it permisiions 
    def voiceSearch(self):
    
        try:
            WebDriverWait(self.driver, 0).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/div/ytd-button-renderer/a/yt-icon-button/button/yt-icon"))
                ).click()
        
        except:
            print("voice search error")

    #scrolls down
    def scroll(self):
        try:
            WebDriverWait(self.driver, 0).until(
                EC.presence_of_element_located((By.TAG_NAME, "html"))
                ).send_keys(Keys.PAGE_DOWN)
        except: print("cannot scroll")
      
    #clicks next video button on an open video
    def nextSong(self):
        try:
            WebDriverWait(self.driver, 1).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-next-button.ytp-button"))
             ).click()
            
        except: print("next song error")
        
    def select(self):
        videos = self.driver.find_elements(By.ID, 'video-title')
        try: videos[0].click()
        except: print("cannot click")
        
    def play(self):
        try:
            WebDriverWait(self.driver, 1).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button"))
             ).click()
            
        except: print("cannot click")
        
    def getScreen(self, width,height):
        self.driver.save_screenshot('a.png')
        screen = cv2.imread('a.png')
        screen = cv2.resize(screen,(width,height))
        return screen
    
    def posClick(self, x,y):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(self.driver.find_element_by_tag_name('html'), x,y).click().perform()
            
            
    def waitForPageToLoad(self,width,height, TO=10):
        #WebDriverWait(self.driver,TO).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#movie_player > div.html5-video-container > video")))
        
        try:WebDriverWait(self.driver,TO).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#movie_player > div.html5-video-container > video")))
        except: return    
        else:
            try:WebDriverWait(self.driver,TO).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                
            #self.driver.implicitly_wait(25)
            except: return
            else:
                time.sleep(1)
                
                print("loaded")
                return self.getScreen(width, height)
            
    def ping(self):
        return self.driver.current_url
        
        
        