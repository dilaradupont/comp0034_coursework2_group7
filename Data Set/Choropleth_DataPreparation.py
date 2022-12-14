"""
Python file created for the reorganization of the database as a starting point for the page with choropleth map and bar
chart. Using melt and pivot to combine and switch columns with rows
"""
import pandas as pd

df = pd.read_csv('DBJoint.csv')

df = df[df['Urban Code'].isnull()]
df = df.drop(columns=['Currency Unit', 'Indicator Code'])

df = df.melt({'Country Name', 'Country Code', 'Urban Code', 'Urban Area Name', 'Region', 'Income Group',
              'Indicator Name'}, value_name='Score', var_name='Year')

df = df[['Country Name', 'Country Code', 'Urban Code', 'Urban Area Name', 'Region', 'Income Group', 'Year',
         'Indicator Name',
         'Score']]

df = df.pivot(index={'Country Name', 'Country Code', 'Urban Code', 'Urban Area Name', 'Region', 'Income Group', 'Year'},
              columns='Indicator Name', values='Score')
df = df.reset_index()

df = df[['Country Name', 'Country Code', 'Urban Area Name', 'Urban Code', 'Region', 'Income Group', 'Year',
         'Starting a business - Score', 'Starting a business: Cost - Men (% of income per capita)',
         'Starting a business: Cost - Men (% of income per capita) - Score',
         'Starting a business: Cost - Women (% of income per capita)',
         'Starting a business: Cost - Women (% of income per capita) - Score',
         'Starting a business: Minimum capital (% of income per capita)',
         'Starting a business: Paid-in Minimum capital (% of income per capita) - Score',
         'Starting a business: Procedures required - Men (number)',
         'Starting a business: Procedures required - Men (number) - Score',
         'Starting a business: Procedures required - Women (number)',
         'Starting a business: Procedures required - Women (number) - Score',
         'Starting a business: Time - Men (days)', 'Starting a business: Time - Men (days) - Score',
         'Starting a business: Time - Women (days)',
         'Starting a business: Time - Women (days)- Score']]

df['Starting a business: Cost - Average (% of income per capita) - Score'] = df[
    ['Starting a business: Cost - Men (% of income per capita) - Score',
     'Starting a business: Cost - Women (% of income per capita) - Score']].mean(axis=1)

df['Starting a business: Procedures required - Average (number) - Score'] = df[
    ['Starting a business: Procedures required - Men (number) - Score',
     'Starting a business: Procedures required - Women (number) - Score']].mean(axis=1)

df['Starting a business: Time - Average (days) - Score'] = df[['Starting a business: Time - Women (days)- Score',
                                                               'Starting a business: Time - Men (days) - Score']].mean(
    axis=1)

df = df.drop(columns=['Starting a business: Cost - Men (% of income per capita)',
                      'Starting a business: Cost - Men (% of income per capita) - Score',
                      'Starting a business: Cost - Women (% of income per capita)',
                      'Starting a business: Cost - Women (% of income per capita) - Score',
                      'Starting a business: Minimum capital (% of income per capita)',
                      'Starting a business: Procedures required - Men (number)',
                      'Starting a business: Procedures required - Men (number) - Score',
                      'Starting a business: Procedures required - Women (number)',
                      'Starting a business: Procedures required - Women (number) - Score',
                      'Starting a business: Time - Men (days)', 'Starting a business: Time - Men (days) - Score',
                      'Starting a business: Time - Women (days)',
                      'Starting a business: Time - Women (days)- Score', 'Urban Area Name', 'Urban Code'])

df = df[['Country Name', 'Country Code', 'Region', 'Income Group', 'Year',
         'Starting a business - Score', 'Starting a business: Cost - Average (% of income per capita) - Score',
         'Starting a business: Procedures required - Average (number) - Score',
         'Starting a business: Time - Average (days) - Score',
         'Starting a business: Paid-in Minimum capital (% of income per capita) - Score']]

df = df.sort_values('Year')
df.to_csv('DBresorted_cm.csv', index=False)
