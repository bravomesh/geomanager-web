from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailiconchooser.blocks import IconChooserBlock


class InfoBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100,
        label=_("Section Title"),
        help_text=_("Section title"),
    )
    description = blocks.CharBlock(
        max_length=150,
        required=False,
        label=_("Section Description"),
    )

    items = blocks.ListBlock(
        blocks.CharBlock(
            max_length=150,
            label=_("Item"),
        ),
        label=_("Items"),
    )
    image = ImageChooserBlock()

    class Meta:
        template = "blocks/info_block.html"
        icon = "placeholder"
        label = _("Title, Text and Image")


class FeatureBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100,
        label=_("Title"),
    )
    icon = IconChooserBlock(label=_("Icon"))
    description = blocks.CharBlock(
        max_length=150,
        label=_("Description"),
    )
