
"""
In this robot we will teach the robot how for process the order
1. I has to save the order HTML receipt as a PDF file
2. Saves the screenshot of the ordered robot.
3. Embeds the screenshot of the robot to the PDF receipt
4. Create a ZIP archive of the receipts and images.
"""
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Archive import Archive
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
    """ Close the modal pop up after open the robot order website """
    modal_button = browser.find_element("css:button.btn-dark")
    browser.click_button(modal_button)
 

def store_the_receipt_as_pdf_and_embed_the_robot(order_number):
    """ 
        Create a PDF receipt
        Documentation: https://robocorp.com/docs/libraries/rpa-framework/rpa-pdf/keywords#template-html-to-pdf
    """
    # Get the receipt element
    try:
        receipt_element = browser.find_element("css:div#receipt")
        pdf = PDF()
        pdf.html_to_pdf(receipt_element.get_attribute("outerHTML"), f"output/receipts/{order_number}.pdf")

        # take screenshot of the robot
        robot_screenshot = browser.find_element("css:div#robot-preview-image") 
        browser.screenshot(robot_screenshot, filename=f"output/receipts/{order_number}.png")
        
        # create new receipt pdf with both contents
        pdf.add_files_to_pdf(files=[f"output/receipts/{order_number}.pdf", 
                                     f"output/receipts/{order_number}.png"],
                                     target_document=f"output/receipts/{order_number}.pdf")
    except Exception as e:
        print(e)
        pass




def fill_the_form_and_submit(order):
    """ Fill in the order form """
    try:
        # Select the robot head
        robot_head = browser.find_element("//select[@id='head']")
        browser.select_from_list_by_value(robot_head, f"{order['Head']}")

        # Select the robot body
        # Documentation: https://robocorp.com/docs/libraries/rpa-framework/rpa-browser-selenium/keywords#select-radio-button
        browser.select_radio_button(group_name="body", value=f"{order['Body']}")

        # Fill the robot leg
        robot_legs = browser.find_element("//input[@type='number']")
        browser.input_text(robot_legs, order['Legs'])

        # Fill the shipping address
        shipping_address = browser.find_element("//input[@name='address']")
        browser.input_text(shipping_address, order['Address'])

        # Preview the ordered robot
        preview_robot = browser.find_element("//button[@id='preview']")
        browser.click_button(preview_robot)


        # Submit the order
        submit_order_button = browser.find_element("//button[@id='order']")
        browser.click_element(submit_order_button)

        #time.sleep(5)

        # Store the order receipt as a PDF and Emmbed the robot image to receipt PDF
        store_the_receipt_as_pdf_and_embed_the_robot(order_number=order['Order number']) 

        # Go back to s
        back_to_new_order = browser.find_element("//button[@id='order-another']")
        browser.click_button(back_to_new_order)

        # Close the annoying modal
        close_the_annoying_modal()

        time.sleep(3)        
    except:
        pass
    



def read_the_data_from_the_downloaded_excel_file():
    """ Read orders from the downloaded excel file and submit 
        Documentation:https://robocorp.com/docs/libraries/rpa-framework/rpa-tables
    """
    library = Tables()
    orders = library.read_table_from_csv("orders.csv")

    # Loop through the orders and submit each
    for order in orders:
       fill_the_form_and_submit(order)



def archive_out_put():
    """ 
        Create zip for the receipt folder 
        link to documentation https://robocorp.com/docs/libraries/rpa-framework/rpa-archive/keywords#archive-folder-with-zip
    """
    zipper = Archive()
    zipper.archive_folder_with_zip(folder="output/receipts", archive_name="receipt.zip")



def main():
    try:
        open_the_robot_orders_web()
        close_the_annoying_modal()
        get_orders()
        read_the_data_from_the_downloaded_excel_file()
        archive_out_put()
    finally:
        browser.close_all_browsers()

if __name__ == "__main__":
    main()
