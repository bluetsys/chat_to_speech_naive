// LivePlayer.min.js 에서 필요 부분 복붙.

var _ = String.fromCharCode(27),
    k = String.fromCharCode(9),
    w = String.fromCharCode(12),
    SVC_KEEPALIVE = 0,
    SVC_LOGIN = 1,
    SVC_JOINCH = 2;

// KeepAlive --> login --> joinch
// 순서는 Trial&error로 알아냄... ㅠ.ㅠ
// 아프리카는 트위치 처럼 websocket exchange가 안보이는데, 내용 또한 parsing이 필요.

function keepAlive() {
    var e = new Array;
    e.push(w);
    var t = makeBuffer(e),
        n = makeBuffer(makeHeader(SVC_KEEPALIVE, t.byteLength, 0)),
        r = mergePacket(n, t);
    
    process.stdout.write(Buffer.from(r));
}

function login(e, t, n) {
    var r = new Array;
    r.push(w), r.push(e), r.push(w), r.push(stringToUint(t)), r.push(w), r.push(n), r.push(w);
    var i = makeBuffer(r),
        a = makeBuffer(makeHeader(SVC_LOGIN, i.byteLength, 0)),
        o = mergePacket(a, i);
    
    process.stdout.write(Buffer.from(o));
}

function joinch(e, t, n, r, i) {
    var a = new Array;
    a.push(w), a.push(e), a.push(w), a.push(t), a.push(w), a.push(n), a.push(w), a.push(stringToUint(r)), a.push(w), a.push(i), a.push(w);
    var o = makeBuffer(a),
        s = makeBuffer(makeHeader(SVC_JOINCH, o.byteLength, 0)),
        l = mergePacket(s, o);
    
    process.stdout.write(Buffer.from(l));
}

// ----------------------------------------------  websocket.send하는데 주요 함수들.
// makeHeader, makeBuffer, mergePacket

function makeHeader(e, t, n) {
    var r = new Array;
    return r.push(_), r.push(k), r.push(Number(e).padLeft(4)), r.push(Number(t).padLeft(6)), r.push(Number(n).padLeft(2)), r
}

function makeBuffer(e) {
    for (var t = 0, n = 0, r = null, i = 0; i < e.length; i++) {
        if (void 0 == e[i] && (e[i] = new Uint8Array(0)), !(e[i] instanceof Uint8Array)) {
            for (var a = new ArrayBuffer(e[i].toString().length),
                o = new Uint8Array(a), s = 0;
                
                s < e[i].toString().length;

                s++)
                o[s] = e[i].toString().charCodeAt(s);
            e[i] = o
        }
        n += e[i].byteLength
    }
    r = new Uint8Array(n);
    for (var i = 0; i < e.length; i++) r.set(e[i], t), t += e[i].byteLength;
    return r
}

function mergePacket(e, t) {
    if (!e && !t)
        throw "Please specify valid arguments for parameters header and body.";
    if (!t || 0 === t.byteLength) return e;
    if (!e || 0 === e.byteLength) return t;
    if (Object.prototype.toString.call(e) !== Object.prototype.toString.call(t))
        throw "The types of the two arguments passed for parameters header and body do not match.";
    var n = new e.constructor(e.byteLength + t.byteLength);
    return n.set(e), n.set(t, e.byteLength), n.buffer
}

// ----------------------------------------------  Websocket 메세지 읽는데 필요한 주요 함수들
// readBuffer, parseMessage

function readBuffer(e) {
    var t = Buffer.from(e);
    // Accidentally passed `e` instead `t`. Returns `serviceCode: 0, retCode: 0, and packet: []`
    process.stdout.write(JSON.stringify(parseMessage(t)));
}

function parseMessage(e) {
    var t = e.slice(0, 14),
        n = e.slice(14, e.byteLength),
        r = readInt(t.slice(2, 6)),
        i = (readInt(t.slice(6, 12)), readInt(t.slice(12, 14))),
        a = readBody(n, i),
        o = { serviceCode: r, retCode: i, packet: a };
    return i > 0 ? void 0 : o
}


// ---------------------------------------------- 유틸리티

Number.prototype.padLeft = function(e, t) { return Array(e - String(this).length + 1).join(t || "0") + this }, Number.prototype.convertSecondToTime = function() {
    var e = arguments.length > 0 && void 0 !== arguments[0] && arguments[0],
        t = parseInt(this),
        n = Math.floor(t / 3600),
        r = Math.floor((t - 3600 * n) / 60),
        i = t - 3600 * n - 60 * r;
    n < 10 && (n = "0" + n), r < 10 && (r = "0" + r), i < 10 && (i = "0" + i);
    var a = n + ":" + r + ":" + i;
    if (e) { var o = (this - t).toFixed(2).split(".")[1]; return a += "." + o.substring(0, 1) }
    return a
}

function readInt(e) {
    for (var t = new Int8Array(e), n = "", r = 0; r < e.byteLength; r++)
        n += String.fromCharCode(t[r]);
    return Number(n)
}

function stringToUint(e) {
    try {
        var e = unescape(encodeURIComponent(e))
    } catch (t) {
        var e = unescape(e)
    }
    for (var t = e.split(""), n = [], r = 0; r < t.length; r++)
        n.push(t[r].charCodeAt(0));
    return new Uint8Array(n)
}

function packetError(a) {
    process.stderr.write("ERROR parsing message: " + a);
}

// function received(a) {
//     process.stdout.write(JSON.stringify(a))
// }

function readInt(e) {
    for (var t = new Int8Array(e), n = "", r = 0; r < e.byteLength; r++)
        n += String.fromCharCode(t[r]);
    return Number(n)
}

function readBody(e, t) {
    for (var n = new Uint8Array(e), r = [], i = 0, a = 0, o = 1; o < e.byteLength; o++)
        n[o] != w.charCodeAt() ?
            (void 0 == r[i] && (r[i] = new Array), r[i][a] = n[o], a++) :
            (void 0 == r[i] && (r[i] = new Array), i++, a = 0);
        for (var o = 0; o < r.length; o++)
            r[o] = uintToString(new Uint8Array(r[o]), t);
    return r
}

function uintToString(e, t) {
    var n = String.fromCharCode.apply(null, e);
    try {
        var r = decodeURIComponent(escape(n))
    } catch (e) {
        var r = escape(n)
    }
    return r;
}

// Export되는 함수들은 단 4개.

module.exports = {
    keepAlive: keepAlive,
    login: login,
    joinch: joinch,
    readBuffer: readBuffer
}