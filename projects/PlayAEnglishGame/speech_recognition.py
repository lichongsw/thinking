#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.
#
# Microsoft Cognitive Services (formerly Project Oxford): https://www.microsoft.com/cognitive-services
#
# Copyright (c) Microsoft Corporation
# All rights reserved.
#
# MIT License:
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
import requests
import base64
import json
import time
import random
import sys
import shutil
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from ratelimit import limits

import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(subscription="e82807440b154003abb0db805cb70f3b", region="westus")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
# The neural multilingual voice can speak different languages based on the input text.
speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


# subscriptionKey = "e82807440b154003abb0db805cb70f3b" # replace this with your subscription key
# region = "westus" # replace this with the region corresponding to your subscription key, e.g. westus, eastasia

subscriptionKey = "e7849e713ed7417f8a4dd76d507c998d" # replace this with your subscription key
region = "eastasia" # replace this with the region corresponding to your subscription key, e.g. westus, eastasia

# a common wave header, with zero audio length
# since stream data doesn't contain header, but the API requires header to fetch format information, so you need post this header as first chunk for each query
WaveHeader16K16BitMono = bytes([ 82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18, 0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0, 125, 0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0 ])

# a generator which reads audio data chunk by chunk
# the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
def get_chunk(audio_source, chunk_size=10240):
    yield WaveHeader16K16BitMono
    while True:
        # time.sleep(chunk_size / 32000) # to simulate human speaking rate
        # time.sleep(chunk_size / 320000) # to simulate human speaking rate
        chunk = audio_source.read(chunk_size)
        if not chunk:
            uploadFinishTime = time.time()
            break
        yield chunk

# reference text and audio is enough to do recognition
def do_recognition(referenceText, audio):
    audioFile = open(audio, 'rb')
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\", \"granularity\":\"Phoneme\", \"phonemeAlphabet\":\"IPA\"}" % referenceText
    print("pronAssessmentParamsJson:", pronAssessmentParamsJson)
    pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

# build request
    url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-us" % region
    print("url:", url)
    headers = { 'Accept': 'application/json;text/xml',
            'Connection': 'Keep-Alive',
            'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
            # 'Content-Type': 'audio/mp3; codecs=audio/mpeg; samplerate=48000',
            'Ocp-Apim-Subscription-Key': subscriptionKey,
            'Pronunciation-Assessment': pronAssessmentParams,
            'Transfer-Encoding': 'chunked',
            'Expect': '100-continue' }
    # print("headers:", headers)
    # send request with chunked data
    response = requests.post(url=url, data=get_chunk(audioFile), headers=headers)
    print("response:", response)
    getResponseTime = time.time()
    audioFile.close()
    os.remove(audio)
    return response,getResponseTime


def recognition(referenceText, referenceAudio):
    uploadFinishTime = time.time()
    startTime = time.time()
    response, getResponseTime = do_recognition(referenceText, referenceAudio)
    resultJson = json.loads(response.text)
    # print(json.dumps(resultJson, indent=4))
    # 写到json文件
    with open('sample.json', 'w') as f:
        json.dump(resultJson, f, indent=4)

    latency = getResponseTime - uploadFinishTime
    print("Latency = %sms" % int(latency * 1000))
    print("start time:", startTime, " , upload finish time:", uploadFinishTime, " , get response time:", getResponseTime, " , latency:", latency)
    return resultJson


app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization, Text')
    return response

@app.route('/upload_audio', methods=['POST', "GET"])
def upload_audio():
    print("1111111111111")
    print(request)
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file part'})
    
    # 获取上传文件
    file = request.files['audio']
    
    # 检查文件是否为空
    if file.filename == '':
        return {'error': 'No selected file'},
    
    # 保存文件到本地
    filename = f'{"upload_" + file.filename}'
    print("22222222222")
    print(filename)
    file.save(os.path.join(app.root_path, filename))
    
    return jsonify({'message': 'File uploaded successfully'})


last_request_time = {}
@app.route('/binary-data', methods=['POST', "GET"])
@limits(calls=60, period=60)
def receive_binary_data():
    # 客户端IP流控
    ip_address = request.remote_addr
    last = last_request_time.get(ip_address, 0)
    if last != 0:
        if time.time() - last < 5:
            print("Rate limit exceeded")
            return jsonify({"RecognitionStatus": "Failed", "Message": "Try later"})
    last_request_time[ip_address] = time.time()
    
    # 获取二进制数据
    binary_data = request.data
    
    # 打印接收到的二进制数据长度
    print(f"Received {len(binary_data)} bytes of data")
    

    # 返回确认消息
    if request.headers["Text"]:
        # 将其保存到文件中. 为了支持并发，随机文件名
        fileName = "received_data" + random.randint(0, 10000).__str__() + ".wav"
        with open(fileName, "wb") as f:
            f.write(binary_data)
            f.flush()
            f.close()
        return recognition(request.headers["Text"], fileName)
    else:
        return jsonify({"RecognitionStatus": "Failed", "Message": "Invalid text"})

@app.route('/tts', methods=['POST', "GET"])
def text_to_speech():
    # 返回确认消息
    # return jsonify({"message": "Do text_to_speech successfully"})
    print("tts==============================")
    if request.headers["Text"]:
        text = request.headers["Text"]
        print(text)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        with open("tts_output.wav", "wb") as file:
            file.write(speech_synthesis_result.audio_data)
        response = Response(speech_synthesis_result.audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        return response
    else:
        return jsonify({"TTSStatus": "Failed"})


def local_demo():
    # local bemo
    shutil.copy("hello_useful_2.wav", "hello_useful_2_tmp.wav")
    recognition("Hello", "hello_useful_2_tmp.wav")
    # shutil.copy("output.wav", "output_tmp.wav")
    # recognition("", "output_tmp.wav")

def main() -> int:
    # local_demo()
    app.run(port=5000, debug=True)
    return 0


# 添加main函数入口
if __name__ == '__main__':
    sys.exit(main())