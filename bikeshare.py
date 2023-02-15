import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'Bike_Share_project/chicago.csv',
              'new york city': 'Bike_Share_project/new_york_city.csv',
              'washington': 'Bike_Share_project/washington.csv' }

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('available options: (chicago, new york city, washington)')
    citys = ('chicago','new york city','washington')
    while True:  
            city = input('Please, enter a city:')
            if city.lower() in citys:
                print("Thank you!")
                break
            else:
                print("Sorry, I didn't understand that,try again")
                continue
            


    # get user input for month (all, january, february, ... , june)
    print('available options: (all, january, february, ... , june)')
    months = ('all','january', 'february', 'march','april','may','june')
    while True:  
            month = input('Please, enter a month:')
            if month.lower() in months:
                print("Thank you!")
                break
            else:
                print("Sorry, I didn't understand that,try again")
                continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('available options: (all, monday, tuesday, ... sunday)')
    days = ('all','monday', 'tuesday', 'wednesday','thursday','friday','saturday','sunday')
    while True:  
            day = input('Enter a day:')
            if day.lower() in days:
                print("Thank you!")
                break
            else:
                print("Sorry, I didn't understand that,try again")
                continue

    print('-'*40)
    print(city, month, day)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month

    month = df['month'].mode()[0]
    print("\nThe most common month is: {}".format(calendar.month_name[month]))
    # display the most common day of week


    day_of_week = df['day_of_week'].mode()[0]
    print("\nThe most common day of the week is: {}".format(day_of_week))
    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most popular start hour is: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('\nMost commonly used start station...{}\n'.format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\nMost commonly used end station...{}\n'.format(end_station))

    # display most frequent combination of start station and end station trip
    combo_stations = df.groupby(['Start Station','End Station']).size().idxmax()
    print('\nMost commonly used station combination...{}\n'.format(combo_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    diff = abs(df['Start Time'] - df['End Time']).sum()
    print('Total travel time...{}'.format(diff))

    # display mean travel time
    diff = abs(df['Start Time'] - df['End Time']).mean()
    print('Mean travel time...{}'.format(diff))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns :
        user_types = df['User Type'].value_counts()
        print('Number of user types...\n{}'.format(user_types))
    else:
        print('User type data not present')
    

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print('Number of genders...\n{}'.format(gender_types))
    else:
        print('Gender data not present')

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns :
        earliest = min(df['Birth Year'])
        print("\nThe earliest year of birth is...{}".format(earliest))

        most_recent = max(df['Birth Year'])
        print("\nThe recent year of birth is...{}".format(most_recent))
        most_common = df['Birth Year'].mode()[0]
        print("\nThe most common year of birth is...{}".format(most_common))
    else:
        print('Birth Year data not present')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df): 
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')

    while view_data.lower() == 'yes':
        print(df.sample(5))
        
        view_data = input("Do you wish to continue?: ")
        if view_data.lower() != 'yes':
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
