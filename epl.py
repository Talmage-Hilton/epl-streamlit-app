import pandas as pd
import plotly.express as px
import streamlit as st


st.title('English Premier League Players')
st.caption("Welcome to a web app to explore information about the top 250 English Premier League players! You may interact with everything on the app. Look around, stay a while, and enjoy!")

st.header("Description")
st.caption("I am a huge fan of the EPL. I love soccer and staying up to date with the transfer talks throughout the season. This fascination has led me to wonder about how much certain players are worth for owners. A player's Estimated Transfer Value (ETV) is roughly how much a club would have to pay for a player if they were to purchase them in the transfer window. I web scraped this dataset in hopes of finding answers about ETV, as well as other variables, such as a player's skill level, potential, and position. With this dataset, and through this web app, I am hoping to find answers to the following EDA questions:")
st.caption("    * Which position has the highest average skill level among players?")
st.caption("    * What is the relationship between skill level and ETV among players?")
st.caption("    * How does the ETV vary across different positions?")

st.caption("Using this web app, I can find the answers to these questions, as well as more. Have your own fun and start finding answers to your own questions!")
st.caption('    * Defenders, surprisingly enough, have the highest average skill level among players. You can find this by selecting General Position as the X variable and Skill Level as the Y variable under the "Choose Your Own Adventure" tab.')
st.caption("    * Skill Level and ETV have a correlation coefficient of 0.66. This indicates a fairly strong, positive, linear relationship between Skill and ETV. You can find this answer for yourself by looking at the Correlation Matrix under the third tab.")
st.caption('    * Forwards have the highest average ETV, followed by midfielders, defenders, and goalkeepers. You can find this by selecting General Position as the X variable and ETV as the Y variable under the "Choose Your Own Adventure" tab.')

df = pd.read_csv('epl_players.csv')


# Customize the names for the selectbox options
variable_names = {
    'position': 'Specific Position',
    'general_position': 'General Position',
    'skill': 'Skill Level',
    'pot': 'Potential Level',
    'etv': 'Estimated Transfer Value'
}

# Create a reverse dictionary to map display names to column names
reverse_variable_names = {
    'Specific Position': 'position',
    'General Position': 'general_position',
    'Skill Level': 'skill',
    'Potential Level': 'pot',
    'Estimated Transfer Value': 'etv'
}


tab1, tab2, tab3 = st.tabs(['Player vs. Player', 'Choose Your Own Adventure', 'Correlation Matrix'])


with tab1:
    st.subheader("Player Comparison")
    st.caption("Choose two players and the variable to compare between them!")

    player1 = st.selectbox('Select First Player', df['name'])
    player2 = st.selectbox('Select Second Player', df['name'])
    numeric_variables = ['skill', 'pot', 'etv']
    variable = st.selectbox('Select Variable to Compare', [variable_names[key] for key in numeric_variables])

    column_name = reverse_variable_names[variable]

    # Plot comparison
    player1_value = df[df['name'] == player1][column_name].values[0]
    player2_value = df[df['name'] == player2][column_name].values[0]

    data = {
        'Player': [player1, player2],
        variable: [player1_value, player2_value]
    }
    fig_comparison = px.bar(data, x='Player', y=variable, color='Player', labels={'Player': 'Player', variable: variable}, title=f'{player1} vs {player2} - {variable} Comparison')
    st.plotly_chart(fig_comparison)



with tab2:
    st.subheader("Choose Your Own Adventure")
    st.caption("Choose any two variables to compare. If both variables are quantitative, a scatterplot will show the relationship between the two. If the first variable is categorical (either Specific Position or General Postition), a bar chart will appear showing the average (mean) numeric variable for each position.")

    x_variable = st.selectbox('Select X-Axis Variable', [variable_names[key] for key in variable_names.keys()])
    
    # Filter numeric variables for y_variable selectbox
    numeric_variables = ['Skill Level', 'Potential Level', 'Estimated Transfer Value']
    y_variable = st.selectbox('Select Y-Axis Variable', numeric_variables)
    
    if x_variable in ['Specific Position', 'General Position']:  # Check if x-axis variable is categorical
        if y_variable:  # Check if y-axis variable is selected
            x_column = reverse_variable_names[x_variable]  # Map x_variable to column name in the DataFrame
            y_column = reverse_variable_names[y_variable]  # Map y_variable to column name in the DataFrame
            chart_data = df.groupby(x_column)[y_column].mean().reset_index()
            fig = px.bar(chart_data, x=x_column, y=y_column, labels={x_column: x_variable, y_column: y_variable}, title=f'{y_variable} by {x_variable}')
            st.plotly_chart(fig)
        else:
            st.write("Please select a numeric variable for the Y-Axis.")
    else:
        if x_variable != y_variable:  # Ensure x and y variables are not the same
            x_label = x_variable
            y_label = y_variable
            x_column = reverse_variable_names[x_variable]  # Map x_variable to column name in the DataFrame
            y_column = reverse_variable_names[y_variable]  # Map y_variable to column name in the DataFrame
            fig = px.scatter(df, x=x_column, y=y_column, hover_data=['name', 'etv', 'pot', 'general_position'], labels={x_column: x_label, y_column: y_label})
            st.plotly_chart(fig)
        else:
            st.write("Please select different variables for X-Axis and Y-Axis.")

    with st.expander("See explanation"):
        if x_variable in ['Specific Position', 'General Position']:
            st.write(f"The figure above shows the average (mean) {y_variable} for each {x_variable}.")
        else:
            st.write(f"The figure above shows a scatter plot of {x_variable} against {y_variable}.")



with tab3:
    df_copy = df.iloc[:, [4, 5, 6]].copy()
    # Calculate correlation matrix
    corr_matrix = df_copy.corr()
    # Create heatmap
    fig_cor = px.imshow(corr_matrix,
                        labels=dict(x="Variables", y="Variables", color="Correlation"),
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        color_continuous_scale='YlGnBu',
                        zmin=-1, zmax=1)
    # Add annotations
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            fig_cor.add_annotation(x=i, y=j, text=f"{corr_matrix.iloc[i, j]:.2f}",
                                   showarrow=False, font=dict(color='white'))
    # Update layout
    fig_cor.update_layout(title='Correlation Matrix', xaxis_title='', yaxis_title='')
    st.plotly_chart(fig_cor)
    with st.expander("See explanation"):
        st.write("The matrix above shows the correlation between each numeric variable in the data set!")



with st.sidebar:
    selected_player = st.sidebar.selectbox('Select a Player', df['name'])

    player_stats = df[df['name'] == selected_player].squeeze()

    st.write(f"## {selected_player}'s Stats")
    st.write(f"**Position:** {player_stats['general_position']}")
    st.write(f"**Skill:** {player_stats['skill']}")
    st.write(f"**Potential:** {player_stats['pot']}")
    st.write(f"**ETV:** {player_stats['etv']}")