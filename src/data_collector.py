import os
import json
import time
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime

class FootballDataCollector:
    def __init__(self, api_key_path='api_key.txt'):
        # Загрузка API-ключа из файла
        with open(api_key_path, 'r') as f:
            self.api_key = f.read().strip()
        
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-apisports-key': self.api_key
        }
        
        # Создаем директорию для данных, если она не существует
        os.makedirs('data', exist_ok=True)
    
    def _make_request(self, endpoint, params=None):
        """Выполнить запрос к API с обработкой ошибок и ограничений"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # Проверка на ошибки HTTP
            
            # Проверяем статус API-запроса
            data = response.json()
            
            # Добавляем задержку, чтобы не превысить лимит запросов
            time.sleep(0.5)
            
            return data
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к {url}: {e}")
            return None
    
    def get_leagues(self, country=None):
        """Получить список лиг"""
        params = {}
        if country:
            params['country'] = country
        
        data = self._make_request('leagues', params)
        
        if data and 'response' in data:
            leagues = []
            for item in data['response']:
                league = {
                    'league_id': item['league']['id'],
                    'name': item['league']['name'],
                    'type': item['league']['type'],
                    'country': item['country']['name'],
                    'country_code': item['country']['code'],
                    'season': item['seasons'][-1]['year'] if item['seasons'] else None
                }
                leagues.append(league)
            
            # Сохраняем данные в CSV
            leagues_df = pd.DataFrame(leagues)
            leagues_df.to_csv('data/leagues.csv', index=False)
            print(f"Сохранено {len(leagues)} лиг в data/leagues.csv")
            
            return leagues_df
        return None
    
    def get_teams(self, league_id, season):
        """Получить команды для указанной лиги и сезона"""
        params = {
            'league': league_id,
            'season': season
        }
        
        data = self._make_request('teams', params)
        
        if data and 'response' in data:
            teams = []
            for item in data['response']:
                team = {
                    'team_id': item['team']['id'],
                    'name': item['team']['name'],
                    'code': item['team']['code'],
                    'country': item['team']['country'],
                    'founded': item['team']['founded'],
                    'logo': item['team']['logo'],
                    'league_id': league_id,
                    'season': season
                }
                teams.append(team)
            
            # Сохраняем данные в CSV
            filename = f'data/teams_league_{league_id}_season_{season}.csv'
            teams_df = pd.DataFrame(teams)
            teams_df.to_csv(filename, index=False)
            print(f"Сохранено {len(teams)} команд в {filename}")
            
            return teams_df
        return None
    
    def get_fixtures(self, league_id, season, status='FT'):
        """Получить матчи для указанной лиги и сезона"""
        params = {
            'league': league_id,
            'season': season
        }
        
        if status:
            params['status'] = status  # FT = finished matches
        
        data = self._make_request('fixtures', params)
        
        if data and 'response' in data:
            fixtures = []
            for item in data['response']:
                fixture = {
                    'fixture_id': item['fixture']['id'],
                    'date': item['fixture']['date'],
                    'timestamp': item['fixture']['timestamp'],
                    'venue': item['fixture']['venue']['name'] if item['fixture']['venue'] else None,
                    'status': item['fixture']['status']['short'],
                    'league_id': item['league']['id'],
                    'season': item['league']['season'],
                    'round': item['league']['round'],
                    'home_team_id': item['teams']['home']['id'],
                    'home_team': item['teams']['home']['name'],
                    'away_team_id': item['teams']['away']['id'],
                    'away_team': item['teams']['away']['name'],
                    'home_goals': item['goals']['home'],
                    'away_goals': item['goals']['away'],
                    'home_halftime_goals': item['score']['halftime']['home'],
                    'away_halftime_goals': item['score']['halftime']['away'],
                }
                fixtures.append(fixture)
            
            # Сохраняем данные в CSV
            filename = f'data/fixtures_league_{league_id}_season_{season}.csv'
            fixtures_df = pd.DataFrame(fixtures)
            fixtures_df.to_csv(filename, index=False)
            print(f"Сохранено {len(fixtures)} матчей в {filename}")
            
            return fixtures_df
        return None
    
    def get_fixture_statistics(self, fixture_id):
        """Получить статистику для конкретного матча"""
        params = {
            'fixture': fixture_id
        }
        
        data = self._make_request('fixtures/statistics', params)
        
        if data and 'response' in data:
            stats = []
            for team_stats in data['response']:
                team_id = team_stats['team']['id']
                team_name = team_stats['team']['name']
                
                for stat in team_stats['statistics']:
                    stat_entry = {
                        'fixture_id': fixture_id,
                        'team_id': team_id,
                        'team_name': team_name,
                        'stat_type': stat['type'],
                        'stat_value': stat['value']
                    }
                    stats.append(stat_entry)
            
            if stats:
                # Сохраняем данные в CSV
                filename = f'data/statistics_fixture_{fixture_id}.csv'
                stats_df = pd.DataFrame(stats)
                stats_df.to_csv(filename, index=False)
                print(f"Сохранена статистика для матча {fixture_id} в {filename}")
                
                return stats_df
        return None
    
    def collect_data_for_leagues(self, country_list, seasons, include_statistics=True):
        """Собрать данные для списка стран и сезонов"""
        all_leagues = []
        
        # Получаем лиги для каждой страны
        for country in country_list:
            print(f"Получение лиг для страны: {country}")
            leagues = self.get_leagues(country)
            if leagues is not None:
                all_leagues.append(leagues)
        
        if all_leagues:
            leagues_df = pd.concat(all_leagues)
            
            # Фильтруем только высшие лиги
            top_leagues = leagues_df[leagues_df['type'] == 'League'].copy()
            
            # Для каждой лиги и сезона собираем данные
            for _, league in tqdm(top_leagues.iterrows(), total=len(top_leagues), desc="Обработка лиг"):
                league_id = league['league_id']
                
                for season in seasons:
                    print(f"Обработка лиги {league['name']} ({league_id}), сезон {season}")
                    
                    # Получаем команды
                    self.get_teams(league_id, season)
                    
                    # Получаем матчи
                    fixtures_df = self.get_fixtures(league_id, season)
                    
                    # Получаем статистику для каждого матча
                    if include_statistics and fixtures_df is not None:
                        for fixture_id in tqdm(fixtures_df['fixture_id'], desc="Получение статистики матчей"):
                            self.get_fixture_statistics(fixture_id)
                            # Небольшая задержка, чтобы не превысить лимит запросов
                            time.sleep(1)

if __name__ == "__main__":
    # Пример использования
    collector = FootballDataCollector()
    
    # Собираем данные для топ-5 европейских лиг за последние 3 сезона
    countries = ['England', 'Spain', 'Germany', 'Italy', 'France']
    seasons = [2021, 2022, 2023]
    
    collector.collect_data_for_leagues(countries, seasons)
