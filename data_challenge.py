import pandas as pd
import numpy as np

class DataFrame:
    
    def __init__(self, input_file: str):
        self.df = pd.read_csv(input_file)
        self.modes = {}
        
        
    def get_mode(self, column: str) -> str:
        mode_series = self.df[column].dropna().mode()
        mode = mode_series.iloc[0] if not mode_series.empty else None
        
        return mode
    
    
    def get_average(self, column: str) -> float:
        average = pd.to_numeric(self.df[column], errors='coerce').dropna().mean()

        return  round(average, 2)
    
    
    def generate_output(self, output_file: str):
        self.df.to_csv(output_file, index=False)


    def normalize_seniority(self):
        
        COLUMN_NAME = 'Nivel_Senioridade'
        
        column = self.df[COLUMN_NAME]
        
        
        JUNIOR = 'Júnior'
        MIDLEVEL = 'Pleno'
        SENIOR = 'Sênior'

        replacement_map = {
            'Junior': JUNIOR,
            'junior': JUNIOR,
            'júnior': JUNIOR,
            'Jr': JUNIOR,
            'JR': JUNIOR,
            'Júnior': JUNIOR,
            'J': JUNIOR,
            'P': MIDLEVEL,
            'Pleno': MIDLEVEL,
            'pleno': MIDLEVEL,
            'PL': MIDLEVEL,
            'Mid-Level': MIDLEVEL,
            'Midlevel': MIDLEVEL,
            'Sênior': SENIOR,
            'sênior': SENIOR,
            'Senior': SENIOR,
            'senior': SENIOR,
            'Sr': SENIOR,
            'SR': SENIOR,
            'S': SENIOR,
        }

        mode = self.get_mode(COLUMN_NAME)

        self.df[COLUMN_NAME] = column.map(replacement_map).fillna(mode)

    def _normalize_rating(self, rating_column: str):
        column = self.df[rating_column]

        column = pd.to_numeric(column)

        average = self.get_average(rating_column)

        column = column.fillna(average)

        self.df[rating_column] = column
            
    def normalize_ratings(self):
        self._normalize_rating('Avaliacao_Tecnica')
        self._normalize_rating('Avaliacao_Comportamental')

    def normalize_engagement(self):
        COLUMN_NAME = 'Engajamento_PIGs'
        column = self.df[COLUMN_NAME]

        column = column.astype(str).str.rstrip('%')
        column = pd.to_numeric(column, errors='coerce')

        column = column / 100.0

        self.df[COLUMN_NAME] = column

        average = self.get_average(COLUMN_NAME)

        column = column.fillna(average)

        self.df[COLUMN_NAME] = column
        
    def _convert_to_comma(self, column_name: str):
        column = self.df[column_name]
        column = column.round(1)
        column = column.map(lambda x: '{:.1f}'.format(x)).astype(str).str.replace('.', ',')

        self.df[column_name] = column
        
    def convert_floating_values(self):
        self._convert_to_comma('Avaliacao_Tecnica')
        self._convert_to_comma('Avaliacao_Comportamental')
        self._convert_to_comma('Engajamento_PIGs')
        self._convert_to_comma('Score_Desempenho')

    def add_score_column(self):
        new_column_name = "Score_Desempenho"
        tech_rating = self.df['Avaliacao_Tecnica']
        behav_rating = self.df['Avaliacao_Comportamental']

        self.df[new_column_name] = round((tech_rating * 0.5) + (behav_rating * 0.5), 2)
        
    def add_status_column(self):
        new_column_name = "Status_Membro"
        
        value_map = {
            True: "Em Destaque",
            False: "Padrão",
        }
        
        engagement_column = self.df['Engajamento_PIGs']
        score_column = self.df['Score_Desempenho']
        
        self.df[new_column_name] = ((engagement_column >= 0.8) & (score_column >= 7.0)).map(value_map)
        
    def clean_data(self):
        
        self.normalize_seniority()
        self.normalize_ratings()
        self.add_score_column()
        self.normalize_engagement()
        self.add_status_column()
        self.convert_floating_values()
        
def main():
    input_file = 'Base_Membros_Desempenho - Base_Membros_Desempenho.csv'
    output_file = 'Base_Membros_Desempenho_Cleaned.csv'

    data_frame = DataFrame(input_file)
    
    data_frame.clean_data()
    data_frame.generate_output(output_file)


if __name__ == "__main__":
    main()