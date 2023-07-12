from django.contrib import admin


from .models import Book, IssuedBooks, IssueRequest


class IssuedBooksAdmin(admin.ModelAdmin):
    list_display = ('issuedby', 'issued_date', 'expiry_date', 'issuerequest')

class IssuerequestAdmin(admin.ModelAdmin):
    list_display = ('book','student','is_issued','issued_date')


admin.site.register(Book)
admin.site.register(IssuedBooks, IssuedBooksAdmin)
admin.site.register(IssueRequest, IssuerequestAdmin)