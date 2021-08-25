from bs4 import BeautifulSoup
import requests
import smtplib
import os

MY_EMAIL = os.environ.get("EMAIL")
MY_PASS = os.environ.get("EMAIL_PASS")
SEND_TO = os.environ.get("SEND_TO")
AMAZON_LINK = "https://www.amazon.nl/dp/B085K45C3S/ref=gw_nl_desk_other_aucc_brw_kif?pf_rd_r=GXBBKW4X40AXEMDTX8SQ&pf_rd_p=ab22ae0b-434f-4a07-a370-381eb9351cb2&pd_rd_r=2fd55521-34f2-4fce-831f-32838cec6c04&pd_rd_w=M2qzQ&pd_rd_wg=9hBMQ&ref_=pd_gw_unk"

headers = {
    "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

response = requests.get(AMAZON_LINK, headers=headers)
html_page = response.text

soup = BeautifulSoup(html_page, "lxml")
price = soup.find(name="span", id="price_inside_buybox").getText()
price_number = price.strip("\n€\xa0\n")
price_format = price_number.replace(",", ".")
price_float = float(price_format)
print(price_float)
item_name = soup.find(name="span", id="productTitle").getText()
item_format = item_name.rstrip("\n")
item_format = item_format.lstrip("\n")

if price_float < 100.00:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=SEND_TO,
            msg=f"subject:Amazon price tracker\n\n"
                f"{item_format}\nPrice is now {price_number} euro"
        )
else:
    print("Not today buddy")