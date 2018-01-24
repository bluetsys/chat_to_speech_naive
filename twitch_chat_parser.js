// tmi.어쩌고.js 에서 채팅 관련된 부분 복붙.
// 정확한 디테일은 관심 없고, 방송 플랫폼마다 다르므로 스킵.
//   예) 아프리카는 Int8Array, Uint8Array, ArrayBuffer 클래스 등 이용.
function parseMessageParts(msgString) {
    msgString = msgString.trim();
    var parsedMsg = { tags: {}, prefix: null, command: null, params: null, trailing: null };
    var tagsEnd = -1;
    if (msgString.charAt(0) === "@") {
        tagsEnd = msgString.indexOf(" ");
        // parsedMsg.tags = parseTwitchTags(msgString.substr(1, tagsEnd - 1))
    }
    var prefixStart = tagsEnd + 1,
        prefixEnd = -1;
    if (msgString.charAt(prefixStart) === ":") {
        prefixEnd = msgString.indexOf(" ", prefixStart);
        parsedMsg.prefix = msgString.substr(prefixStart + 1, prefixEnd - (prefixStart + 1))
    }
    var trailingStart = msgString.indexOf(" :", prefixStart);
    if (trailingStart >= 0) { parsedMsg.trailing = msgString.substr(trailingStart + 2) } else { trailingStart = msgString.length }
    var actionMatch = (parsedMsg.trailing || "").match(/^\u0001ACTION ([^\u0001]+)\u0001$/);
    if (actionMatch) {
        parsedMsg.style = "action";
        parsedMsg.action = actionMatch[1]
    }
    var commandAndParams = msgString.substr(prefixEnd + 1, trailingStart - prefixEnd - 1).split(" ");
    parsedMsg.command = commandAndParams[0];
    if (commandAndParams.length > 1) { parsedMsg.params = commandAndParams.slice(1) }
    process.stdout.write(JSON.stringify(parsedMsg));
}

module.exports.parseMessageParts = parseMessageParts;