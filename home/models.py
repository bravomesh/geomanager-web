from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from geomanager.models import Category
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api.v2.utils import get_full_url
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtailcache.cache import WagtailCacheMixin
from wagtailmetadata.models import MetadataPageMixin

from .blocks import InfoBlock, FeatureBlock


class HomePage(MetadataPageMixin, WagtailCacheMixin, Page):
    template = "home/home_page.html"
    parent_page_type = ["wagtailcore.Page"]
    subpage_types = []
    max_count = 1

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_("Banner Image"),
        help_text=_("A high quality banner image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    banner_image_2 = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_("Banner Image 2"),
        help_text=_("Second slide image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    banner_image_3 = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_("Banner Image 3"),
        help_text=_("Third slide image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    banner_title = models.CharField(max_length=255, verbose_name=_('Banner Title'))
    banner_subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Banner Subtitle'))

    intro_text = RichTextField(blank=True, null=True, features=["bold"], verbose_name=_('Introduction text'),
                               help_text=_("Introduction section description"))
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_("Introduction Image"),
        help_text=_("A high quality image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    info_blocks = StreamField(
        [
            ("info", InfoBlock(label=_("Info"))),

        ],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name=_("Info Section"),
    )

    feature_blocks = StreamField(
        [
            ("feature", FeatureBlock(label=_("Feature")),),

        ],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name=_("Features"),
    )

    content_panels = Page.content_panels + [

        MultiFieldPanel(
            [
                FieldPanel('banner_title'),
                FieldPanel('banner_subtitle'),
                FieldPanel('banner_image'),
                FieldPanel('banner_image_2'),
                FieldPanel('banner_image_3'),
            ],
            heading=_("Banner Section"),
        ),


        MultiFieldPanel(
            [
                FieldPanel('intro_text'),
                FieldPanel('intro_image'),
            ],
            heading=_("Introduction Section"),
        ),

        FieldPanel('info_blocks'),
        FieldPanel('feature_blocks'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)

        dataset_categories = Category.objects.filter(active=True, public=True)

        context.update({"dataset_categories": dataset_categories})

        mapviewer_url = get_full_url(request, reverse("mapview"))

        context.update({"mapviewer_url": mapviewer_url})

        return context
