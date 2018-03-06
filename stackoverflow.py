import pandas as pd
import requests
import zipfile
import shutil

def downloadSurvey():
    url = "https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM"
    request = requests.get(url)
    file = open("survey2017.zip","wb")
    file.write(request.content)
    file.close()

    zipref = zipfile.ZipFile("survey2017.zip", "r")
    zipref.extractall('survey2017')
    zipref.close()

    shutil.move("survey2017/survey_results_public.csv", "survey2017.csv")
    shutil.rmtree("survey2017")

data = None
filtered = None
def frameworksByLanguage(language):
    global data, filtered
    if data is None:
        data = pd.read_csv('survey2017.csv')
        filtered = data[data['HaveWorkedLanguage'].notnull()]

    python = filtered[filtered['HaveWorkedLanguage'].str.contains(language)]

    frameworks = { 'None': 0 }
    for index, row in python.iterrows():
        if pd.isnull(row['HaveWorkedFramework']):
            frameworks['None'] += 1
            continue

        for framework in row['HaveWorkedFramework'].split('; '):
            if framework not in frameworks:
                frameworks[framework] = 1
            else:
                frameworks[framework] += 1
    return frameworks

if __name__ == "__main__":
    downloadSurvey()
    print(frameworksByLanguage("Python"))
