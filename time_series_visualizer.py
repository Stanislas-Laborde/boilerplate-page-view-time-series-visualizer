import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date")
df.index = pd.to_datetime(df.index)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot

    # Set the figure size and plot style
    fig, ax = plt.subplots(figsize=(12, 9))
    plt.plot(df.index, df['value'], color='#D62728', linewidth=1)
    
    # Setting the title and labels
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Set the locator for the x-axis to display ticks every 6 months
    ax = plt.gca()  # Get the current Axes instance
    ax.xaxis.set_major_locator(MonthLocator(bymonth=(1, 7)))  # Set major ticks to January and July
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))  # Format the dates as "Year-Month"

    plt.close(fig)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Year"] = df_bar.index.year
    df_bar["Month"] = df_bar.index.month_name()
    df_bar = pd.DataFrame(df_bar.groupby(["Year", "Month"], sort=False)["value"].mean().round().astype(int))

    df_bar = df_bar.reset_index()
    df_bar = pd.concat([pd.DataFrame({
        "Year": [2016, 2016, 2016, 2016],
        "Month": ['January', 'February', 'March', 'April'],
        "value": [0, 0, 0, 0]
    }), df_bar])

    # Draw bar plot

    # Set the figure size and plot style
    fig, ax = plt.subplots(figsize=(12, 9))
    graph = sns.barplot(x='Year', y='value', data=df_bar, hue='Month', palette='bright', ax=ax)

    # Setting the labels
    ax.set_xlabel('Years')
    graph.set_xticklabels(graph.get_xticklabels(), rotation=90, horizontalalignment='center')
    ax.set_ylabel('Average Page Views')

    for text, label in zip(ax.legend(loc='upper left', title='Months').texts, ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September','October', 'November', 'December']):
        text.set_text(label)

    plt.close(fig)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    # Set the figure size
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(18, 6))

    # Year-wise Box Plot, Setting the title and labels
    sns.boxplot(x='year', y='value', data=df_box, palette="bright", ax=ax0)
    ax0.set_title('Year-wise Box Plot (Trend)')
    ax0.set_xlabel('Year')
    ax0.set_ylabel('Page Views')

    # Month-wise Box Plot, Setting the title and labels
    sns.boxplot(x='month', y='value', data=df_box, palette="husl", order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ax=ax1)
    ax1.set_title('Month-wise Box Plot (Seasonality)')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Page Views')

    # Adjust layout
    plt.tight_layout()

    plt.close(fig)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
