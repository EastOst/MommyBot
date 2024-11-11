import requests
from itertools import tee
import json
from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS를 위한 임포트
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)  # CORS 설정
class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-DASH-001',
                        headers=headers, json=completion_request, stream=True) as r:
            line_iter, next_iter = tee(r.iter_lines())

            for line in line_iter:
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data:"):
                        json_data = json.loads(line[5:])  # 'data: ' 부분을 제거하고 JSON으로 변환
                        try:
                            if json_data["stopReason"] == "stop_before":
                                print("Content:", json_data['message']['content'])
                                result = json_data['message']['content']
                        except Exception as e:
                            print(f"Error processing line: {e}")
        return result

@app.route('/chat', methods=["POST"])
def chat():
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY/jwXGvS2UWi0VCOK0TnU35Hv5SQh5pNdtWYBU/S/RQv',
        api_key_primary_val='WRaXQs3woQHWg8NMwi7mMBhdPIYKANpOYp2gA7GJ',
        request_id='6a8c132c48ee4387b5611e6ee15ce0fa'
    )

    # 사용자가 보낸 메시지를 리퀘스트 바디에서 받음
    user_message = request.json.get('messages', {}).get('message',"")  # 사용자의 메시지를 받음
    conversation_pattern=request.json.get('chatBot',{}).get('conversationPattern','')
    conversation_Point=request.json.get('conversationPoint',{}).get('conversationPoint','')
    chat_histories=request.json.get('chatHistoryies',[])
    if user_message:
        print("error ",user_message)
    if conversation_pattern:
        print("error",conversation_pattern)

    
    ## db에 저장 로직 
    # 기본 대화 패턴 설정
    preset_text = [
        {"role": "system", "content": f"당신은 한 아이의 어머니 입니다. 아들을 집에서 기다리고 있으며, 아들을 사랑하지만, 사랑표현에 적극적이다. 잔소리를 많이 한다. \n\n\n##대화시점##\n{conversation_Point}\n##대화 패턴##\n{conversation_pattern}\n\n\n\n\n"},
    ]
    if chat_histories:
        for i in chat_histories:
            preset_text.append({"role":"user","content":i["userMessage"]})
            preset_text.append({"role":"assistant","content":i["aiResponse"]})
    preset_text.append({"role": "user", "content": user_message} )
    print(user_message)

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 83,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 1
    }
    

    ai_response = completion_executor.execute(request_data)
    chat_history_data = {
        'userMessage': user_message,
        'aiResponse': ai_response
    }

    
    return jsonify({"aiResponse":ai_response,"userMessage":user_message})

if __name__ == '__main__':
    app.run(port=5000,debug=True)


   
