import pandas as pd
import xml.etree.ElementTree as eTree


inputPath = '..\\DataFile\\download\\'
inputFile_a = inputPath + 'a_lvr_land_a.xml'
inputFile_b = inputPath + 'b_lvr_land_a.xml'
inputFile_e = inputPath + 'e_lvr_land_a.xml'
inputFile_f = inputPath + 'f_lvr_land_a.xml'
inputFile_h = inputPath + 'h_lvr_land_a.xml'

outputfile1 = '..\\DataFile\\SaveData\\filter_a.csv'
outputfile2 = '..\\DataFile\\SaveData\\filter_b.csv'

def loadData(path):
    tree = eTree.parse(path)
    root = tree.getroot()
    get_range = lambda col: range(len(col))
    l = [{r[i].tag:r[i].text for i in get_range(r)} for r in root]

    result = pd.DataFrame.from_dict(l)

    return result

def main():
    df_a = loadData(inputFile_a)
    df_b = loadData(inputFile_b)
    df_e = loadData(inputFile_e)
    df_f = loadData(inputFile_f)
    df_h = loadData(inputFile_h)

    df_all = df_a.append(df_b).append(df_e).append(df_f).append(df_h)

    df_mask = (df_all['主要用途'] == '住家用') & (df_all['建物型態'].str.match('住宅大樓'))
    filtered_df = df_all[df_mask]

    filter_floor = filtered_df[filtered_df["總樓層數"].str.contains('十一層|十二層') == False]

    filter_floor.to_csv(outputfile1, encoding ='utf_8_sig')

    df_all['CarCnt'] = df_all['交易筆棟數'].str.split('位').str[1]

    totalCnt = df_all['總價元'].count()
    totalCarCnt = sum(pd.to_numeric(df_all['CarCnt']))
    totalCarMoney = sum(pd.to_numeric(df_all['車位總價元']))
    avgMoney = pd.to_numeric(df_all['總價元']).mean()
    avgCarMoney = totalCarMoney / totalCarCnt

    grades = {
        "總件數": [totalCnt],
        "總車位數": [totalCarCnt],
        "平均總價元": [avgMoney],
        "平均車位總價元": [avgCarMoney]
    }

    df2 = pd.DataFrame(grades)
    df2.to_csv(outputfile2, encoding ='utf_8_sig')

if __name__ == '__main__':
    main()
    print('finish!')
