from wagtail.core import blocks
from django.db import models
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from django.contrib.auth.models import User


# 18 TitleAndTextBlockを定義
class TitleAndTextBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:
        template = "streams/title_and_text_block.html" # 18 テンプレートの場所
        icon = "edit" # 18 admin画面のアイコン
        label = "Title & Text" # 18 admin画面の表示

class ArticleIndexBlock(blocks.StructBlock):
     article_image = ImageChooserBlock(required=True)
     article_title = blocks.CharBlock(required=True, max_length=40, related_name="post_title")
     article_text = blocks.TextBlock(required=True, max_length=200)
     article_url = blocks.URLBlock(required=False)
     article_time = models.DateTimeField(auto_now_add=True)
     like_num = models.IntegerField(default=0)
     like = models.ManyToManyField(User, blank=True, related_name="likes")

     class Meta:
        template = "streams/article_index_block.html" # 18 テンプレートの場所
        icon = "edit" # 18 admin画面のアイコン
        label = "Article" # 18 admin画面の表示
        ordering = ['-date_created']

class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add your title")
    image = ImageChooserBlock(required=True)
    card_title = blocks.CharBlock(required=True, max_length=40)
    text = blocks.TextBlock(required=True, max_length=200)
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False,help_text="If the button page above is selected, that will be used first.")

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "latest Cards"



# 20 追加
class RichtextBlock(blocks.RichTextBlock):

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"

# 22 追加
class SimpleRichtextBlock(blocks.RichTextBlock):

    # 22 field_block.pyからオーバーライド
    def __init__(self, required=True, help_text=None, editor='default', features=None, **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link",
        ]


    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"

# 25 追加
class CTABlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=40)

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"