import pandas as pd

def load_and_transform_data(filepath):
    data = pd.read_csv(filepath)
    column_mapping = {
        'Player': 'Player',
        'PTS': 'Points',
        'ORB': 'Offensive Rebounds',
        'DRB': 'Defensive Rebounds',
        'TRB': 'Total Rebounds',
        'AST': 'Assists',
        'STL': 'Steals',
        'BLK': 'Blocks',
        'TOV': 'Turnovers',
        '3P': 'Total 3s'
    }
    data = data[list(column_mapping.keys())].rename(columns=column_mapping)
    return data

def data_to_markdown(data):
    markdown_content = "# Player Statistics\n\n"
    for index, row in data.iterrows():
        markdown_content += f"**Player:** {row['Player']}  \n"
        markdown_content += f"**Points:** {row['Points']}  \n"
        markdown_content += f"**Offensive Rebounds:** {row['Offensive Rebounds']}  \n"
        markdown_content += f"**Defensive Rebounds:** {row['Defensive Rebounds']}  \n"
        markdown_content += f"**Total Rebounds:** {row['Total Rebounds']}  \n"
        markdown_content += f"**Assists:** {row['Assists']}  \n"
        markdown_content += f"**Steals:** {row['Steals']}  \n"
        markdown_content += f"**Blocks:** {row['Blocks']}  \n"
        markdown_content += f"**Turnovers:** {row['Turnovers']}  \n"
        markdown_content += f"**Total 3s:** {row['Total 3s']}  \n"
        markdown_content += "\n---\n\n"
    return markdown_content

def save_to_markdown(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def main():
    filepath = '/Users/phill/RAG-model/PlayerData.csv'
    transformed_data = load_and_transform_data(filepath)
    markdown_content2 = data_to_markdown(transformed_data)
    save_to_markdown("data/nba_data.md", markdown_content2)

if __name__ == "__main__":
    main()