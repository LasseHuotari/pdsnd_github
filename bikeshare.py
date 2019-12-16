import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
   
    #
    city = None
    month = None
    day = None
    

    while city not in ['chicago','new york city', 'washington']:
        city = input("What city you want to select, Chicago, New York City or Washington? ").lower()
        
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = int(input("Please select a month by number (1=January, 2=February ... 12=December, 13=all): "))
            break
        except ValueError:
            print("Give proper month.")
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    while True:
        try:
            day = int(input("Please select a day of the wekk by number (1=Sunday, 2=Monday ... 7=Saturday, 8=all): "))
            break
        except ValueError:
            print("Give proper day.")

    print('-'*40)

    print("your values were: ", city, " " ,str(month), " " ,str(day))

    print("Your city was: ", city)
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
        
    file_name = city.replace(" ","_") + ".csv"
    
    df = pd.read_csv(file_name)
    
    df['startdate'] = pd.to_datetime(df['Start Time'], format="%Y-%m-%d %H:%M:%S")
    df['enddate'] = pd.to_datetime(df['End Time'], format="%Y-%m-%d")
    
    if day != 8 and month != 13:
        df = monthfilter(month, df)
        df = dayfilter(day, df)
        
    elif day == 8 and month != 13:
        df = monthfilter(month, df)
        
    elif month == 13 and day != 8:
        df = dayfilter(day, df)
        
 
    return df


def time_stats(df):
    df.head()
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    
    for i,r in df['startdate'].dt.month.value_counts().head(1).items():
        print("most common month was: ", i, " counts ", r)

    # TO DO: display the most common day of week
    
    for i,r in df['startdate'].dt.dayofweek.value_counts().head(1).items():
        print("most common day of week was: ", i, " counts ", r)

    # TO DO: display the most common start hour

    for i,r in df['startdate'].dt.hour.value_counts().head(1).items():
        print("most common start hour was: ", i, " counts ", r)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    
    # Print the most commonly used start stations by taking value counts, sort them, take the first row and print value name and value count
    for i,r in df['Start Station'].value_counts().sort_values(ascending = False).head(1).items():
        print("most common start station was: ", i, ", counts ", r)

    
    # Print the most commonly used end stations by taking value counts, sort them, take the first row and print value name and value count
    for i,r in df['End Station'].value_counts().sort_values(ascending = False).head(1).items():
        print("most common end station was: ", i, ", counts ", r)

    # Print the most frequent start/end station combination by using combiner, taking value counts, sort them, take the first row and print value name and value count
   
    kind = 1
    col1, col2, output = 'Start Station', 'End Station', 'Route'
    
    combiner(kind, df, col1, col2, output)
    
    for i,r in df['Route'].value_counts().sort_values(ascending = False).head(1).items():
        print("most common route combination was: ", i, ", counts ", r)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Displaying total travel time by using combiner function and taking timedelta value from sum time and extracting time values from timedelta values with timehandler function.
    kind = 3
    col1, col2, output = 'enddate', 'startdate', 'traveltime'
    
    combiner(kind, df, col1, col2, output)
    timedelta = df['traveltime'].sum()
    
    days, hours, mins, seconds = timehandler(timedelta)
    print("Total travel time was: ", days, " days ", hours, " hours ", mins, " minutes", seconds, " seconds")

    
    #Displaying average travel time by calculating average and taking timedelta value from sum time and extracting time values from timedelta values with timehandler function.
    timedelta = df['traveltime'].sum() / len(df['traveltime'])
   
    days, hours, mins, seconds = timehandler(timedelta)
    print("Average travel time was: ", days, " days ", hours, " hours ", mins, " minutes ", round(seconds, 1), " seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying user types counts by using value_counter function
    colname = 'User Type'
    counted_values = value_counter(colname, df)
    
    print("Counts for user types are:\n\n", counted_values)

    # Displaying genders counts by using value_counter function, and city is New York City or Chicago
    if city == "new_york_city" or city == "chicago":
        colname = 'Gender'
        counted_values = value_counter(colname, df)

        print("\nCounts for genders are:\n\n", counted_values)
    
        # Displaying earliest, most recent and most common year of birth
        print("\nEarliet birth year is: ", round(df['Birth Year'].min(),0))
    
    
        print("Most recent birth year is: ", round(df['Birth Year'].max(),0))
    
        for i,r in df['Birth Year'].value_counts().head(1).items():
            print("Most common birth year is: ", round(i,0))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def dayfilter(day,df):
    """
    Filter a dataset based on specified day of the week.

    Args:
        df - Pandas dataframe where to filter
        (int) day - day of the week that is used as a filter
    Return:
        df - filtered Pandas dataframe
    """
    df = df[df['startdate'].dt.dayofweek == int(day)]
    
    return df

def monthfilter(month,df):
    """
    Filter a dataset based on specified month.

    Args:
        df - Pandas dataframe where to filter
        (int) month - number of month that is used as a filter
    Return:
        df - filtered Pandas dataframe
    """
    df = df[df['startdate'].dt.month == int(month)]
    
    return df

def combiner(kind, df, col1, col2, output):
    """
    Function to do subraction, addition and string combination operations between two columns

    Args:
        df - Pandas dataframe where to filter
        (int) kind - number that specifies wanted operation (1 for string combination, 2 for addition and 3 for substraction)
        (str) col1 - Variable name that is used in operations as first variable
        (str) col2 - Variable name that is used in operations as second variable
        (str) output - Name for output column
    Return:
        df - Pandas dataframe with new operated column
    """
    if kind == 1:
        df[output] = df[col1] + " , " + df[col2]
        
    elif kind == 2:
        df[output] = df[col1] + df[col2]
        
    elif kind == 3:
        df[output] = df[col1] - df[col2]
    
    return df

def timehandler(timedelta):
    """
    Function to do subraction, addition and string combination operations between two columns

    Args:
        (datetime) timedelta - Time Delta value from where other time values are extracted
    Return:
        (int) days - Sum of whole days were in time delta value
        (int) hours - Sum of whole hours were in time delta value
        (int) mins - Sum of whole mins were in time delta value
        (float) mins - Sum of whole senconds were in time delta value
    """
    
    days = timedelta.days
    hours = timedelta.seconds // 3600
    wholehours = timedelta.seconds / 3600
    exactmins = (wholehours - hours) * 60
    mins = timedelta.seconds // 60 % 60
    exactsecs = (exactmins - mins) * 60
    
    if hours == 0:
        seconds = (timedelta.seconds / 60 - mins) * 60
    else:
        seconds = round(exactsecs,2)
    
    return days, hours, mins, seconds


def value_counter(colname, df):
    """
    Function to count value counts in given column

    Args:
        (str) colname - Column name from where the value counts are counted
        df - Pandas dataframe where that column is
    Return:
        counted_values - Pandas dataframe that has value counts
    """
    
    counted_values = df[colname].value_counts().sort_values(ascending=False).to_frame()
    
    return counted_values
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    

if __name__ == "__main__":
	main()

