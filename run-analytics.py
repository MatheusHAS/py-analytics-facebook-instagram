import os
import argparse
from unidecode import unidecode
from colorama import init,Fore, Back, Style
import requests
import time
import datetime
import json
import xlsxwriter

init()
parser = argparse.ArgumentParser(description='DATA ANALYTICS OF FACEBOOK AND INSTAGRAM')
parser.add_argument('-tkf',dest='tkf',action='store', default='')
parser.add_argument('-tki',dest='tki',action='store', default='')
parser.add_argument('-f',dest='file',action='store', default='output')
ARGS = parser.parse_args()

print(Fore.YELLOW+"==== DATA ANALYTICS OF FACEBOOK AND INSTAGRAM ==== ")
print(Fore.YELLOW+str("==== DESENVOLVIDO POR: {} e {}  ==== ").format("Matheus Azambuja","Geisiane Araujo"))
print(Style.RESET_ALL)

# 0 => FACEBOOK
# 1 => INSTAGRAM
SOCIALS = ['FACEBOOK','INSTAGRAM']
ENDPOINT = ('https://graph.facebook.com/v2.11/','https://api.instagram.com/v1/')
URL_BASE = ['me/posts?fields=created_time%2Cstory%2Cmessage%2Cshares%2Creactions.type(LIKE).limit(0).summary(1).as(like)%2Creactions.type(LOVE).limit(0).summary(1).as(love)%2Creactions.type(HAHA).limit(0).summary(1).as(haha)%2Creactions.type(WOW).limit(0).summary(1).as(wow)%2Creactions.type(SAD).limit(0).summary(1).as(sad)%2Creactions.type(ANGRY).limit(0).summary(1).as(angry)&limit=10',
            'users/{}/media/recent']
URL_BASE_GETID = ['me','users/self']
ACCESS_TOKEN = (ARGS.tkf,ARGS.tki)

DEFAULT_FOLDER = "GRAFICOS"
DEFAULT_FOLDER_TXT = "DADOS"

if not os.path.isdir(DEFAULT_FOLDER):
    print(str('Diretório {} criado').format(DEFAULT_FOLDER))
    os.system('mkdir '+DEFAULT_FOLDER)

if not os.path.isdir(DEFAULT_FOLDER_TXT):
    print(str('Diretório {} criado').format(DEFAULT_FOLDER_TXT))
    os.system('mkdir '+DEFAULT_FOLDER_TXT)

FILE_FB = DEFAULT_FOLDER+'/fb-'+ARGS.file
FILE_IN = DEFAULT_FOLDER+'/in-'+ARGS.file
FILE_ATTR = 'w'
DEFAULT_EXT = "-dados.txt"
FILES = [open(FILE_FB.replace(DEFAULT_FOLDER,DEFAULT_FOLDER_TXT)+DEFAULT_EXT,FILE_ATTR), open(FILE_IN.replace(DEFAULT_FOLDER,DEFAULT_FOLDER_TXT)+DEFAULT_EXT,FILE_ATTR)]
FILE_LOG = open('logs.txt','a')
LOG_LINE = "[{}]-[{}] : {}"

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S+0000'
VECTOR_DAYS = ('SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM')
SEP = "|"
SUM_REACTIONS_DAYS_FB = [0,0,0,0,0,0,0]
SUM_REACTIONS_DAYS_IN = [0,0,0,0,0,0,0]

VECTOR_HOURS_LIKE_FB = [0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0]
VECTOR_HOURS_LIKE_IN = [0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0]

def getUserId(json):
    if json.get('data') == None:
        return json['id']
    else:
        return json['data']['id']

def getUserName(json):
    if json.get('data') == None:
        return json['name']
    else:
        return json['data']['username']

