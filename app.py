import json
import uvicorn


def is_valid_accept_header(headers=None):
    if headers.get('accept', '').lower() == 'application/json':
        return True

    if is_valid_content_type(headers) and headers.get('accept', '').lower() == '*/*':
        return True

    return False


def is_valid_content_type(headers=None):
    if headers.get('content-type', '').lower() == 'application/json':
        return True
    return False


def is_ok_http_method(http_method):
    if http_method in ['post']:
        return True
    return False


def get_payload(message):
    payload_body = message.get('body', b'{}')
    try:
        request = json.loads(payload_body.decode('utf-8'))
    except Exception:
        request = None
    return request


def is_payload_empty(request):
    if request is None or request == {}:
        return True
    return False


def is_payload_valid(request_data):
    _request_data = request_data if request_data else {}
    if 'name' not in _request_data:
        return False

    if 'email' not in _request_data:
        return False

    return True


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

    if not is_valid_accept_header(headers=headers):
        return 406, b'Not acceptable request'

    if not is_valid_content_type(headers=headers):
        return 400, b'Bad request'

    if is_valid_accept_header(headers=headers) and is_valid_content_type(headers=headers) and is_payload_valid(request_data):
        return 200, b'Successful'

    if is_payload_empty(request_data):
        return 400, b'Bad request'
    
    if not is_payload_valid(request_data):
        return 422, b'Missing or empty name or email'

    return 500, b'Error'


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

