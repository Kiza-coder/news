from django.contrib import admin
from .models import Article



class ArticleAdmin(admin.ModelAdmin):
    
    #colonnes visibles
    list_display = [
        "title",
        "body",
        "author",
    ]
    
    #recherche par titre ou contenu
    search_fields = [
        "title",
        "body",
    ]
    
    #filtres latéraux
    list_filter = [
        "author",
        "created_at",
    ]
    
    #tri du plus récent au plus ancien
    ordering = [
        "author",
        "title",
    ]
    
    #champ non modifiable
    readonly_fields = [
        "created_at",
    ]
    
    #organisation des champs
    fieldsets = [
        ("Infos Principales", {"fields" : ["title","body"]} ),
        ("Auteur & Date", {"fields": ["author", "created_at"]}),
    ]
 
    #champs visibles à la création
    add_fieldsets = [
        (None, {"fields": ["title","body","author"]})
    ]

admin.site.register(Article, ArticleAdmin)