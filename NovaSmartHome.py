# speech recognition
import speech_recognition as sr
import playsound
# OS
import os
# google text to speech
from gtts import gTTS
# date time and calendar
import datetime
import calendar
# warning
import warnings
# random list
import random
# nltk
import nltk
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize
from nltk.tag import CRFTagger
# http request
import requests
import string
# time
import time

# Ignore any warning messages
warnings.filterwarnings('ignore')

# variable global
i = j = k = 0
response = Action = CurrentResponse = ''
id = Value = Device = DeviceNumber = VerbStem = ''

response = response.translate(str.maketrans('', '',
                                            string.punctuation)).lower()
# http request
# action
urlAction = 'http://localhost/novasmarthome/api/actionapi'
ActionRespons = requests.get(urlAction)
VerbDirect = ActionRespons.json()
# device
urlDevice = 'http://localhost/novasmarthome/api/deviceapi'
DeviceRespons = requests.get(urlDevice)
DeviceDirect = DeviceRespons.json()
# response sukses
urlResponse = 'http://localhost/novasmarthome/api/responseapi'
ResponseSukses = requests.get(urlResponse)
arrayResponse = ResponseSukses.json()


# function rekam audio
def recordAudio():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    with sr.Microphone(device_index=None, sample_rate=16000,
                       chunk_size=1024) as source:
        print('Katakan sesuatu!')
        audio = r.listen(source)
    # Speech recognition using Google's Speech Recognition
    data = ''
    try:
        data = r.recognize_google(audio, language='id-ID')
        print('You said: ' + data)
    except sr.UnknownValueError:
        print(
            'Google Speech Recognition tidak dapat memahami audio, kesalahan yang tidak diketahui'
        )
    except sr.RequestError as e:
        print(
            'Meminta hasil dari kesalahan layanan Google Speech Recognition' +
            e)

    return data


# function Nova Assistant
def NovaResponse(text):
    print(text)

    # Convert the text to speech
    myobj = gTTS(text=text, lang='id', slow=False)
    r = random.randint(1, 100000)
    # Save the converted audio to a file
    audio_file = 'audio-' + str(r) + '.mp3'
    myobj.save(audio_file)

    # Play the converted file
    playsound.playsound(audio_file)
    os.remove(audio_file)


def responBalik():
    for DeviceData in DeviceDirect['data']:
        if (DeviceData['device_category'] == Device):
            iDevice = Device
    for actionData in arrayResponse['data']:
        if (actionData['action_stem'] == VerbStem):
            iAction = VerbStem
    values = [
        v for d in arrayResponse['data'] for k, v in d.items()
        if k == 'response' if iDevice == d['device_category']
        if iAction == d['action_stem']
    ]
    try:
        CurrentResponse = random.choice(values)
        print('Response Balikan ke User : ' + CurrentResponse)
        # respon balik saat melakukan action pada device
        NovaResponse(CurrentResponse)
    except IndexError:
        print("nothing found")


def PutFucntion():

    responBalik()

    putdata = {
        'id': id,
        'device_category': Device,
        'number': DeviceNumber,
        'status': Value
    }

    respons = requests.put(urlDevice, putdata)
    message = respons.json()
    print(message)
    return putdata


def NumberResponse():
    NumRes = [
        'Nomor yang anda tuju tidak terdaftar',
        'perintah di tolak, nomor device tidak terdaftar',
        'cek kembali nomor device', 'terjadi kesalahan pada nomor device',
        'gagal menyalakan device, nomor device tidak boleh kosong',
        'maaf Nova tidak dapat menyalakan device. Cek kembali koneksi dan device'
    ]
    CurResp = random.choice(NumRes)
    NovaResponse(CurResp)


def ValueResponse():
    ValRes = [
        'perintah tidak dimengerti. lakukan perintah kembali',
        'Nova tidak dapat menyalakan apapun, tolong lakukan kembali',
        'maaf Nova tidak dapat menyalakan device. Cek kembali koneksi dan device'
        'maaf, gagal menyalakan device'
    ]
    CurResp = random.choice(ValRes)
    NovaResponse(CurResp)


