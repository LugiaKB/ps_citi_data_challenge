import pandas as pd

class DataFrame:
    
    def __init__(self, input_file: str):
        self.df = pd.read_csv(input_file)
        self.modes = {}
        
        
    def get_mode(self, column: str) -> str:
        mode_series = self.df[column].dropna().mode()
        mode = mode_series.iloc[0] if not mode_series.empty else None
        self.modes[column] = mode
        
        return mode
    
    
    def generate_output(self, output_file: str):
        self.df.to_csv(output_file, index=False)
        
    
    def normalize_seniority(self):
        
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
        
        mode = self.get_mode('Nivel_Senioridade')
        
        self.df['Nivel_Senioridade'] = self.df['Nivel_Senioridade'].map(replacement_map).fillna(mode)
        
        
    
def main():
    input_file = 'Base_Membros_Desempenho - Base_Membros_Desempenho.csv'
    output_file = 'Base_Membros_Desempenho_Cleaned.csv'

    data_frame = DataFrame(input_file)
    
    data_frame.normalize_seniority()
    
    data_frame.generate_output(output_file)


if __name__ == "__main__":
    main()