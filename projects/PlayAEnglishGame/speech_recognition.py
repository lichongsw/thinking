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

import requests
import base64
import json
import time
import sys
from flask import Flask, request, jsonify
# import pyaudio
# import wave

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
            # 'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
            'Content-Type': 'audio/mp3; codecs=audio/mpeg; samplerate=48000',
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
    return response,getResponseTime

def test_demo(referenceText, referenceAudio):
    uploadFinishTime = time.time()
    # referenceText = "Hello"
    # referenceAudio = "hello_useful_2.wav"

    # referenceText = "Interactive language learning with pronunciation assessment gives you instant feedback on pronunciation, fluency, prosody, grammar, and vocabulary through interactive chats."
    # referenceAudio = "Interactive_language_learning_02.mp3"

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


app = Flask(__name__)

@app.route('/upload_audio', methods=['POST', "GET"])
def upload_audio():
    # 获取上传的文件
    audio_file = request.files['audio']
    
    # 保存语音文件
    filename = f'uploaded_audio_{request.form["filename"]}' if 'filename' in request.form else 'uploaded_audio.wav'
    audio_file.save(f'{filename}')
    
    # # 处理语音文件（这里只是简单保存，实际应用可能需要更多操作）
    # p = pyaudio.PyAudio()
    # wf = wave.open(f'{filename}', 'rb')
    
    # # 假设我们要将语音转换为文本
    # text = convert_audio_to_text(wf)
    
    # # 返回结果
    return jsonify({'message': f'Audio uploaded successfully', 'text': "hello world"})

def main() -> int:
    # test_demo("Hello", "hello_useful_2.wav")
    app.run(port=5000, debug=True)
    return 0

# 添加main函数入口
if __name__ == '__main__':
    sys.exit(main())