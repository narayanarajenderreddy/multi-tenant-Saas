def success_response(
    data=None,
    message: str = "Success"
):
    return {
        "success": True,
        "message": message,
        "data": data
    }
