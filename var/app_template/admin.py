# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
logger = logging.getLogger('django')


# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
# http
#from django.http import HttpResponseRedirect
# contrib
from django.contrib import admin
# # admin
#from django.contrib.admin.views.main import ChangeList
#from django.contrib.admin.util import quote
# # auth
#from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User, Permission
# core
#from django.core.urlresolvers import reverse

# reversion
import reversion

# Import / Export
from import_export.admin import ImportExportMixin
from import_export import resources

from read_only.admin import ReadOnlyAdmin

# 
from .forms import *
from .models import *


# MODEL INLINES
# ---------------------------------------------------------------------------------------------------------------------#
#class AdvancedModelInline(admin.StackedInline):
class AdvancedModelInline(admin.TabularInline):
    model = AdvancedModel  # 1 Foreignkey
    #model = AdvancedModel.many2many.through   # 1 Many2Many
    fk_name = 'fk_basic'  # Multiple Foreignkeys

    fields = ('description', 'fk_basic')

    can_add = True
    can_change = True
    can_delete = False

    verbose_name_plural = 'Plural name here:'
    extra = 2


# RESOURCE CLASSES
# ---------------------------------------------------------------------------------------------------------------------#
class BasicModelResource(resources.ModelResource):

    class Meta:
        model = BasicModel


# MODEL ADMIN
# ---------------------------------------------------------------------------------------------------------------------#
class BasicModelAdmin(ImportExportMixin, reversion.VersionAdmin):
#class BasicModelAdmin(admin.ModelAdmin):
    resource_class = BasicModelResource

    # All fields shortcut
    all = BasicModel._meta.get_all_field_names()

    # Additional fields
    # - by function
    def link_field(self, obj):
        return '<a href="mailto:%s">%s</a>' % (obj.email_field, obj.email_field)

    link_field.allow_tags = True
    link_field.short_description = 'Email'
    link_field.admin_order_field = 'email_field'

    # - by annotation
    def queryset(self, request):
        from django.db.models import Count

        qs = super(BasicModelAdmin, self).queryset(request)
        return qs.annotate(aggregation=Count('email_field'))

    def aggregationfield(self, obj):
        return obj.aggregation
    aggregationfield.short_description = 'Aggregation'
    aggregationfield.admin_order_field = 'aggregation'

    # Change|View list options
    list_display = ('char_field', 'integer_field', 'date_field', 'email_field', 'link_field')
    list_filter = ['date_field', 'integer_field']
    search_fields = ['char_field']

    # Add|Change form options
    fieldsets = [
        (None, {'fields': ['char_field', 'email_field', 'html_field']}),
        ('Heading1', {'fields': ['date_field', ('decimal_field', 'integer_field')]}),
        ('Heading2', {'fields': ['image_field', 'url_field'], 'classes': ['grp-collapse grp-open', ]}),
        #('Admin',    {'fields': ['created_on', 'updated_on' ], 'classes': ['collapse']}),
    ]

    # Inlines
    inlines = [
        AdvancedModelInline,
    ]

    # Admin options
    readonly_fields = ['url_field']

    #def get_changelist(self, request, **kwargs):
    #    return ViewList

class AdvancedModelAdmin(admin.ModelAdmin):
    # Additional fields
    # - by relation
    @staticmethod
    def fk_related_field(obj):
        return obj.fkbasic2.datefield

    fk_related_field.short_description = 'date_field'
    fk_related_field.admin_order_field = 'fk_basic__date_field'

    # Change|View list options
    list_display = ('description', 'fk_basic', 'created_on')
    list_editable = ['fk_basic', ]

    list_filter = ['fk_basic__integer_field', 'updated_on']
    date_hierarchy = 'updated_on'
    search_fields = ['description', 'fk_basic__char_field']

    # Add|Change form options
    fieldsets = [
        #(None, {'fields': ['description', 'fk_basic', 'fkbasic2']}),
        (None, {'fields': ['description', 'fk_basic']}),
        ('Relations', {'fields': ['many2many'], 'classes': ['wide']}),
        ('Quality', {'fields': [('created_on', 'updated_on'), 'note'], 'classes': ['collapse']}),
    ]
    filter_horizontal = ('many2many',)

    # Admin options
    readonly_fields = ['created_on', 'updated_on']

    raw_id_fields = ('fk_basic',)
    autocomplete_lookup_fields = {
        'fk': ['fk_basic'],
    }

    # Overrides
    form = AdvancedModelForm

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.description = 'Newly created!'
        obj.description += 'Just updated!'
        obj.save()


class PersonAdmin(admin.ModelAdmin):
    all = Person._meta.get_all_field_names()
    list_display = [field for field in all if not (field.endswith('_id') or field == 'id' or field.endswith('_ptr'))]

class CompanyAdmin(admin.ModelAdmin):

    # - by annotation
    def queryset(self, request):
        from django.db.models import Count

        qs = super(CompanyAdmin, self).queryset(request)
        return qs.annotate(aggregation=Count('person'))

    @staticmethod
    def aggregation_field(obj):
        return obj.aggregation
    aggregation_field.short_description = 'Employees'
    aggregation_field.admin_order_field = 'aggregation'

    # Change|View list options
    list_display = ('name', 'owner', 'aggregation_field')
    search_fields = ['name', 'owner__name']


admin.site.register(Person, PersonAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(AdvancedModel, AdvancedModelAdmin)
admin.site.register(BasicModel, BasicModelAdmin)