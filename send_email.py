from streamsqel import find_stock_price
below_lowest_messages = []  # Collect messages for stocks below the lowest price
above_highest_messages = []  # Collect messages for stocks above the highest price
for row in rows:
    id, ticker, exchange, highest_price, lowest_price = row
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    class1 = "YMlKec fxKbKc"
    found_element = soup.find(class_=class1)

    if found_element:
          try:
              price = float(found_element.text.strip()[1:].replace(",", ""))
          except ValueError:
              below_lowest_messages.append(f"Invalid price format for {ticker}:{exchange}")
              continue

            # Get current stock price and display it in the alert
    current_price_label = f" ({price})"
    if price > highest_price:    
          above_highest_messages.append(f"{ticker}:{exchange} is above the support price {highest_price}! (Current Price:{current_price_label})")

    if price < lowest_price:
        below_lowest_messages.append(f"{ticker}:{exchange} is below the support price {lowest_price}! (Current Price:{current_price_label})")

    else:
        below_lowest_messages.append(f"Could not find stock data for {ticker}:{exchange}")
import smtplib, ssl
import os


port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')
message = """\
Subject: STOCK HOLDING ALERT

{below_lowest_messages} /n
{above_highest_messages}
"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME,PASSWORD)
    server.sendmail(USERNAME,USERNAME,message)
    
    
