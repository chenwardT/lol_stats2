from django.db import models

class ItemManager(models.Manager):
    def bulk_create_items(self, item_data):
        """
        Accepts the value of the 'data' key from RiotWatcher's static_get_item_list
        and replaces the table w/the items.

        item_data is expected to be a dict, keyed by the item's ID with values being a
        dict containing:
        -description
        -group
        -item id (repeated)
        -name

        Returns the number of items created.
        """
        to_create = []
        for item in map(lambda x: x[1], item_data.items()):
            to_create.append(Item(item_id=item.get('id'),
                                  description=item.get('description', ''),
                                  plaintext=item.get('plaintext', ''),
                                  group=item.get('group', ''),
                                  name=item.get('name')))
        self.all().delete()
        self.bulk_create(to_create)

        return len(to_create)

class Item(models.Model):
    item_id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True)
    plaintext = models.TextField(blank=True)
    group = models.CharField(max_length=36, blank=True)
    name = models.CharField(max_length=42)

    objects = ItemManager()

    def __str__(self):
        return '{}: {}'.format(self.item_id, self.name)