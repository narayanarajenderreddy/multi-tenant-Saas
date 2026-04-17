def success_response(
    data=None,
    message: str = "Success"
):
    return {
        "success": True,
        "message": message,
        "data": data
    }
    
def error_response(message:str = "something went wrong",error_code:str = "Error"):
    return {
        "success":False,
        "message":message,
        "error_code":error_code
    }   
    
def pagination_response(
    items,
    page,
    size,
    total,
    message:str = "Success"
):
    return {
        "success":True,
        "message":message,
        "data": items,
        "page": page,
        "size": size,
        "total": total
        
    }     
