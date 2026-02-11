def current_location(request):
    return {
        "current_location": request.session.get("location")
    }
