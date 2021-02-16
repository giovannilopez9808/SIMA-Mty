import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


class SIMA:
    def __init__(self, year_i, year_f, stations):
        self.year_i = year_i
        self.year_f = year_f
        self.years = [year for year in range(year_i, year_f+1)]
        self.stations = stations

    def read_data(self, file, path):
        self.data = pd.read_csv(path+file, index_col=0)
        for key in self.data.keys():
            if not key in self.stations:
                self.data = self.data.drop(key, 1)

    def calc_year_mean(self):
        self.year_mean = pd.DataFrame(index=self.years, columns=self.stations)
        for station in self.stations:
            for year in self.years:
                hour_f, hour_i = count_hours_per_year(
                    [year, 1, 1], [self.year_i, 1, 1])
                self.year_mean[station][year] = round(
                    self.data[station][hour_i:hour_f].mean(), 1)

    def calc_month_mean(self, station):
        self.month_mean = pd.DataFrame(columns=self.years,
                                       index=[i for i in range(12)])
        for year in self.years:
            for month in range(1, 13):
                hour_f, hour_i = count_hours_per_month(date_f=[year, month, 1],
                                                       date_i=[self.year_i, 1, 1])
                self.month_mean[year][month - 1] = round(
                    self.data[station][hour_i:hour_f].mean(), 4)

    def calc_season_hour_mean(self, station):
        season_names = ["Spring Sum", "Summer Sum", "Autumn Sum", "Winter Sum",
                        "Spring Count", "Summer Count", "Autumn Count", "Winter Count"]
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        seasons_dates = {'Summer': (datetime.date(2020, 6, 21), datetime.date(2020, 9, 22)),
                         'Autumn': (datetime.date(2020, 9, 23), datetime.date(2020, 12, 20)),
                         'Spring': (datetime.date(2020, 3, 21), datetime.date(2020, 6, 20))}
        season_count = pd.DataFrame(
            columns=season_names, index=np.arange(24))
        season_count = season_count.fillna(0)
        total_days = count_days(date_i=[self.year_i, 1, 1], date_f=[
                                self.year_f, 12, 31])
        for hour in range(24):
            sum = 0
            count = 0
            for year in range(self.year_f-self.year_i+1):
                for day in range(365):
                    date = consecutiveday2date(day, 2020)
                    season_name = get_season(date, seasons_dates)
                    hour_value = (year*365+day)*24+hour
                    value = self.data[station][hour_value]
                    if str(value) != "nan":
                        season_count[season_name+" Sum"][hour] += value
                        season_count[season_name+" Count"][hour] += 1
        self.season_hourly_mean = pd.DataFrame(
            columns=seasons, index=np.arange(24))
        for season in seasons:
            for hour in range(24):
                self.season_hourly_mean[season][hour] = round(
                    season_count[season+" Sum"][hour]/season_count[season+" Count"][hour], 1)

    def calc_day_mean(self, station):
        self.day_mean = pd.DataFrame(index=self.years, columns=[
                                     i for i in range(365)])
        for year in self.years:
            for day in range(365):
                month = obtain_month(year, day)
                hour_f, hour_i = count_hours_per_month(date_f=[year, month, 1],
                                                       date_i=[self.year_i, 1, 1])
                self.day_mean[day][year] = round(
                    self.data[station][hour_i:hour_f].mean(), 1)

    def plot_month_means(self):
        choose_months = np.arange(1, 11, 3)
        choose_months = np.append(choose_months, 12)
        month_names = obtain_month_names(choose_months)
        fig, axs = plt.subplots(
            2, 3, sharex=True, sharey=True, figsize=(10, 12))
        plt.subplots_adjust(left=0.083, right=0.95, top=0.926)
        axs = np.reshape(axs, 6)
        for year, ax in zip(self.years, axs):
            ax.set_ylabel("PM$_{10}$", fontsize=12)
            ax.set_xticks(choose_months)
            ax.set_xticklabels(month_names, rotation=45, fontsize=12)
            ax.set_xlim(1, 12)
            ax.set_ylim(0, 120)
            ax.set_title("Year: {}".format(year))
            ax.grid(ls="--", color="grey", alpha=0.5, lw=2)
            ax.plot(np.arange(1, 13),
                    self.month_mean[year], ls="--", color="green", lw=3, marker="o")

        plt.show()

    def plot_season_means(self):
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        xticks = np.arange(0, 22, 2)
        xticks = np.append(xticks, 23)
        plt.xlim(0, 23)
        plt.xticks(xticks)
        plt.ylim(30, 100)
        plt.xlabel("Local Time (h)")
        plt.ylabel("PM$_{10}$", fontsize=12)
        for season in seasons:
            plt.plot(self.season_hourly_mean[season], label=season)
        plt.legend(frameon=False, ncol=4, mode="expand",
                   bbox_to_anchor=(0, 1.07, 1, 0.02))
        plt.grid(ls="--", color="grey", alpha=0.5, lw=2)
        plt.show()
    
    def cut_year(self,date_i,date_f):
        self.data.index = pd.to_datetime(self.data.index)
        self.section = self.data.loc[ (self.data.index >= date_i) & 
                                            (self.data.index <= date_f) ]

def count_days(date_i, date_f):
    year, month, day = date_f
    year_i, month_i, day_i = date_i
    days = (datetime.date(year, month, day) -
            datetime.date(year_i, month_i, day_i)).days
    return days


def count_hours_per_year(date_f, date_i):
    year, month, day = date_f
    year_i, month_i, day_i = date_i
    hour_i = count_days(date_i=[year_i, month_i, day_i],
                        date_f=[year, month, day])*24
    hour_f = hour_i+count_days(date_i=[year, month, day],
                               date_f=[year+1, month, day])*24+1
    return hour_f, hour_i


def count_hours_per_month(date_f, date_i):
    year, month, day = date_f
    year_i, month_i, day_i = date_i
    hour_i = count_days(date_i=[year_i, month_i, day_i],
                        date_f=[year, month, day])*24
    year_f, month_f = validate_date(date=[year, month])
    hour_f = hour_i+count_days(date_i=[year, month, day],
                               date_f=[year_f, month_f, day])*24+1
    return hour_f, hour_i


def validate_date(date):
    year, month = date
    month += 1
    if month > 12:
        month = 1
        year += 1
    return year, month


def obtain_month(year, day):
    month = (datetime.date(year, 1, 1) +
             datetime.timedelta(days=day)).month
    return month


def obtain_month_names(months):
    names = []
    for month in months:
        date = datetime.date(2020, month, 1)
        names.append(date.strftime("%b"))
    return names


def get_season(date, seasons):
    for season, (season_start, season_end) in seasons.items():
        if date >= season_start and date <= season_end:
            return season
    else:
        return 'Winter'


def consecutiveday2date(conse_day, year):
    date = datetime.date(year, 1, 1)+datetime.timedelta(days=conse_day)
    return date
