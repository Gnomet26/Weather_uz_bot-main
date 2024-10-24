import requests
from bs4 import BeautifulSoup
from Sity_Dict import my_dict


class ObHavo:
    def __init__(self, sity):
        self.sity = my_dict[sity]

        self.base_url = f"https://obhavo.uz/{self.sity}"

        self.bugun_data = []
        self.haftalik_data = []
        self.day_help = []

        try:

            with requests.session() as ssesiya:
                base_data = ssesiya.request(method="GET", url=self.base_url)
                filter_data = BeautifulSoup(base_data.text, "html.parser")

                self.bugun_data.append(filter_data.find("div", class_="current-day").text)
                self.bugun_data.append(filter_data.find("div", class_="padd-block").find_all("span")[1].text)
                self.bugun_data.append(filter_data.find("div", class_="padd-block").find_all("span")[2].text)
                self.bugun_data.append(filter_data.find("div", class_="current-forecast-desc").text)

                for i in range(1, len(filter_data.find("table", class_="weather-table").find_all("tr"))):
                    self.day_help.append(filter_data.find("table", class_="weather-table").find_all("tr")[i].find("td",
                                                                                                                  class_="weather-row-day").find(
                        "strong").text)
                    self.day_help.append(filter_data.find("table", class_="weather-table").find_all("tr")[i].find("td",
                                                                                                                  class_="weather-row-day").find(
                        "div").text)
                    self.day_help.append(filter_data.find("table", class_="weather-table").find_all("tr")[i].find("td",
                                                                                                                  class_="weather-row-forecast").find(
                        "span", class_="forecast-day").text)
                    self.day_help.append(filter_data.find("table", class_="weather-table").find_all("tr")[i].find("td",
                                                                                                                  class_="weather-row-forecast").find(
                        "span", class_="forecast-night").text)
                    self.day_help.append(filter_data.find("table", class_="weather-table").find_all("tr")[i].find("td",
                                                                                                                  class_="weather-row-desc").text.replace(
                        " ", "").replace("\n", ""))
                    self.haftalik_data.append(self.day_help)
                    self.day_help = []


                ssesiya.close()

        except:
            self.bugun_data = ["Ma'lumot topilmadi"]
            self.haftalik_data = ["Ma'lumot topilmadi"]

    def get_today(self):
        return self.bugun_data

    def get_week(self):
        return self.haftalik_data

    def clear_all(self):
        self.bugun_data = []
        self.haftalik_data = []
