def cart_length(request):
    cart_count = 0
    if request.user.is_authenticated:
        if request.user.cart_db_set.count():
            cart_count = request.user.cart_db_set.count()
                          
    return {'cart_length': cart_count}