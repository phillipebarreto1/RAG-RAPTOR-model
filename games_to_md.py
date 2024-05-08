import requests
import json

def get_api_data(endpoint, headers, params=None):
    base_url = "https://api-nba-v1.p.rapidapi.com"
    response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code} {response.text}")
        return None

def json_to_markdown(data):
    markdown_content = "# NBA Games Data\n\n"
    if 'response' in data and data['response']:
        games = data['response']
        for game in games:
            home_team = game['teams']['home']['name']
            away_team = game['teams']['visitors']['name']
            home_points = game['scores']['home'].get('points')
            away_points = game['scores']['visitors'].get('points')

            # Convert points to integers if possible, else set to None
            home_points = int(home_points) if home_points is not None else None
            away_points = int(away_points) if away_points is not None else None

            # Safely get quarter scores
            home_scores = game['scores']['home']
            away_scores = game['scores']['visitors']
            # Ensure quarter scores are extracted correctly
            homeQ1 = game['scores']['home']['linescore'][0] if len(game['scores']['home']['linescore']) > 0 else 'N/A'
            homeQ2 = game['scores']['home']['linescore'][1] if len(game['scores']['home']['linescore']) > 1 else 'N/A'
            homeQ3 = game['scores']['home']['linescore'][2] if len(game['scores']['home']['linescore']) > 2 else 'N/A'
            homeQ4 = game['scores']['home']['linescore'][3] if len(game['scores']['home']['linescore']) > 3 else 'N/A'
            awayQ1 = game['scores']['visitors']['linescore'][0] if len(game['scores']['visitors']['linescore']) > 0 else 'N/A'
            awayQ2 = game['scores']['visitors']['linescore'][1] if len(game['scores']['visitors']['linescore']) > 1 else 'N/A'
            awayQ3 = game['scores']['visitors']['linescore'][2] if len(game['scores']['visitors']['linescore']) > 2 else 'N/A'
            awayQ4 = game['scores']['visitors']['linescore'][3] if len(game['scores']['visitors']['linescore']) > 3 else 'N/A'

            # Determine the winning team, ensuring no comparison is made if points are None
            if home_points is not None and away_points is not None:
                winning_team = home_team if home_points > away_points else away_team
            else:
                winning_team = "Undetermined"

            markdown_content += f"**Date:** {game['date']}  \n"
            markdown_content += f"**Home Team:** {home_team}  \n"
            markdown_content += f"**Away Team:** {away_team}  \n"
            markdown_content += f"**Home Points:** {home_points if home_points is not None else 'N/A'}  \n"
            markdown_content += f"**Away Points:** {away_points if away_points is not None else 'N/A'}  \n"
            markdown_content += f"**Home Q1:** {homeQ1}, **Home Q2:** {homeQ2}, **Home Q3:** {homeQ3}, **Home Q4:** {homeQ4}  \n"
            markdown_content += f"**Away Q1:** {awayQ1}, **Away Q2:** {awayQ2}, **Away Q3:** {awayQ3}, **Away Q4:** {awayQ4}  \n"
            markdown_content += f"**Winning Team:** {winning_team}  \n"
            markdown_content += "\n---\n\n"  # Markdown for a horizontal rule as a break
    else:
        markdown_content += "No game data available.\n"
    return markdown_content

def save_to_markdown(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def main():
    headers = {
        "X-RapidAPI-Key": "08564dfb67msh82741cd0b6a650dp17b6b5jsn25d43c03ab6d",
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    
    # Use correct parameter names as per API
    games_params = {"season": "2023"}  # Adjust this if necessary
    games = get_api_data("games", headers, games_params)
    
    markdown_content = json_to_markdown(games if games else {"response": []})
    save_to_markdown("data/nba_data.md", markdown_content)

if __name__ == "__main__":
    main()
