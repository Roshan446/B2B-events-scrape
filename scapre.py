from bs4 import BeautifulSoup
import requests
import sys
import time
import json
sys.stdout.reconfigure(encoding='utf-8')

def find_events():
    data = requests.get("https://www.tradeindia.com/tradeshows/search.html?search_term=b2b")


    data_html = BeautifulSoup(data.text, "lxml")


    events_conatiner = data_html.find("div", class_ ="ti-container bx-brd-box")

    events_row = events_conatiner.find_all("div", class_="row")[1]

    event_card =events_row.find_all("div", class_ ="cardBox cardSec relative-div")

    info_list = []

    for r in event_card:
        event_name = r.find("p", class_="Typography__Body2R-sc-weqsjw-12 ThA-DK body1R twoLineShowText mb-2").a.text
        event_time = r.find("p", class_="Typography__Body3R-sc-weqsjw-13 eguDTo mb-2 p-color Body5R").text
        event_venue = r.find("a", class_ ="underlineNone").p.text
        event_country = r.find("span", class_ = "cityCountry").text
        event_info = r.find("span", class_ = "Typography__Body3R-sc-weqsjw-13 eguDTp p-color Body4R").text.strip("")
        event_more_info = r.find("div", class_ ="card-container").a["href"]
        event_website = r.find("div", class_="mb-2 mb-md-0 d-flex align-items-center")
        if event_website and event_website.a:
            event_website = event_website.a["href"]
        else:
            event_website = "No website"
        info_list.append({
            "Event":event_name,
            "Event date and time":event_time, 
            "event location":event_country,
            "venue":event_venue,
            "info": f"{event_info} at {event_more_info}",
            "website":event_website




        })
    with open("post/data.json", "w") as file:
        json.dump(info_list, file)
        print("file saved")
    print(info_list)


if __name__ == '__main__':
    while True:
        find_events()
        print("will get updated data every 10 minutes.. Please Wait..")

        time.sleep(600)

    




