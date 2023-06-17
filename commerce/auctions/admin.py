from django.contrib import admin

# Register your models here.
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ListingAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'slug', 'cat', 'description', 'image', 'timestamp', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('creator', 'title')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active', 'timestamp', 'cat')


class BidAdmin(admin.ModelAdmin):
    list_display = ('bidder', 'listing', 'bid_amount', 'timestamp')
    list_filter = ('bidder', 'listing',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'comment_author', 'listing', 'timestamp', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('comment_author', 'listing',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)