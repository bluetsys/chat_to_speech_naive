import urllib3, json
import websocket, subprocess
from threading import Timer
import threading

def main():
  http = urllib3.PoolManager()
  url = "http://live.afreecatv.com:8057/afreeca/player_live_api.php"
  method = "POST"

  # 여러 data를 보내는데 "bno"만 보내도 가능
  data = { "bno" : "204995968" }
  
  # Request 보냄
  r = http.request(method, url, fields=data)

  # b"foo bar"임
  result = r.data

  
  # b"foo bar"을 "foo bar"로 바꾸기
  result = result.decode('utf-8')

  print(result)

  # 내가 선호하는 json으로 바꾸기.
  result = json.loads(result, encoding='utf-8')
  # `encoding='utf-8'` parameter를 또 해야 한국어가 보임 (왜 인지는 따로 찾아보겠음)
  # 하지만 한국어로 된 값을 사용하지는 않음. 예) 방제와 BJ이름 등만 한국어.

  # 형태 { Channel: "모든 것" }
  result = result["CHANNEL"]

  # 필요한 값들은 단4개
  szChatIp = result["CHIP"]
  szChatPort = result["CHPT"]
  nChatNo = result["CHATNO"]
  szFanTicket = result["FTK"]

  # 나름 Class도 써봄
  cb = WSCallback(szChatIp, szChatPort, nChatNo, szFanTicket)

  # 복붙. 여기서 부터 Twitch랑 비슷
  ws = websocket.WebSocketApp("ws://" + szChatIp + ":" + szChatPort + "/Websocket",
    # 없어도 돌아감.
    # subprotocols = ["chat"],
    on_message = cb.on_message,
    on_error = cb.on_error,
    on_close = cb.on_close)
  ws.on_open = cb.on_open

  ws.run_forever()

def t_on_message(message):
  # b'blah' 를 'blah'
  message = message.decode()

  # 여기서는 json.dumps안해도 됨 (왜 인지는 따로 찾아보겠음!)
  output = subprocess.check_output(['node', '-e', 'require("./afreeca_ws_util.js").readBuffer("{}")'.format(message)])

  # 내가 추구하는 json 형식으로 바꿈.
  # output은 b'foo bar' 형태임으로 `.decode` 사용
  output = json.loads(output.decode())

  # ["serviceCode"] 관련해서는 아프리카 측 세부사항
  if output["serviceCode"] != 4:
    # print(output)
    if output["serviceCode"] == 5:
      print(output["packet"])
      print(output["packet"][0])

  # tts는 안함. 빨리 끝내고 싶어서 트위치만 했음 ㅠ.ㅠ

class WSCallback():
  def __init__(self, szChatIp, szChatPort, nChatNo, szFanTicket):
    websocket.enableTrace(True)
    self.szChatIp = szChatIp
    self.szChatPort = szChatPort
    self.nChatNo = nChatNo
    self.szFanTicket = szFanTicket
    self.szTicket = ""
    self.util_name = "./afreeca_ws_util.js"

  def on_message(self, ws, message):
    # 트위치랑 같음
    threading.Thread(target=t_on_message,args=(message,)).start()

  def on_error(self, ws, error):
    print("WS ERROR")
    print(error)

  def on_close(self, ws):
    print("### closed ###")

  def on_open(self, ws):
    print("OPEN")

    # KeepAlive --> login --> joinch
    # afreeca_ws_util 주석 참고
    msg0 = self.keepAlive()
    msg1 = self.login()
    msg2 = self.joinch()

    # 한번에 3개 다 보내면 안되는 줄 알았는데 되는것 같은데 ...
    # (귀찮아서 안 지운것은 아님 ^^)
    # 직접 Timer 있이, 없이 실행해보기 추천!
    Timer(0.5, ws.send, (msg0,)).start()
    Timer(1, ws.send, (msg1,)).start()
    Timer(1.5, ws.send, (msg2,)).start()

  def keepAlive(self):
    return subprocess.check_output(['node', '-e', 'require("./afreeca_ws_util.js").keepAlive()'])

  def login(self):
    USER_TYPE = None
    GUEST = 16

    # Third argument to login
    USER_TYPE = GUEST
    # (1) szTicket, (2) "", (3) USER_TYPE
    return subprocess.check_output(['node', '-e', 'require("./afreeca_ws_util.js").login("{}", "{}", {})'.format(self.szTicket, "", USER_TYPE)])

  def joinch(self):
    # (1) nChatNo, (2) szFanTicket, (3) z0, (4) z1, (5) z2
    return subprocess.check_output(['node', '-e', 'require("./afreeca_ws_util.js").joinch({}, "{}", "{}", "{}", "{}")'.format(self.nChatNo, self.szFanTicket, "", "", "")])
    # FROM production code as of 201801191252
    # // z2 = v.LivePlayerInfo.getLog({
    # //     set_bps: v.LivePlayerInfo.nRate,
    # //     view_bps: String(Math.min(v.LivePlayerInfo.nRate, 0 == v.LivePlayerInfo.nQuality ? 1e3 : 1 == v.LivePlayerInfo.nQuality ? 2e3 : v.LivePlayerInfo.nRate)),
    # //     quality: 0 == v.LivePlayerInfo.nQuality ?
    # //         "normal" :
    # //         1 == v.LivePlayerInfo.nQuality ?
    # //             "high" : "ori",
    # //     ad_uuid: v.LivePlayerInfo.ad_uuid,
    # //     uuid: v.LivePlayerInfo.uuid,
    # //     geo_cc: v.LivePlayerInfo.geo_cc,
    # //     geo_rc: v.LivePlayerInfo.geo_rc,
    # //     acpt_lang: v.LivePlayerInfo.acpt_lang,
    # //     svc_lang: v.LivePlayerInfo.svc_lang
    # // }) +
    # // v.LivePlayerInfo.getAddInfo({
    # //     pwd: v.LivePlayerInfo.szPassword,
    # //     auth_info: v.LivePlayerInfo.szAuthInfo
    # // })

if __name__ == "__main__":
  main()