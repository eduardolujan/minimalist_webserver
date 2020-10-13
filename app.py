import json
import uvicorn


def is_ok_accept_header(headers):
    if 'accept' in headers and headers.get('accept', '').lower() != 'application/json':
        return True
    return False


def is_ok_content_type(headers):
    if headers.get('content-type', '').lower() == 'application/json':
        return True
    return False


def is_ok_http_method(http_method):
    if http_method in ['post']:
        return True
    return False


def is_ok_request(request_data):
    if not request_data:
        return False

    if 'name' not in request_data:
        return False

    if 'email' not in request_data:
        return False

    return True


def get_payload(message):
    payload_body = message.get('body', b'{}')
    try:
        request = json.loads(payload_body.decode('utf-8'))
    except Exception:
        request = None
    return request


async def process(scope, receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    http_method = scope.get('method', '').lower()
    headers = {
        key.decode('utf-8'): value.decode('utf-8')
        for key, value in scope.get('headers', tuple())
    }
    message = await receive()
    request_data = get_payload(message)

    if not is_ok_http_method(http_method):
        return 405, b'Method not allowed'

    elif not is_ok_accept_header(headers):
        return 406, b'Not acceptable request'

    elif not is_ok_content_type(headers):
        return 400, b'Bad request'

    elif not is_ok_request(request_data):
        return 422, b'Missing or empty name or email '

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

