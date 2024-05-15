import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    frequent_categories = categories[categories >= cutoff].index    
    category_map = pd.Series(categories.index, index=categories.index)
    category_map = category_map.where(category_map.isin(frequent_categories), 'Other')
    return category_map.to_dict()


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public_2023.csv")    
    df = df[["Country", "Age", "EdLevel", "YearsCodePro", "Employment", "RemoteWork", "ConvertedCompYearly"]]       
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)
    
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != "Other"]
    
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df

# df = load_data()


def show_explore_page():
    st.title("Software Engineer Salaries 2023")   
    st.write("""### Stack Overflow Annual [Developer Survey](https://survey.stackoverflow.co/).""")

    df = load_data()
    
    # Distribution by Countries
    st.write("""#### Distribution by Countries:""")
    country = df["Country"].value_counts()
    labels = country.index
    values = country.values

    fig, axs = plt.subplots(1, 2, figsize=(20, 10))

    axs[0].bar(labels, values, width=0.7)
    axs[0].set_xticklabels(labels, rotation=90)
    axs[1].pie(values, labels=labels, autopct='%.0f%%', startangle=90)
    axs[1].axis('equal')
    
    st.pyplot(fig)    

    # Hybrid, Remote, or In-Person
    st.write("""#### Hibrid, Remote or In-Person:"""    )

    remote = df["RemoteWork"].value_counts()
    labels_remote = remote.index
    values_remote = remote.values

    fig1, ax1 = plt.subplots(1, 2, figsize=(20, 10))

    ax1[0].bar(labels_remote, values_remote, width=0.7)
    ax1[0].set_xticklabels(values_remote, rotation=90)
    ax1[1].pie(values_remote, labels=labels_remote, autopct='%.0f%%', startangle=90)
    ax1[1].axis('equal')
    st.pyplot(fig1)
    
    # Average Salary by Country
    st.write("""#### Average Salary by Country:""")
    salary_by_country = df.groupby("Country")["Salary"].mean().sort_values()
    st.bar_chart(salary_by_country)
    
    # # Salary by Age
    # st.write("""#### Salary by Age:""")
    # plt.figure(figsize=(20, 10))
    # ax = sns.histplot(data=df, x="Salary", hue="Age", kde=True, bins=30) <-- ERROR HERE
    # sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1)) 
    # st.pyplot(plt.gcf())
    # plt.clf()

    
    # # Salary by Education Level
    # st.write("""#### Salary by Education Level:""")
    # plt.figure(figsize=(20, 10))
    # ax = sns.histplot(data=df, x="Salary", hue="EdLevel", kde=True)  <-- ERROR HERE
    # sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    # st.pyplot(plt.gcf())
    # plt.clf()