from django.contrib import admin
from .models import Section, Product, Article, Review, ReviewProductRelation, Order, OrderProductRelation


class ReviewProductRelationInline(admin.TabularInline):
    model = ReviewProductRelation
    extra = 0


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewProductRelationInline]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderProductRelation)
class OrderProductRelationAdmin(admin.ModelAdmin):
    pass


class OrderProductRelationInline(admin.TabularInline):
    model = OrderProductRelation
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductRelationInline]
