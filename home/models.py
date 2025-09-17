from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from geomanager.models import Category
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail import blocks
from wagtail.api.v2.utils import get_full_url
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page, Orderable
from wagtailcache.cache import WagtailCacheMixin
from wagtailmetadata.models import MetadataPageMixin

from .blocks import InfoBlock, FeatureBlock


class Navbar(Page):
    max_count = 1
    template = "partials/navbar.html"
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Navbar Logo"),
        help_text=_("A high quality logo image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    menu_links = StreamField(
        [ 
            ("link", blocks.StructBlock(
                [
                    ("name", blocks.CharBlock(max_length=100, label=_("Menu item name"), required=True)),
                    ("url", blocks.URLBlock(label=_("Menu URL"), required=True, help_text="Menu item URL")),
                ],
                icon="link",
            )),
        ],
        blank=True,
        use_json_field=True,
        help_text=_("List of menu items in the navbar"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("logo"),
        MultiFieldPanel(
            [FieldPanel("menu_links")],
            heading=_("Menu Links"),
        ),
    ]
    
class Footer(Page):
    max_count = 1
    template = "partials/footer.html"
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Footer Logo"),
        help_text=_("A high quality footer logo image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Logo Description"),
        help_text=_("A short text to display below the logo"),
    )

    services = StreamField(
        [ (
            "link", blocks.StructBlock(
                [
                    ("name", blocks.CharBlock(max_length=100, label=_("Service name"), required=True)),
                    ("url", blocks.URLBlock(label=_("Service URL"), required=True, help_text="Service URL link")),
                ],
                icon="link",
                ),
        )],
        blank=True,
        use_json_field=True,
        help_text=_("List of link services in the footer"),
    )

    tools_and_data = StreamField(
        [(
            "link", blocks.StructBlock(
                [
                    ("name", blocks.CharBlock(max_length=100, label=_("Tool and Data name"), required=True)),
                    ("url", blocks.URLBlock(label=_("Tool and Data URL"), required=True, help_text="Tool and data URL link")),
                ],
                icon="link",
                ),
        )],
        blank=True,
        use_json_field=True,
        help_text=_("List of tool and data links in the footer"),
    )

    organisation = StreamField([
        (
            "link", blocks.StructBlock(
                [
                    ("name", blocks.CharBlock(max_length=100, label=_("Organisation name"), required=True)),
                    ("url", blocks.URLBlock(label=_("Organisation URL"), required=True, help_text="Organisation URL link")),
                ],
                icon="link",
            ),
        )],
        blank=True,
        use_json_field=True,
        help_text=_("List of organisation links in the footer"),
    )

        # Social media URLs
    facebook = models.URLField(blank=True, help_text="Facebook page URL")
    twitter  = models.URLField(blank=True, help_text="Twitter profile URL")
    youtube  = models.URLField(blank=True, help_text="YouTube channel URL")
    linkedin = models.URLField(blank=True, help_text="LinkedIn page URL")
    github   = models.URLField(blank=True, help_text="GitHub repo URL")
    podcast  = models.URLField(blank=True, help_text="Podcast feed URL")

    #editor interface panels
    content_panels = Page.content_panels + [
        FieldPanel("logo"),
        FieldPanel("description"),

        #grouped panels for each StreamField section
        MultiFieldPanel(
            [FieldPanel("services")],
            heading= "Services",
        ),
        MultiFieldPanel(
            [FieldPanel("tools_and_data")],
            heading="TOOLS & DATA",
        ),
        MultiFieldPanel(
            [FieldPanel("organisation")],
            heading="ORGANISATION",
        ),

        #grouped panels for social links
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("twitter"),
                FieldPanel("youtube"),
                FieldPanel("linkedin"),
                FieldPanel("github"),
                FieldPanel("podcast"),
            ],
            heading="SOCIAL LINKS",
        ),
    ]



class BannerImage(Orderable):
    """A banner image for the home page."""

    id = models.BigAutoField(primary_key=True)  # specify the primary key
    page = ParentalKey("HomePage", related_name="banner_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Banner Image"),
        help_text=_("A high quality banner image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("image"),
    ]


class HomePage(MetadataPageMixin, WagtailCacheMixin, Page):
    template = "home/home_page.html"
    parent_page_type = ["wagtailcore.Page"]
    subpage_types = []
    max_count = 1

    banner_title = models.CharField(max_length=255, verbose_name=_("Banner Title"))
    banner_subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Banner Subtitle"))

    intro_text = RichTextField(
        blank=True,
        null=True,
        features=["bold"],
        verbose_name=_("Introduction text"),
        help_text=_("Introduction section description"),
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Introduction Image"),
        help_text=_("A high quality image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
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
            (
                "feature",
                FeatureBlock(label=_("Feature")),
            ),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name=_("Features"),
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                InlinePanel("banner_images", label=_("Banner Images"), max_num=10),
            ],
            heading=_("Banner Section"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("intro_text"),
                FieldPanel("intro_image"),
            ],
            heading=_("Introduction Section"),
        ),
        FieldPanel("info_blocks"),
        FieldPanel("feature_blocks"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)

        dataset_categories = Category.objects.filter(active=True, public=True)

        context.update({"dataset_categories": dataset_categories})

        mapviewer_url = get_full_url(request, reverse("mapview"))

        context.update({"mapviewer_url": mapviewer_url})

        footer = Footer.objects.live().first()
        context["footer"] = footer
        
        navbar = Navbar.objects.live().first()
        context["navbar"] = navbar
        
        return context

class SiteTheme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text="Name for this theme")
    primary_color = models.CharField(max_length=7, default="#034930", help_text="Main brand color (navbar, footer, primary buttons)")
    secondary_color = models.CharField(max_length=7, default="#198754", help_text="Secondary color (buttons, highlights)")
    accent_color = models.CharField(max_length=7, default="#fbc02d", help_text="Accent color (call-to-action elements)")
    primary_text_color = models.CharField(max_length=7, default="#ffffff", help_text="Main text color")
    secondary_text_color = models.CharField(max_length=7, default="#333333", help_text="Secondary text color")
    background_color = models.CharField(max_length=7, default="#ffffff", help_text="Main background color")
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one active theme
            SiteTheme.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Active)" if self.is_active else self.name

    class Meta:
        verbose_name = "Site Theme"
        verbose_name_plural = "Site Themes" 