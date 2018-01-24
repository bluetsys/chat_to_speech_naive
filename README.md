# 영상

[![영상](https://img.youtube.com/vi/LFwscNJQ6aQ/0.jpg)][https://youtu.be/LFwscNJQ6aQ]

[https://youtu.be/LFwscNJQ6aQ](https://youtu.be/LFwscNJQ6aQ)

관련 영상.

# 실행방법

### Twitch chat to speech

```
# twitch_chat.py
def on_open(ws):
  ws.send("CAP REQ :twitch.tv/tags twitch.tv/commands")

  # 로그인 하지 않은 사용자 관련 (추측)
  ws.send("PASS SCHMOOPIIE") # 로그인 했을때는 
  ws.send("NICK justinfan62158") # 숫자부분은 달라지는 것 같으며, 로그인 시에는 내 아이디로 변경됨
  ws.send("USER justinfan62158 8 * :justinfan62158") # 여기도

  # 스트리머 아이디
  ws.send("JOIN #스트리머_아이디")
```

위 코드에서 "JOIN #스트리머_아이디", '스트리머_아이디'를 "www.twitch.tv/스트리머_아이디" 에서 스트리머_아이디로 대체 한후 `python twitch_chat.py` 실행

### 아프리카 chat to speech

아프리카 방송 시청 url, "http://play.afreecatv.com/스트리머_아이디/방송국_숫자", 에서 "방송국_숫자"를

```
# afreeca_chat.py 파일

# 여러 data를 보내는데 "bno"만 보내도 가능
data = { "bno" : "방송국 숫자 ID 같음" }
```

위 코드에서 "bno" 키의 값, "방송국 숫자 ID 같음" 부분에 입력후 `python afreeca_chat.py`.

### 코드 참고

"twitch_chat_parser.js"은 "https://www.twitch.tv/스트리머_아이디/chat" 페이지에서 "tmi.숫자랑영어.js" 참고

"afreeca_ws_util.js"은 아프리카 방송시청 페이지에서 "LivePlayer.min.js" 참고

C# SpeechSynthesizer: https://msdn.microsoft.com/en-us/library/system.speech.synthesis.speechsynthesizer(v=vs.110).aspx

Web Speech API (Mozilla): https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
-> Demo github repo: https://github.com/mdn/web-speech-api/

WebSocket API (Mozilla): https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

Python websocket-client: https://github.com/websocket-client/websocket-client

Python Threading: https://docs.python.org/3/library/threading.html#thread-objects

Twitch Developers: https://dev.twitch.tv/