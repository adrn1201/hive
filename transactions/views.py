from django.shortcuts import render

def display_transactions(request):
    return render(request, "transactions/transactions.html")
