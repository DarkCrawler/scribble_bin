from fastapi import FastAPI
from kiteconnect import KiteConnect
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/kitelogintest")
async def kiteLoginTest():
    api_key = "f2e0buhl6izq43qa"
    api_secret = '6x4882mb3tksblpqdgm1gw46acebf7qw'

    kite = KiteConnect(api_key=api_key)

    login_url = kite.login_url()
    return RedirectResponse(url=login_url)


@app.get("/kitecallback")
def auth_callback(request_token: str):
    # https://kite.trade/?status=success&request_token=n1bHps7vNAZa3hSuvBwjdpLdE4fQow1V&action=login&type=login
    api_key = "f2e0buhl6izq43qa"
    api_secret = '6x4882mb3tksblpqdgm1gw46acebf7qw'

    kite = KiteConnect(api_key=api_key)
    kite.generate_session(request_token,api_secret=api_secret)

    portfolio = kite.holdings()

    return portfolio
