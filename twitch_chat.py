import websocket, subprocess, json, threading
# 게임이랑 전혀 상관없이 mixer만을 위해 존제
# 그래도 pygame 관련해서는 [페이지][10] 참고.
# 
# [10]: https://www.pygame.org/news
# [11]: https://www.pygame.org/docs/
from pygame import mixer

def main():
  # websocket 모듈 깃헙 [페이지][1]에서 복붙
  # 
  # [1]: https://github.com/websocket-client/websocket-client#examples
  # 
  # 아프리카 같은 경우 websocket으로 연결한 주소 부분이 IP 형식. 이 IP를 얻기위해
  # http://live.afreecatv.com:8057/afreeca/player_live_api.php에 POST request를 보낸후
  # response에서 여러 값 이용. 
  websocket.enableTrace(True)
  ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv/",
    # 없어도 가능. Twitch 는 "irc"
    # 아프리카는 'chat', 'agent', 등 여러가지 사용하지만 채팅 [sub]protocol은 'chat'
    # subprotocols = ["foo"],
    on_message = on_message,
    on_error = on_error,
    on_close = on_close)
  ws.on_open = on_open

  # StackOverflow [답변][2]에서 복붙.
  # 
  # [2]: https://stackoverflow.com/a/23826081/3290525
  mixer.init()

  ws.run_forever()

def t_on_message(message):
  # Twitch_chat_parser.js는 twitch.tv/스트리머_아이디/chat 에서 `tmi.뭐시기.tv` 파일에서 함수 복붙
  # `json.dumps` 하니깐 되서 그냥 함.
  # `node -e require("js script file name").method_name`은
  # 구글에서 "how to call javascript module in command line"에서 나온 이 StackOverflow [답변][3] 참고
  # 
  # [3]: https://stackoverflow.com/a/36480927/3290525
  output = subprocess.check_output(['node', '-e', 'require("./twitch_chat_parser.js").parseMessageParts({})'.format(json.dumps(message))])

  msg = json.loads(output.decode("utf-8"))
  cmd = msg["command"]
  cht = None

  # cmd 가 여러가지. 채팅 관련된 것만 필터링.
  if cmd == "PRIVMSG":
    cht = msg["trailing"]
  else:
    return

  # Command Prompt에 출력 (그냥 + 없으면 고장난 것 같지 않게)
  print(cht)

  # C#를 사용. TTS에서 파일을 만들고, 파일이름을 출력함
  filename = subprocess.check_output(['tts.exe', cht])

  # 출력된 파일이름을 사용해서 재생.
  mixer.Sound("D:\\temp\\" + filename.decode() + ".wav").play()

def on_message(ws, message):
  # 파이썬 Threading 모듈 [페이지][3] 읽고 따로 간단하게 시도 해본후 적용
  # 
  # [3]: https://docs.python.org/3/library/threading.html
  threading.Thread(target=t_on_message, args=(message,)).start()
  # Threading 없이 t_on_message에 있는 내용 이곳에 하면 "좀 느리게" 실행됨.

def on_error(ws, error):
  print(error)

def on_close(ws):
  print("### closed ###")

# 여기서 `ws.send` 하는 메시지는 Twitch 방송에서
# F12 > 네트워크 탭 > irc exchange > frame 탭에서 참고.
# 
# `CAP REQ`, `PASS`, `JOIN` 등을 capability 라고 하는것 같은데
# 이것 관련해서는 트위치 개발자 IRC [문서][4] 참고.
# 
# [4]: https://dev.twitch.tv/docs/irc
def on_open(ws):
  ws.send("CAP REQ :twitch.tv/tags twitch.tv/commands")

  # 로그인 하지 않은 사용자 관련 (추측)
  ws.send("PASS SCHMOOPIIE") # 로그인 했을때는 
  ws.send("NICK justinfan62158") # 숫자부분은 달라지는 것 같으며, 로그인 시에는 내 아이디로 변경됨
  ws.send("USER justinfan62158 8 * :justinfan62158") # 여기도

  # 스트리머 아이디
  ws.send("JOIN #스트리머_아이디")

if __name__ == "__main__":
  main()