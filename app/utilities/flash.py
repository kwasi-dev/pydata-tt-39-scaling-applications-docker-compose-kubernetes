from fastapi import Request


def flash(request: Request, message: str, messageType: str = "error"):
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append((message, messageType))


def get_flashed_messages(request: Request):
    messages = request.session.pop("_messages", [])
    return messages