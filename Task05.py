import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, f_oneway, ttest_ind

# Function to load the dataset
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

# Function to display basic data information
def display_basic_info(df):
    print(df.head())
    print(df.shape)
    print(df.isnull().sum())
    df = df.dropna()
    print(df.isnull().sum())
    print(df.info())
    return df

# Function to display and plot the counts of different columns
def display_and_plot_counts(df, column, n=30):
    print(df[column].value_counts())
    sns.countplot(y=column, data=df[:n])
    plt.show()

# Function to convert Start_Time to datetime and create additional columns
def process_datetime(df):
    df.Start_Time = pd.to_datetime(df.Start_Time, format='mixed')
    df['start_day'] = df.Start_Time.dt.day
    df['start_hr'] = df.Start_Time.dt.time
    df['start_date'] = df.Start_Time.dt.date
    return df

# Function to analyze time-based accident data
def analyze_time_of_accident(df):
    time_of_accident = df.start_hr.value_counts()
    time_of_accident_high = time_of_accident[time_of_accident >= 1000]
    time_of_accident_low = time_of_accident[time_of_accident < 1000]
    print(time_of_accident_high, '\n', time_of_accident_low)
    time_of_accident_high[:20].plot(kind='barh')
    plt.show()

# Function to display and plot accident severity
def analyze_severity(df):
    print(df["Severity"].value_counts())
    sns.countplot(x="Severity", data=df)
    plt.show()

# Function to drop unnecessary columns
def drop_columns(df, columns):
    df.drop(columns=columns, axis=1, inplace=True)
    return df

# Function to plot histograms of geographic data
def plot_geographic_data(df):
    sns.histplot(data=df["Start_Lat"][:200], kde=True)
    plt.show()
    sns.histplot(data=df["Start_Lng"][:200], kde=True, color="navy")
    plt.show()
    sns.histplot(data=df["End_Lat"][:200], kde=True, color="brown")
    plt.show()
    sns.histplot(data=df["End_Lng"][:200], kde=True, color="orange")
    plt.show()

# Function to plot histograms of various features
def plot_histograms(df):
    sns.histplot(data=df["Distance(mi)"][:200], kde=True, color="green")
    plt.show()
    sns.histplot(data=df["Humidity(%)"], kde=True)
    plt.show()

# Function to plot pie charts for categorical features
def plot_pie_charts(df):
    fig, ((ax1, ax2, ax3), (ax4, ax5, _)) = plt.subplots(2, 3, figsize=(18, 12))
    colors = ['#ff9999', '#66b3ff']
    explode = (0.2, 0,)

    features = ['Station', 'Stop', 'Traffic_Calming', 'Traffic_Signal', 'Sunrise_Sunset']
    labels = [[True, False], [True, False], [True, False], [True, False], ['Night', 'Day']]

    for ax, feature, label in zip([ax1, ax2, ax3, ax4, ax5], features, labels):
        val1 = len(df[df[feature] == label[0]])
        val2 = len(df[df[feature] == label[1]])
        ax.set_title(feature)
        ax.pie([val1, val2], labels=label, autopct='%1.1f%%', explode=explode, shadow=True, colors=colors)

    fig.delaxes(_)
    plt.tight_layout()
    plt.show()

# Function to test statistical hypotheses
def test_hypotheses(df):
    alpha = 0.05

    # Hypothesis 1: Day/Night and accident severity
    contingency_table = pd.crosstab(df['Sunrise_Sunset'], df['Severity'])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    print('p-value:', p)
    print("The following null hypothesis is", p > alpha, ": There is no statistically significant relationship between the Day/Night and accident severity.")

    # Hypothesis 2: Severity across different times of day
    morning_severity = df[(df.Start_Time.dt.hour >= 0) & (df.Start_Time.dt.hour < 6)]['Severity']
    afternoon_severity = df[(df.Start_Time.dt.hour >= 6) & (df.Start_Time.dt.hour < 12)]['Severity']
    evening_severity = df[(df.Start_Time.dt.hour >= 12) & (df.Start_Time.dt.hour < 18)]['Severity']
    night_severity = df[(df.Start_Time.dt.hour >= 18)]['Severity']
    f_statistic, p = f_oneway(morning_severity, afternoon_severity, evening_severity, night_severity)
    print('p-value:', p)
    print("The following null hypothesis is", p > alpha, ": There is no statistically significant difference in the severity of accidents across different times of day.")

    # Hypothesis 3: Severity across different weather conditions
    feature_categories = df['Weather_Condition'].unique()
    data = [df[df['Weather_Condition'] == category]['Severity'] for category in feature_categories]
    _, p = f_oneway(*data)
    print('p-value:', p)
    print("The following null hypothesis is", p > alpha, ": There is no statistically significant difference in the severity of accidents across different weather conditions.")

    # Hypothesis 4: Severity between hot and cold weather
    df['Severity'] = pd.to_numeric(df['Severity'], errors='coerce')
    hot_weather = df[df['Temperature(F)'] > 90]['Severity']
    cold_weather = df[df['Temperature(F)'] < 32]['Severity']
    t_stat, p = ttest_ind(hot_weather, cold_weather, equal_var=False)
    print('p-value:', p)
    print("The following null hypothesis is", p > alpha, ": There is no significant difference in accident severity between hot and cold weather.")

# Main function to execute all steps
def main():
    filepath = "US_Accidents_March23.csv"
    df = load_data(filepath)
    df = display_basic_info(df)
    display_and_plot_counts(df, "Weather_Timestamp")
    display_and_plot_counts(df, "City")
    df = process_datetime(df)
    analyze_time_of_accident(df)
    analyze_severity(df)
    df = drop_columns(df, ["ID"])
    plot_geographic_data(df)
    plot_histograms(df)
    plot_pie_charts(df)
    test_hypotheses(df)

if __name__ == "__main__":
    main()
