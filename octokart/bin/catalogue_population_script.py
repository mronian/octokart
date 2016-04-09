import os
import sys

DJANGO_PATH='../'
sys.path.insert(0, DJANGO_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octokart.settings')

import django
django.setup()

from seller.models import CatalogueItem

def populate():
    
    item1 = add_item("Samsung Galaxy On5","")
    item2 = add_item("Samsung Galaxy S7 Edge","")
    item3 = add_item("Apple iPhone 6S","")
    item4 = add_item("Apple iPad","")
    item5 = add_item("Apple iMac","")
    item6 = add_item("Micromax Canvas HD2","")
    item7 = add_item("Moto G3","")
    item8 = add_item("Moto X Play","")
    item9 = add_item("Red Mi 4","")
    item10 = add_item("Asus Zenfone 2","")
    item11 = add_item("Lenovo A7000","")
    item12 = add_item("Samsung Galaxy E5","")
    item13 = add_item("Sony Xperia E4","")
    
def add_item(item_name, item_desc):
    
    it=CatalogueItem.objects.get_or_create(name=item_name, desc=item_desc)
    
    return str(it)

def delete_topics():
    
    for t in CatalogueItem.objects.all():
        t.delete()
        

if __name__ =='__main__':
    if sys.argv[1]=='populate': 
        print "Populating Catalogue Database"
        populate()
    elif sys.argv[1]=='delete':
        print "Deleting Catalogue Database"
        delete_topics()