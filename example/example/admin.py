from django.contrib import admin
from .models import Person, Child, Home, Car
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple


class ChildInline(admin.StackedInline):
    model = Child
    extra = 0


class HomeInline(admin.StackedInline):
    model = Home
    extra = 0


class CarInline(admin.StackedInline):
    model = Car
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    inlines = (ChildInline, HomeInline, CarInline)
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }


admin.site.register(Person, PersonAdmin)
admin.site.register(Child, admin.ModelAdmin)
admin.site.register(Home, admin.ModelAdmin)
admin.site.register(Car, admin.ModelAdmin)
