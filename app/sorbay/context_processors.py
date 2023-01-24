def host(request):
    """Convienence function to return the host part of the current request"""
    return {"host": request.build_absolute_uri("/")}
