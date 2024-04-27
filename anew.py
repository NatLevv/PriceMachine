import os
import pandas as pd
class PriceMachine:
    def __init__(self, folder_path):
        self.all_data = {
            'наименование': [],
            'цена': [],
            'вес': [],
            'файл': [],
            'цена за кг': []
        }
        self.folder_path = folder_path

    def load_prices(self):
        for i in range(8):
            filename = f"price_{i}.csv"
            if os.path.exists(filename):
                df = pd.read_csv(filename, delimiter=',')
                an_columns = list(df.columns)
                for column in an_columns:
                    if column in ("название", "продукт", "товар", "наименование"):
                        self.all_data['наименование'] += list(df[column])
                for column in an_columns:
                    if column in ("цена", "розница"):
                        self.all_data['цена'] += list(df[column])
                for column in an_columns:
                    if column in ("фасовка", "масса", "вес"):
                        self.all_data['вес'] += list(df[column])
                        self.all_data['файл'] += [filename for _ in range(len(list(df[column])))]
                        self.all_data['цена за кг'] = [round(self.all_data['цена'][i] / self.all_data['вес'][i], 2) for i in
                                                       range(len(self.all_data['цена']))]

        #print(self.all_data)

        self.main_df = pd.DataFrame(self.all_data)
        self.main_df = self.main_df.sort_values(by=['цена за кг'])
        #print(self.main_df)
        return self.main_df
        #print(main_df)


    def export_to_html(self, filename='output.html'):
        html_table = self.main_df.to_html(index=False)
        with open(filename, 'w') as f:
            f.write(html_table)
        print(f"Данные успешно сохранены в файл: {filename}")

    def find_text(self, search_term):
        #main_df = self.load_prices()
        found_rows = []
        for index, row in self.main_df.iterrows():
            #print(row['наименование'])
            if search_term in row['наименование'].split(' '):
                found_rows.append(row)
        found_df = pd.DataFrame(found_rows)
        #print(found_df)
        return found_df



if __name__ == "__main__":
    price_machine = PriceMachine('.')
    price_machine.load_prices()
    #print(main_df)

    while True:
        search_term = input("Введите фрагмент названия товара для поиска (для выхода введите 'exit'): ")
        price_machine.export_to_html()
        if search_term.lower() == "exit":
            print("Программа завершена.")
            break
        else:
            found_items = price_machine.find_text(search_term)
            if found_items.empty:
                print("Товар не найден.")
            else:
                print("Найденные товары:")
                print(found_items)