from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 2

    # mudar o nome do parametro de page 
    # page_query_param='pagenum'

    # mudar o nome do parametro "max_items" de items
    page_size_query_param='size'
    
    # limitar a quantidade de items 
    max_page_size=8