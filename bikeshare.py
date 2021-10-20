import time
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
from datetime import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['january','february','march','april','may','june']
DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
FILTER_DATA = ['month', 'day', 'both', 'none']

def get_month():
    """ 
    This function is used to get months from the user that can be filtered for in the data frame 
    
    Returns:
    (str) month - returns string if all months must be used OR
    (list) month - the list of months used to filter the data 

    """
    months = []
    while True:
        month = str(input("Which month/s would you like to filter for? (blank is all months) (Seperate with a comma) [January, February, March, April, May, June]\n").lower().strip()).split(",")

        if month[0].strip() == "":
            month = "all"
            break
        else:
            for i in month:
                if i.strip() in MONTH_DATA:
                    months.append(i.strip())
                else:
                    print("There is a problem with entry: {}. Please type the months again.".format(i.title()))
                    months = []
                    break
        if len(months) != 0:
            break
            
    if month == 'all':
        print("Great! you chose all months\n")
    else:
        month = months
        
        if len(month) == 6:
            print("Great! you chose all months\n")
            month = 'all'
        else:
            print("Great! the months you chose are: {}\n".format(" and ".join(month)))
            for i in range(0,len(month)):
                month[i] = MONTH_DATA.index(month[i])+1

    return month

def get_day():
    """ 
    This function is used to get days from the user that can be filtered for in the data frame
   
     Returns:
     (str) month - returns string if all days must be used OR
    (list) day - the list of days used to filter the data 
    """
    days = []
    while True:
        day = str(input("Which day/s would you like to filter for? (blank is all days) (Seperate with a comma) [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]\n").lower().strip()).split(",")

        if day[0].strip() == "":
            day = "all"
            break
        else:
            for i in day:
                if i.strip() in DAY_DATA:
                    days.append(i.strip())
                else:
                    print("There is a problem with entry: {}. Please type the months again.".format(i.title()))
                    days = []
                    break
        if len(days) != 0:
            break
    if day == 'all':
        print("Great! you chose all days\n")
    else:
        day = days
        if len(day) == 7:
            day = 'all'
            print("Great! you chose all days\n")
        else:
            print("Great! the days you chose are: {}\n".format(" and ".join(day)))   
            for i in range(0, len(day)):
               day[i] = day[i].title()
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!\n\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("Which city would you like to analyse? Chicago, New York City, Washington\n")).lower().strip()
        if CITY_DATA.get(city):
            break
        else:
            match = 0
            city_guess = ""
            for key in CITY_DATA:
                match_new = SequenceMatcher(None, key, city).ratio()
                if match_new > match:
                    match = match_new
                    city_guess = key
            if match > 0.5:
                confirm_guess = input("That does not seem quite right, did you mean: '{}'? Enter yes or no.\n".format(city_guess.title())).lower()
                if confirm_guess == "yes":
                    city = city_guess
                    break
                else:
                    print("It seems that is not an available option. Please type the city name again")
            else:            
                print("It seems that is not an available option. Please type the city name again")
    print("\nGreat! you chose: {}\n".format(city.title()))

    # get filter information from the user
    # This function has 'guess' functionality. This will evaluate the user input according to correct inputs and make suggestions if typos are encountered.
    while True:
        user_filter = str(input("Would you like to apply a filter? Please type month, day, both or none\n")).lower().strip()
        if user_filter in FILTER_DATA:
            break
        else:
            match = 0
            filter_guess = ""
            for key in FILTER_DATA:
                match_new = SequenceMatcher(None, key, user_filter).ratio()
                if match_new > match:
                    match = match_new
                    filter_guess = key
            if match > 0.5:
                confirm_guess = input("That does not seem quite right, did you mean: '{}'? Enter yes or no.\n".format(filter_guess.title())).lower()
                if confirm_guess == "yes":
                    user_filter = filter_guess
                    break
                else:
                    print("It seems that is not an available option. Please type the filter again")
            else:            
                print("It seems that is not an available option. Please type the filter again")

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if user_filter.lower().strip() == 'none':
        print("No filter will be applied\n")
        month = 'all'
        day = 'all'
    elif user_filter.lower().strip() == 'both':
        month = get_month()
        day = get_day()
    elif user_filter.lower().strip() == 'month':
        month = get_month()
        day = 'all'
    elif user_filter.lower().strip() == 'day':
        day = get_day()
        month = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    try:
        df['day_of_week'] = df['Start Time'].dt.day_name() # version issue
    except:
        df['day_of_week'] = df['Start Time'].dt.weekday_name() # version issue
    df['start_hour'] = df['Start Time'].dt.hour
    df['route_combo'] = df['Start Station'] + "|" + df['End Station']

    # Filter Month
    if month != 'all':
        if len(month) == 1:
            df = df.loc[(df['month'] == month[0])]
        elif len(month) == 2:
            df = df.loc[(df['month'] == month[0]) | (df['month'] == month[1])]
        elif len(month) == 3:
            df = df.loc[(df['month'] == month[0]) | (df['month'] == month[1]) | (df['month'] == month[2])]
        elif len(month) == 4:
            df = df.loc[(df['month'] == month[0]) | (df['month'] == month[1]) | (df['month'] == month[2]) | (df['month'] == month[3])]
        elif len(month) == 5:
            df = df.loc[(df['month'] == month[0]) | (df['month'] == month[1]) | (df['month'] == month[2]) | (df['month'] == month[3]) | (df['month'] == month[4])]
    # Filter Day
    if day != 'all':
        if len(day) == 1:
            df = df.loc[df['day_of_week'] == day[0]]
        elif len(day) == 2:
            df = df.loc[(df['day_of_week'] == day[0]) | (df['day_of_week'] == day[1])]
        elif len(day) == 3:
            df = df.loc[(df['day_of_week'] == day[0]) | (df['day_of_week'] == day[1]) | (df['day_of_week'] == day[2])]
        elif len(day) == 4:
            df = df.loc[(df['day_of_week'] == day[0]) | (df['day_of_week'] == day[1]) | (df['day_of_week'] == day[2]) | (df['day_of_week'] == day[3])]
        elif len(day) == 5:
            df = df.loc[(df['day_of_week'] == day[0]) | (df['day_of_week'] == day[1]) | (df['day_of_week'] == day[2]) | (df['day_of_week'] == day[3]) | (df['day_of_week'] == day[4])]
        elif len(day) == 6:
            df = df.loc[(df['day_of_week'] == day[0]) | (df['day_of_week'] == day[1]) | (df['day_of_week'] == day[2]) | (df['day_of_week'] == day[3]) | (df['day_of_week'] == day[4]) | (df['day_of_week'] == day[5])]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("    The most common month in the extracted data is: {}".format(MONTH_DATA[df['month'].mode().get(0)-1].title()))

    # display the most common day of week
    print("    The most common day of the week is: {}".format(df['day_of_week'].mode().get(0)))

    # display the most common start hour
    print("    The most common start hour is: {}:00".format(df['start_hour'].mode().get(0)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("    The most common start station is: {}".format(df['Start Station'].mode().get(0)))

    # display most commonly used end station
    print("    The most common end station is: {}".format(df['End Station'].mode().get(0)))

    # display most frequent combination of start station and end station trip
    print("    The most common combination of start and end point is: '{}' to '{}'".format(df['route_combo'].mode().get(0).split("|")[0],df['route_combo'].mode().get(0).split("|")[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("    The total travel time is: {} minutes".format(np.sum(df['Trip Duration'])))

    # display mean travel time
    print("    The average travel time is: {} minutes".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("    The counts for the different users are: ")
    for val in pd.unique(df['User Type']):
        if str(val) != 'nan':
            print("{}    {}".format(val, df['User Type'].value_counts().get(val)))
    print("\n")

    # Display counts of gender
    print("    The counts for the different genders are: ")
    for val in pd.unique(df['Gender']):
        if str(val) != 'nan':
            print("{}    {}".format(val, df['Gender'].value_counts().get(val)))
    print("\n")

    # Display earliest, most recent, and most common year of birth
    if (datetime.now().year-round(df['Birth Year'].min())) > 100:
        print("    The earliest year of birth was extracted as {} but this seems a bit unlikely.".format(round(df['Birth Year'].min())))
    else:
        print("    The oldest person using the service was born in: {} [Current Age: {}]".format(round(df['Birth Year'].min()),datetime.now().year-round(df['Birth Year'].min())))
    print("    The youngest person using the service was born in: {} [Current Age: {}]".format(round(df['Birth Year'].max()),datetime.now().year-round(df['Birth Year'].max())))
    print("    The average birth year is: {} [Current Age: {}]".format(round(df['Birth Year'].mean()),datetime.now().year-round(df['Birth Year'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """
    Main function where funtions are called from
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
    
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city == "washington":
            print("Whoops! In this release there are no user statistics available for {}".format(city.title()))
        else:
            user_stats(df)

        row_count = 0
        amount_raw_rows = 5
        while True:
            if row_count < len(df.index)-(amount_raw_rows+1):
                if row_count == 0:
                    trip_data = str(input("Would you like to view {} rows of raw trip data? Enter yes or no.\n".format(amount_raw_rows))).lower()
                else:
                    trip_data = str(input("Would you like to view another {} rows of raw trip data? Enter yes or no.\n".format(amount_raw_rows))).lower()
                if trip_data == "yes":
                    if (row_count+amount_raw_rows) < len(df.index)-1:
                        for i in range(row_count,row_count+amount_raw_rows):
                            print("\n{}\n".format(df.loc[row_count]))
                    else:
                        print("There are no more rows left.")
                    row_count+=amount_raw_rows
                else:
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
