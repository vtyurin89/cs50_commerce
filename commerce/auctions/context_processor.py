
"""
main menu
"""
menu = [{'title': "Active listings", 'url_name': 'index', 'menu_pos': 1},
       {'title': "Categories", 'url_name': 'categories', 'menu_pos': 2},
       {'title': "Watchlist", 'url_name': 'watchlist', 'menu_pos': 3, 'needs_authentication': True},
       {'title': "Create Listing", 'url_name': 'create_listing', 'menu_pos': 4, 'needs_authentication': True},
]


def standard_interface(request):
    return {'menu': menu}