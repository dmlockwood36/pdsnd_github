import time
import pandas as pd
import numpy as np
import math

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

#week_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
#month_val = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def time_convert(hour_val):
    if hour_val >= 1 and hour_val < 12:
        time_12h = str(hour_val) + ":00 A.M."
    if hour_val == 0:
        time_12h =  "12:00 A.M."
    if hour_val >= 12 and hour_val < 23:
        time_12h =  str(hour_val) + ":00 P.M."

    return time_12h


def get_filters():
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\033[1m' + 'Hello! Let\'s explore some US bikeshare data!')
    print('\033[0m')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('\nEnter city name (Chicago, New York City, or Washington): ')
            city = city.title()
       
        except ValueError:
            print("Please enter a correct value for city")
            continue
        else:
            if city not in ('Chicago','New York City','Washington'):
                print('{} is not a valid choice for city name.'.format(city))
                continue
            else:
                break

    # get user input for month (all, January, February, March ... , june)
    while True:
        try:
            month = input('\nEnter month (All, January, February, March, April, May, June): ')
            month = month.title()
        except ValueError:
            print('\nPlease enter a correct value for month')
            continue
        else:
            if month not in ('January','February','March','April','May','June','All'):
                print('{} is not one of the possible choices for month.'.format(month))
                continue
            else:
                break

    # get user input for day of week (all, Monday, Tuesday, ... Sunday)
    while True:
        try:
            day = input('\nEnter day (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ')
            day = day.title()
        except ValueError:
            print('\nPlease enter a correct value for the day of the week.')
            continue
        else:
            if day not in ('All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'):
                print('{} is not one of the possible choices for the day of the week.'.format(day))
                continue
            else:
                break

    print('-'*40)
    return city, month, day

def view_summary(city, month, day):

    print('\nYou selected bikeshare data for the following (City : {}, Month : {}, Weekday : {}).'.format(city,month,day))

def view_data(df):

    view_data_yn = ''
    a = 0
    b = 9
    str_var = 'the first'

    while view_data_yn != 'No':
        try:
            view_data_yn = input('\nWould you like to view ' + str_var + ' 10 rows of the bikeshare you selected? (yes, no) ')
            view_data_yn = view_data_yn.title()
        except ValueError:
            print('\nPlease enter either yes or no.')
            continue
        else:
            if view_data_yn not in ('Yes','No'):
                print('{} is not one of the possible choices. Please select either yes or no.'.format(view_data_yn))
                continue
            if view_data_yn == 'Yes':
                print('\n')
                print(df.iloc[a:b,])
                a += 10
                b += 10
                str_var = 'an additional' #change the context of the message
                continue
            if view_data_yn == 'No':
                break
            else:
                break

def load_data(city, month, day):

    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    df['Start_Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start_Time'].dt.month_name()
    df['DOW'] = df['Start_Time'].dt.day_name()

    if month != "All":
        df = df[df["Month"] == month]

    if day != "All":
        df = df[df["DOW"] == day]

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    

    # display the most common month

    # df['month'] = df['Start_Time'].dt.month
    popular_month = df['Month'].mode()[0]
    print("The most popular month is: " + popular_month)

    # display the most common day of week

    popular_dow = df['DOW'].mode()[0]
    print("The most popular day of week is: " + popular_dow)

    # display the most common start hour

    df['hour'] = df['Start_Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular hour is: " + time_convert(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is: " + popular_start_station)

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end station is: " + popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + " / " + df['End Station']
    popular_route = df['Route'].mode()[0]
    print("The most popular route is: " + popular_route)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_days = math.floor(total_travel_time / 86400)
    total_hours = math.floor((total_travel_time % 86400)/3600)
    total_minutes = math.floor(((total_travel_time % 86400) % 3600) / 60)
    total_seconds = math.floor(((total_travel_time % 86400) % 3600) % 60) 

    print("Total time used for bikeshare travel for the selected criteria is: " 
        + str(total_days) + " Days " + str(total_hours) + " Hours " + str(total_minutes) + " Minutes " 
        + str(total_seconds) + " Seconds (" + str(total_travel_time) + ") Seconds.")

    # display mean travel time
    avg_travel_time = round(df['Trip Duration'].mean(),2)
    print('\nThe mean travel time for the selected criteria is: ' + str(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_val = df['User Type'].value_counts()
    print(user_val)
    print('\n')

    # Display counts of gender
    if city != 'Washington':
        gender_val = df['Gender'].value_counts()
        print(gender_val)
        print('\n')

    # Display earliest, most recent, and most common year of birth
    if city != 'Washington':
        earliest_birth_year = df['Birth Year'].min()
        print("The earliest year of birth is: " + str(int(earliest_birth_year)))

        recent_birth_year = df['Birth Year'].max()
        print("The most recent year of birth is: " + str(int(recent_birth_year)))

        common_birth_year = df['Birth Year'].mode()[0]
        print("The most common year of birth is: " + str(int(common_birth_year)))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_summary(city, month, day)
        view_data(df)
        time_stats(df)
        input("Press enter to continue.")
        station_stats(df)
        input("Press enter to continue.")
        trip_duration_stats(df)
        input("Press enter to continue.")
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
