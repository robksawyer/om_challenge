# Ordermark Challenge
# Parse input HTML file and respond with formatted JSON
from bs4 import BeautifulSoup
from flask import jsonify, json
import re

def parse():
    inputHTML = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">

    <html>

       <head>

          <title>

             Order Email

          </title>

       </head>

       <body style="font-size:15px;">

          <div id="cust_service_info" style="font-weight:bold; font-size:125%;">

             Order 99250207-8683267

          </div>

          <table style="width:400px;">

             <tr>

                <td>

                   Deliver to:

                </td>

             </tr>

             <tr>

                <td>

                   James Bond

                </td>

             </tr>

          </table>

          <div style="display:none; display: none !important;" data-section="order-data">

             <div data-section="diner">

                <div data-field="phone">

                   (555) 555-1212

                </div>

             </div>

             <div data-section="menu-item">

                <div data-field="menu-item-name" menu-item-id="434">

                   Wings

                </div>

                <div data-field="quantity">

                   1

                </div>

                <div data-field="price">

                   $8.99

                </div>

             </div>

             <div data-section="menu-item">

                <div data-field="menu-item-name" menu-item-id="123">

                   Mozzarella Sticks

                </div>

                <div data-field="quantity">

                   1

                </div>

                <div data-field="price">

                   $6.49

                </div>

             </div>

             <div data-section="menu-item">

                <div data-field="menu-item-name" menu-item-id="12">

                   Pepperoni Pizza

                </div>

                <div data-field="quantity">

                   1

                </div>

                <div data-field="price">

                   $17.00

                </div>

             </div>

             <div data-section="menu-item">

                <div data-field="menu-item-name" menu-item-id="54">

                   Garlic Knots

                </div>

                <div data-field="quantity">

                   1

                </div>

                <div data-field="price">

                   $2.99

                </div>

             </div>

             <div data-section="restaurant">

                <div data-field="restaurant-name">

                   Food Is Tasty

                </div>

             </div>

          </div>

       </body>

    </html>


    --000000000000339e91056cf80d96
    Content-Type: application/json; name="parsing_o
    """

    version = 1
    print(f'Ordermark challenge version {version}')

    soup = BeautifulSoup(inputHTML, "html5lib")

    # DOM parsing variables
    customerTable = soup.find('table')
    customerTableRows = customerTable.find_all('tr')
    customerName = customerTableRows[1].text.strip()
    customerPhone = soup.find('div', attrs={'data-field': 'phone'}).text.strip()

    # Customer order
    customerServiceInfo = soup.find('div', id='cust_service_info').text.strip()

    # Menu items
    menuItems = soup.find_all('div', attrs={'data-section': 'menu-item'})
    # Menu attributes
    menuItemIdAttr = 'menu-item-id'
    menuItemNameAttr = {'data-field': 'menu-item-name'}
    menuItemPriceAttr = {'data-field': 'price'}
    menuItemQuantityAttr = {'data-field': 'quantity'}

    # Restaurant details
    restaurant = soup.find('div', attrs={'data-section': 'restaurant'})
    restaurantName = restaurant.find('div', attrs={'data-field': 'restaurant-name'}).text.strip()

    # Overview of the response schema
    jsonData = {
        'customer': {},
        'customer_order_id': "",
        'menu_items': [],
        'restaurant': {}
        }

    # Add customer service info
    cCustomerServiceInfo = re.sub('Order ', '',customerServiceInfo)
    jsonData['customer_order_id'] = cCustomerServiceInfo

    # Add basic customer details
    jsonData['customer'] = {
        "name": customerName,
        "phone": customerPhone
    }

    # Handle collecting menu items
    for item in menuItems:
        tId = item.findAll('div')[0].attrs[menuItemIdAttr]
        tName = item.find('div', attrs=menuItemNameAttr).text.strip()
        tPrice = item.find('div', attrs=menuItemPriceAttr).text.strip()
        cPrice = re.sub('[^0-9.]','', tPrice)
        tQuantity = item.find('div', attrs=menuItemQuantityAttr).text.strip()
        jsonData['menu_items'].append({
            'id': int(tId),
            'item_name': tName,
            'price': float(cPrice),
            'quantity': int(tQuantity),
        })

    # Sort menu items
    jsonData['menu_items'] = sorted(jsonData['menu_items'], key=lambda k: k['id'])

    # Restaurant details
    jsonData['restaurant'] = {
        'restaurant_name': restaurantName
    }

    print(json.dumps(jsonData, indent=2))

parse()
