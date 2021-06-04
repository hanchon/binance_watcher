import uuid

import uvicorn
from fastapi import FastAPI
from fastapi import WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import HTMLResponse

app = FastAPI()

PORT = 8000


@app.get('/')
def index():
    return HTMLResponse('''
        <body>
            <h1>BNB/BUSD</h1>
            <h2>Tendency: <span id='tendency'></span></h2>
            <h2>Last Change: <span id='lastChange'>  </span></h2>
            <h2>Bids</h2>
            <table>
            <head>
            <tr>
            <th>Precio</th>
            <th>Cantidad</th>
            <tr>
            </head>
            <tbody id='bids'>
            </tbody>
            </table>
            <h2>Asks</h2>
            <table>
            <head>
            <tr>
            <th>Precio</th>
            <th>Cantidad</th>
            <tr>
            </head>
            <tbody id='asks'>
            </tbody>
            </table>

            <button onClick="fetch('http://127.0.0.1:7000/test').then((r) => r.json().then((msg) => console.log(msg)))">
            Test
            </button>
            <script>
                const ws = new WebSocket('ws://localhost:8000/ws');
                ws.onmessage = (e) => {
                    data = JSON.parse(e.data);
                    console.log(data.pair);
                    console.log(data.key);
                    console.log(data.value)

                    if (data.key == 'bids' || data.key == 'asks'){
                        d = JSON.parse(data.value)
                        var tbody;
                        if (data.key == 'bids') {
                            var tbody = document.getElementById('bids')
                        } else {
                            var tbody = document.getElementById('asks')
                        }
                        while (tbody.firstChild && !tbody.firstChild.remove()) {}
                        d.forEach((e) => {
                            var row = document.createElement("tr");
                            var price = document.createElement("td");
                            price.appendChild(document.createTextNode(e[0]));
                            var amount = document.createElement("td");
                            amount.appendChild(document.createTextNode(e[1]));
                            row.appendChild(price);
                            row.appendChild(amount);
                            tbody.appendChild(row);
                        })
                    }

                }

            </script>
        </body>
    ''')


websockets = {}


@app.get('/broadcast')
async def broadcast(pair: str, key: str, value: str):
    # Make a copy because if it fails and delete a key, we must continue
    keys = list(websockets)

    for w in keys:
        try:
            await websockets[w].send_json({'pair': pair, 'key': key, 'value': value})
        except Exception:
            del websockets[w]
    return {'result': 'Sent'}


@app.websocket_route('/ws')
class WebSocketTicks(WebSocketEndpoint):
    async def on_connect(self, websocket: WebSocket) -> None:
        global websockets
        self.id = uuid.uuid4()
        await websocket.accept()
        websockets[self.id] = websocket

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        global websockets
        del websockets[self.id]


if __name__ == '__main__':
    uvicorn.run(app, port=PORT)
