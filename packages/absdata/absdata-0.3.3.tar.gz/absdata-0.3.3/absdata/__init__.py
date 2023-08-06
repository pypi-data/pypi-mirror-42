#connecting to the sql server
engine = create_engine('mysql+pymysql://root:password@35.197.186.120/Demographics')  #username:password
engine.connect()
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)  
session = Session()


def get_c_ratio(code, year):
    '''obtains the set of correspondencies and ratios a code, at this point it outputs an array'''
    correspondencies = pd.read_sql_table('Correspondencies', engine)
    if year == 2016:
        #subsetting the dataframe according to code2016, selecting ratios and 2011 codes as columns
        df = correspondencies[correspondencies['Code2016'] == code][['Code2011', 'Ratio']]
        code_list = list(df['Code2011'])
        ratio_list = list(df['Ratio'])
        #creating a tuple so that mapping codes to ratios is easier
        code2011_ratio = zip(code_list, ratio_list)
        return(code2011_ratio)
    if year == 2011:
        #obtaining correspondencies and ratios
        df = correspondencies[correspondencies['Code2011'] == code][['Code2016', 'Ratio']]
        code_list = list(df['Code2016'])
        ratio_list = list(df['Ratio'])
        #creating a tuple so that mapping codes to ratios is easier
        code2016_ratio = zip(code_list, ratio_list)
        return(code2016_ratio)
    
        
def correct_weights(f, code, year, demographic):
    '''converts function output using appropriate weights'''
    #obtaining correspondencies
    code_ratio = get_c_ratio(code = code, year = year)
    try:
    #obtaining statistic for each 2011 code, then weighting by ratio associated with that code
        output_list =  [f(code = x, year = year, demographic = demographic)*y for x,y in code_ratio]
        weighted_value = sum(output_list)
        return(weighted_value) #we index 0 since the object is actually a singleton array
    except TypeError:
        print('The function you have specfied does not produce a numeric value')
  
    
def get_population(code, year, demographic):
    '''The function returns the total population of a demographic group within a statistical region'''
    #population is in the g01 table
    if year == 2016:
        G01_2016 = pd.read_sql_table('G01_2016', engine)
        if demographic == 'Male':
            return(list(G01_2016[G01_2016['Code'] == code]['Tot_P_M'].values)[0])
        if demographic == 'Female':
            return(list(G01_2016[G01_2016['Code'] == code]['Tot_P_F'].values)[0])
        if demographic == 'Total':
            return(list(G01_2016[G01_2016['Code'] == code]['Tot_P_M'] +  G01_2016[G01_2016['Code'] == code]['Tot_P_F'])[0])
        else:
            print('Error: Check arguments')
    
    if year == 2011:
        B01_2011 = pd.read_sql_table('B01_2011', engine)
        if demographic == 'Male':
            return(list(B01_2011[B01_2011['Code'] == code]['Tot_P_M'].values)[0])
        if demographic == 'Female':
            return(list(B01_2011[B01_2011['Code'] == code]['Tot_P_F'].values)[0])
        if demographic == 'Total':
            return(list(B01_2011[B01_2011['Code'] == code]['Tot_P_M'] +  B01_2011[B01_2011['Code'] == code]['Tot_P_F'])[0])
        else:
            print('Error: Check arguments')
    
    else:
        print('Error: Check arguments')


def list_correspondencies(code, year):
    '''lists correspondencies and ratios for a code -- differs slightly from get_c_ratio, more user friendly'''

    correspondencies = pd.read_sql_table('Correspondencies', engine)
    if year == 2016:
        #subsetting the dataframe according to code2016, selecting ratios and 2011 codes as columns
        df = correspondencies[correspondencies['Code2016'] == code][['Code2011', 'Ratio']]
        code_list = list(df['Code2011'])
        ratio_list = list(df['Ratio'])
        #creating a tuple so that mapping codes to ratios is easier
        code2011_ratio = zip(code_list, ratio_list)
        return(list(code2011_ratio))
    if year == 2011:
        #obtaining correspondencies and ratios
        df = correspondencies[correspondencies['Code2011'] == code][['Code2016', 'Ratio']]
        code_list = list(df['Code2016'])
        ratio_list = list(df['Ratio'])
        #creating a tuple so that mapping codes to ratios is easier
        code2016_ratio = zip(code_list, ratio_list)
        return(list(code2016_ratio))