time.sleep(1)
while True:
    # # Rekam audio
    text = recordAudio()
    response = ''  #String respons kosong untuk menambahkan teks respons asisten virtual
    response = response + text
    # NLTK
    # Stop Words
    StopWordFactory = StopWordRemoverFactory()
    StopWord = StopWordFactory.create_stop_word_remover()
    # Stemming
    StemFactory = StemmerFactory()
    Stemmer = StemFactory.create_stemmer()
    # pos tagging
    ct = CRFTagger()
    ct.set_model_file('all_indo_man_tag_corpus_model.crf.tagger')

    # # stop word
    # stop = StopWord.remove(kalimat)
    #tokenize
    tokenize = nltk.tokenize.word_tokenize(response)
    # pos tagging
    tag = ct.tag_sents([tokenize])

    print(tag)
    # print(direct)

    # nltk
    for i in tag[0]:
        # http request
        for DeviceData in DeviceDirect['data']:
            if (i[1] == 'NN'):
                # mencari NN untuk Device
                if (tokenize[j] == DeviceData['device_category']):
                    # hasil dari NN dengan membandungkan device pada database
                    id = DeviceData['id']
                    Device = DeviceData['device_category']
                    # print(
                    #     'ini hasil dari NN dengan membandungkan device pada database : ',
                    #     Device)
                    pass
            if (i[1] == 'JJ'):
                # mencari NN untuk Device
                if (tokenize[j] == DeviceData['device_category']):
                    # hasil dari NN dengan membandungkan device pada database
                    id = DeviceData['id']
                    Device = DeviceData['device_category']
                    # print(
                    #     'ini hasil dari NN dengan membandungkan device pada database : ',
                    #     Device)
                    pass
            if (i[1] == 'VB'):
                # mencari NN untuk Device
                if (tokenize[j] == DeviceData['device_category']):
                    # hasil dari NN dengan membandungkan device pada database
                    id = DeviceData['id']
                    Device = DeviceData['device_category']
                    # print(
                    #     'ini hasil dari NN dengan membandungkan device pada database : ',
                    #     Device)
                    pass
            if (i[1] == 'CD'):
                # mencari NN untuk Device
                if (tokenize[j] == DeviceData['number']):
                    # hasil dari NN dengan membandungkan device pada database
                    DeviceNumber = DeviceData['number']
                    # print(
                    #     'ini hasil dari NN dengan membandungkan device pada database : ',
                    #     DeviceNumber)
                    pass
                if (tokenize[j] != DeviceData['number']):
                    if (tokenize[j] == 'satu'):
                        CurNumber = '1'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'dua'):
                        CurNumber = '2'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'tiga'):
                        CurNumber = '3'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'empat'):
                        CurNumber = '4'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'lima'):
                        CurNumber = '5'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'enam'):
                        CurNumber = '6'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'tujuh'):
                        CurNumber = '7'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'delapan'):
                        CurNumber = '8'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'sembilan'):
                        CurNumber = '9'
                        DeviceNumber = CurNumber
                    elif (tokenize[j] == 'sepuluh'):
                        CurNumber = '10'
                        DeviceNumber = CurNumber
        for VerbData in VerbDirect['data']:
            if (i[1] == 'VB'):
                if (tokenize[j] == VerbData['action_name']):
                    Verb = tokenize[j]
                    # stemming
                    VerbStem = Stemmer.stem(Verb)
                    if (VerbData['action_stem'] == VerbStem):
                        # hasil perbandingan stemming dengan action_stem database
                        # print('ini hasil dari Verb setelah stemming : ', VerbStem)
                        # value perbandingan mengambil dari database action table
                        Value = VerbData['value']
                        # print('ini hasil dari Verb mengambil value dari table : ',
                        #       Value)
        j = j + 1
    print('ID Device Category : ', id)
    print('Device Category : ', Device)
    print('Action \t\t: ', VerbStem)
    print('Device Number \t: ', DeviceNumber)
    print('Value \t\t: ', Value)
    j = 0
    if (Device != '' and DeviceNumber != '' and Value != ''):
        PutFucntion()
        id = Value = Device = DeviceNumber = VerbStem = ''
    elif (DeviceNumber == ''):
        NumberResponse()
    elif (Value == ''):
        ValueResponse()
    else:
        time.sleep(1)