def utc2local (utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.datetime.fromtimestamp (epoch) - datetime.datetime.utcfromtimestamp (epoch)
    return utc + offset

def writeLog(social=0,message=""):
    day_hour = datetime.datetime.now()
    FILE_LOG.write(LOG_LINE.format(day_hour,SOCIALS[social],message+"\n"))

def getUrlWithToken(pos=0,url=""):
    url = url + "?access_token="+ACCESS_TOKEN[pos] if "?" not in url else url + "&access_token="+ACCESS_TOKEN[pos]
    return url

def saveFacebookData(post,file):
    # 0 => Data de Criação (FACEBOOK GRAPH API)
    # 1 => Data em SP
    # 2 => Dia da Semana
    # 3 => POST ID
    # 4 => LIKE COUNT
    # 5 => LOVE COUNT
    # 6 => HAHA COUNT
    # 7 => WOW COUNT
    # 8 => SAD COUNT
    # 9 => ANGRY COUNT
    date_obj = datetime.datetime.strptime(post['created_time'],DATE_FORMAT)
    hour_post = utc2local(date_obj).hour #horário da postagem 00~23
    weekday_date = date_obj.weekday()
    data_save = unidecode(post['created_time']+SEP+
                    str(utc2local(date_obj))+SEP+
                    str(VECTOR_DAYS[weekday_date])+SEP+
                    post['id']+SEP+
                    str(post['like']['summary']['total_count'])+SEP+
                    str(post['love']['summary']['total_count'])+SEP+
                    str(post['haha']['summary']['total_count'])+SEP+
                    str(post['wow']['summary']['total_count'])+SEP+
                    str(post['sad']['summary']['total_count'])+SEP+
                    str(post['angry']['summary']['total_count'])+SEP+
                    "\n")
    file.write(data_save)
    total_count = 0
    total_count = post['like']['summary']['total_count']+post['love']['summary']['total_count']+post['haha']['summary']['total_count']+post['wow']['summary']['total_count']+post['sad']['summary']['total_count']+post['angry']['summary']['total_count']
    SUM_REACTIONS_DAYS_FB[weekday_date] = SUM_REACTIONS_DAYS_FB[weekday_date] + total_count
    VECTOR_HOURS_LIKE_FB[hour_post] = VECTOR_HOURS_LIKE_FB[hour_post] + total_count

def timestamp_to_datetime(ts):
    return datetime.datetime.utcfromtimestamp(float(ts))

#def datetime_to_timestamp(dt):
#    return calendar.timegm(dt.timetuple())

def getGraphLineReactionsByHourXLS(workbook,data,title,network):
    
    data_start_loc_dt1 = [0,0]
    data_end_loc_dt1 = [12,0]

    data_start_loc_dt2 = [0,1]
    data_end_loc_dt2 = [10,1]

    data_start_loc_1 = [0, 2]
    data_end_loc_1 = [12, 2]

    data_start_loc_2 = [0, 3]
    data_end_loc_2 = [10, 3]

    VECTOR_HOURS1 = []
    VECTOR_DT1 = []
    VECTOR_HOURS2 = []
    VECTOR_DT2 = []

    for x in range(0,13):
        VECTOR_DT1.append(data[x])
    
    for x in range(12,24):
        VECTOR_DT2.append(data[x])
    
    for x in range(13):
        VECTOR_HOURS1.append(x)

    for x in range(13,25):
        if x == 24:
            VECTOR_HOURS2.append("00")
        else:
            VECTOR_HOURS2.append(x)

    # Configurações do Grafico
    chart = workbook.add_chart({'type': 'line'})
    chart.set_y_axis({'name': 'Quantidade de Curtidas'})
    chart.set_x_axis({'name': 'Horários'})
    chart.set_title({'name': title})

    worksheet = workbook.add_worksheet("POR HORA")

    # Adicionar dados as Colunas
    worksheet.write_column(*data_start_loc_dt1, data=VECTOR_DT1)
    worksheet.write_column(*data_start_loc_1, data=VECTOR_HOURS1)
    worksheet.write_column(*data_start_loc_dt2, data=VECTOR_DT2)
    worksheet.write_column(*data_start_loc_2, data=VECTOR_HOURS2)


    chart.add_series({
        'values': [worksheet.name] + data_start_loc_dt1 + data_end_loc_dt1,
        'categories': [worksheet.name] + data_start_loc_1 + data_end_loc_1,
        'name': "Curtidas",
    })

    worksheet.insert_chart('E1', chart)

    # Configurações do Grafico 2
    chart2 = workbook.add_chart({'type': 'line'})
    chart2.set_y_axis({'name': 'Quantidade de Curtidas'})
    chart2.set_x_axis({'name': 'Horários'})
    chart2.set_title({'name': title})

    chart2.add_series({
        'values': [worksheet.name] + data_start_loc_dt2 + data_end_loc_dt2,
        'categories': [worksheet.name] + data_start_loc_2 + data_end_loc_2,
        'name': "Curtidas",
    })

    worksheet.insert_chart('E16', chart2)

    workbook.close()

def genGraphLineSUMReactionsDaysXLS(data,data_hours,categories_data,title,file,network):
    data_start_loc = [0, 0]
    data_end_loc = [6, 0]

    data_start_loc_cat = [0,1]
    data_end_loc_cat = [6,1]

    workbook = xlsxwriter.Workbook(file+'.xlsx')

    # Configurações do Grafico
    chart = workbook.add_chart({'type': 'line'})
    chart.set_y_axis({'name': 'Quantidade de Curtidas'})
    chart.set_x_axis({'name': 'Dias da Semana'})
    chart.set_title({'name': title})

    worksheet = workbook.add_worksheet("DIAS DA SEMANA")
    # Adicionar dados as Colunas
    worksheet.write_column(*data_start_loc, data=data)
    worksheet.write_column(*data_start_loc_cat, data=categories_data)

    chart.add_series({
        'values': [worksheet.name] + data_start_loc + data_end_loc,
        'categories': [worksheet.name] + data_start_loc_cat + data_end_loc_cat,
        'name': "Curtidas",
    })
    worksheet.insert_chart('C1', chart)
    getGraphLineReactionsByHourXLS(workbook,data_hours,str("Por Hora - {}").format(network),network)

def saveInstagramData(post,file):
    # 0 => Data de Criação (FACEBOOK GRAPH API)
    # 1 => Data em SP
    # 2 => Dia da Semana
    # 3 => POST ID
    # 4 => LIKE COUNT
    date_obj = timestamp_to_datetime(post['created_time'])
    
    hour_post = utc2local(date_obj).hour #horário da postagem 00~23

    weekday_date = date_obj.weekday()
    likes = 0
    if post.get('likes') == None:
        likes = 0
    else:
        likes = int(post['likes']['count'])
    data_save = unidecode(post['created_time']+SEP+
                    str(utc2local(date_obj))+SEP+
                    str(VECTOR_DAYS[weekday_date])+SEP+
                    post['id']+SEP+
                    str(likes)+
                    "\n")
    file.write(data_save)
    SUM_REACTIONS_DAYS_IN[weekday_date] = SUM_REACTIONS_DAYS_IN[weekday_date] + likes
    VECTOR_HOURS_LIKE_IN[hour_post] = VECTOR_HOURS_LIKE_IN[hour_post] + likes

def run(argpos=0, file=''):
    r = requests.get(ENDPOINT[argpos]+getUrlWithToken(argpos,URL_BASE_GETID[argpos])).json()
    if r.get('error'):
        msg_erro = 'Ocorreu um erro:'+r['error']['message']
        print(Fore.RED+'\n\n'+msg_erro+'\n\n')
        print(Style.RESET_ALL)
        writeLog(argpos,msg_erro)
    else:
        USERID = getUserId(r)
        USERNAME = getUserName(r)
        if USERID != None:
            msg = "ID Obtido com Sucesso"
            msg_coleta = "Iniciando coleta de dados do {} no usuário {}"
            msg_coleta_fim = "Coleta de dados finalizada"
            msg_final = "[{}] [{}] "+msg
            writeLog(argpos,msg_final.format(SOCIALS[argpos],USERNAME))
            print(Fore.GREEN+msg_final.format(SOCIALS[argpos],USERNAME))
            #print(Style.RESET_ALL)
            print(Fore.YELLOW+msg_coleta.format(SOCIALS[argpos],USERNAME))
            print(Style.RESET_ALL)
            if argpos == 0:
                url_posts = ENDPOINT[argpos]+getUrlWithToken(argpos,URL_BASE[argpos])
                #print(url_posts)
                posts = requests.get(url_posts).json()
                while True:
                    try:
                        [saveFacebookData(post=post,file=file) for post in posts['data']]
                        posts = requests.get(posts['paging']['next']).json()
                    except KeyError:
                        FILES[argpos].close()
                        break
            if argpos == 1:
                url_posts = ENDPOINT[argpos]+getUrlWithToken(argpos,URL_BASE[argpos].format(USERID))
                #print(url_posts)
                posts = requests.get(url_posts).json()
                while True:
                    try:
                        [saveInstagramData(post=post,file=file) for post in posts['data']]
                        posts = requests.get(posts['pagination']['next_url']).json()
                    except KeyError:
                        FILES[argpos].close()
                        break
            print(Fore.GREEN+msg_coleta_fim)
            print(Style.RESET_ALL)

if ACCESS_TOKEN[0]:
    run(0,FILES[0])
    categories_data = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']
    genGraphLineSUMReactionsDaysXLS(SUM_REACTIONS_DAYS_FB,VECTOR_HOURS_LIKE_FB,categories_data,str("Dias da Semana - {}").format(SOCIALS[0]),FILE_FB,SOCIALS[0])

if ACCESS_TOKEN[1]:
    run(1,FILES[1])
    categories_data = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']
    genGraphLineSUMReactionsDaysXLS(SUM_REACTIONS_DAYS_IN,VECTOR_HOURS_LIKE_IN,categories_data,str("Dias da Semana - {}").format(SOCIALS[1]),FILE_IN,SOCIALS[1])

for f in FILES:
    f.close()