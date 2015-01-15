from django.contrib import admin

from finances.models import Person, Transaction, TransactionItem


# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    list_display = ("nick_name", "email", )


class TransactionItemInline(admin.TabularInline):
    model = TransactionItem


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "entered_by", "total", "description")

    inlines = [
        TransactionItemInline,
    ]

    actions = ['recalculate_debt', ]

    def recalculate_debt(modeladmin, request, queryset):
        for obj in queryset:
            obj.recalculate_debt_graph()
            obj.save()
    recalculate_debt.short_description = "Recalculates the debt graph."


admin.site.register(Person, PersonAdmin)
admin.site.register(Transaction, TransactionAdmin)
#admin.site.register(TransactionItem)
