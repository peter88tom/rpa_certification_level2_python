
"""
In this robot we will teach the robot how for process the order
1. I has to save the order HTML receipt as a PDF file
2. Saves the screenshot of the ordered robot.
3. Embeds the screenshot of the robot to the PDF receipt
4. Create a ZIP archive of the receipts and images.
"""
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
import time

browser = Selenium()

url = "https://robotsparebinindustries.com/#/robot-order"
data_url = "https://robotsparebinindustries.com/orders.csv"

def open_the_robot_orders_web():
    """ Open a browser and vist the order application """
    browser.open_available_browser(url)
    

def get_orders():
    """ 
        Get order excel file from the remote server
        - Will use RPA.HTTP library to download the file.
        - We will have to overwrite the downloaded file if exist by using the keyword overwrite=True
    """
    http = HTTP()
    http.download(url=data_url, overwrite=True)



def close_the_annoying_modal():
    """ Close the modal pop up after open the robot web """
    modal_button = browser.find_element("css:button.btn-dark")
    browser.click_button(modal_button)




def fill_the_form():
    pass



def download_and_store_the_excle_file():
    pass



def archive_out_put():
    pass



def main():
    try:
        open_the_robot_orders_web()
        close_the_annoying_modal()
        get_orders()
    finally:
        time.sleep(30)
        browser.close_all_browsers()

if __name__ == "__main__":
    main()
