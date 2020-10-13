

import json
import uvicorn


async def process(scope, receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """

    if scope.get('method', '').lower() not in ['post']:
        return 405, b'Method not allowed'

    headers = {
        key.decode('utf-8'): value.decode('utf-8')
            for key, value in scope.get('headers', tuple())
    }

    message = await receive()
    body = message.get('body', b'{}')
    try:
        request = json.loads(body.decode('utf-8'))
    except Exception:
        request = {}

    if 'accept' in headers and headers.get('accept', '').lower() != 'application/json' and \
            ('name' not in request or 'email' not in request):
        return 406, b'Not acceptable request'

    if ('accept' in headers and headers.get('accept', '').lower() == 'application/json') and \
            (headers.get('content-type', '').lower() == 'application/xml' or
             ('name' not in request and 'email' not in request)):
        return 400, b'Bad request'

    if ('accept' in headers and headers.get('accept', '').lower() == 'application/json') and \
            headers.get('content-type', '').lower() == 'application/json' and \
            ('name' not in request or 'email' not in request):
        return 500, b'Missing or empty name or email '

    return 200,  b'Successful'


async def app(scope, receive, send):
    status_code, message = await process(scope, receive)

    await send({
        'type': 'http.response.start',
        'status': status_code,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': message,
    })


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=9292,
        log_level="debug"
    )

