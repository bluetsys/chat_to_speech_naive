import urllib3, json
import websocket, subprocess
from threading import Timer
import threading

def main():
  http = urllib3.PoolManager()
  url = "http://live.afreecatv.com:8057/afreeca/player_live_api.php"
  method = "POST"

  data = { "bno" : "205276997" }
  
  r = http.request(method, url, fields=data)

  result = r.data

  
  result = result.decode('utf-8')

  print(result)

  result = json.loads(result, encoding='utf-8')

  result = result["CHANNEL"]

  szChatIp = result["CHIP"]
  szChatPort = result["CHPT"]
  nChatNo = result["CHATNO"]
  szFanTicket = result["FTK"]

  cb = WSCallback(szChatIp, szChatPort, nChatNo, szFanTicket)

  ws = websocket.WebSocketApp("ws://" + szChatIp + ":" + szChatPort + "/Websocket",
    on_message = cb.on_message,
    on_error = cb.on_error,
    on_close = cb.on_close)
  ws.on_open = cb.on_open

  ws.run_forever()

def t_on_message(message):
  message = message.decode()

  output = subprocess.check_output(['node', '-e', 'require("./afreeca_ws_util.js").readBuffer("{}")'.format(message)])

  output = json.loads(output.decode())

  if output["serviceCode"] != 4:
    # print(output)
    if output["serviceCode"] == 5:
      print(output["packet"])
      print(output["packet"][0])

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
    threading.Thread(target=t_on_message,args=(message,)).start()

  def on_error(self, ws, error):
    print("WS ERROR")
    print(error)

  def on_close(self, ws):
    print("### closed ###")

  def on_open(self, ws):
    print("OPEN")

    # KeepAlive --> login --> joinch
    msg0 = self.keepAlive()
    msg1 = self.login()
    msg2 = self.joinch()

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