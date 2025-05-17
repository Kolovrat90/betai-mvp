from data_collector import FootballDataCollector

def main():
    # Инициализация коллектора данных
    collector = FootballDataCollector()
    
    # Определение параметров сбора данных
    countries = ['England', 'Spain', 'Germany', 'Italy', 'France']
    seasons = [2021, 2022, 2023]
    
    print("Начинаем сбор данных для следующих стран:", countries)
    print("Сезоны:", seasons)
    
    # Запуск сбора данных
    collector.collect_data_for_leagues(countries, seasons, include_statistics=True)
    
    print("Сбор данных завершен!")

if __name__ == "__main__":
    main()
