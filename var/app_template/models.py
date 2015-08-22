# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
logger = logging.getLogger('django')

# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django.db import models
from django.core.urlresolvers import reverse

try:
    from ckeditor.fields import RichTextField as HTMLField
except ImportError:
    try:
        logger.warning('ckeditor not found, trying tinymce')
        from tinymce.models import HTMLField
    except ImportError:
        logger.warning('ckeditor not found, trying tinymce')
        from django.db.models import TextField as HTMLField


# ABSTRACT MODELS
# ---------------------------------------------------------------------------------------------------------------------#
class AbstractBaseModel(models.Model):
    # Quality fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)

    class Meta:
        abstract = True


# BASE MODELS
# ---------------------------------------------------------------------------------------------------------------------#
class BasicModel(models.Model):
    #id = models.AutoField(primary=True)
    slug = models.SlugField(max_length=50)

    char_field = models.CharField(max_length=50, blank=True)
    integer_field = models.IntegerField()
    boolean_field = models.BooleanField(default=False)
    html_field = HTMLField()

    OPTION1 = 'O1'
    OPTION2 = 'O2'

    CHOICES = (
        (OPTION1, 'Option One'),
        (OPTION2, 'Option Two'),
    )
    choice_field = models.CharField(
        max_length=3,
        choices=CHOICES,
        default=OPTION1
    )

    decimal_field = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    date_field = models.DateField(null=True, blank=True)
    email_field = models.EmailField(blank=True)
    url_field = models.URLField(blank=True, null=True)
    image_field = models.ImageField(upload_to='images', null=True, blank=True)

    #Grappelli
    @staticmethod
    def autocomplete_search_fields():
        return "id__iexact", "char_field__icontains"

    # Methods
    def model_method(self):
        if self.choice_field:
            return "%s %s" % (self.get_choicefield_display(), self.char_field)
        else:
            return "%s" % self.char_field

    model_method.admin_order_field = 'char_field'
    model_method.short_description = 'If then display'

    # Overrides
    def get_absolute_url(self):
        return reverse(':basic_model_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return "%s" % (self.char_field.title())

    class Meta:
        managed = True
        app_label = ''

        verbose_name = "Basic Model"
        verbose_name_plural = "Basic Models"
        ordering = ['char_field']
        get_latest_by = "order_date"

        permissions = (('permission_code', 'Human readable permission name'),)
        default_permissions = ('add', 'change', 'delete')

        unique_together = (('email_field', 'char_field'),)


# MODELS
# ---------------------------------------------------------------------------------------------------------------------#
class AdvancedModel(AbstractBaseModel, models.Model):
    description = models.CharField(max_length=45, blank=False)
    fk_basic = models.ForeignKey(BasicModel, null=True, blank=True, verbose_name='Basic Foreignkey Filtered')
    #fk_basic2 = models.ForeignKey(BasicModel, related_name='basic_other', verbose_name='Basic Foreignkey')

    many2many = models.ManyToManyField(BasicModel, related_name='related_many', verbose_name='Many 2 Many Relation')

    def __str__(self):
        return self.description


class ChildModel(BasicModel):
    fk_advanced = models.ForeignKey(AdvancedModel)
    additional_field = models.CharField(max_length=45, blank=False)


class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(blank=True, null=True)
    company = models.ForeignKey('Company', blank=True, null=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=20)
    owner = models.OneToOneField(Person, related_name='comapny_owner')

    def __str__(self):
        return self.name