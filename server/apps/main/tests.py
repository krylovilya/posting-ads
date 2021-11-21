>>> import random

>>> from apps.main.models import Ad, Category, Seller, Tag


>>> tags = [Tag(title=f'test tag {i}') for i in range(10)]
>>> _ = [tag.save() for tag in tags]
>>> categories = [Category(title=f'test category {i}') for i in range(10)]
>>> _ = [category.save() for category in categories]
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> users = [User(username=f'test user {i}') for i in range(3)]
>>> _ = [user.save() for user in users]
>>> sellers = [Seller(user=user) for user in users]
>>> _ = [seller.save() for seller in sellers]


>>> def gen_ad(title, seller, categories_list, tags_list):
...     new_ad = Ad.objects.create(
...         title=title,
...         seller_id=seller.id,
...         category_id=random.choice(categories_list).id
...     )
...     new_ad.tags.add(*(tag.id for tag in random.sample(tags_list, random.randint(3, 5))))
...     new_ad.description = f'this is test ad with tags: {[tag.title for tag in new_ad.tags.all()]}',
...     new_ad.save()
...     return new_ad

>>> ads = [[gen_ad(f'test ad {i} by {seller}', seller, categories, tags) for i in range(random.randint(3, 5))] for seller in sellers]

[[<Ad: self.title [test user 0]>, <Ad: self.title [test user 0]>,
<Ad: self.title [test user 0]>, <Ad: self.title [test user 0]>],
[<Ad: self.title [test user 1]>, <Ad: self.title [test user 1]>,
<Ad: self.title [test user 1]>], [<Ad: self.title [test user 2]>,
<Ad: self.title [test user 2]>, <Ad: self.title [test user 2]>,
<Ad: self.title [test user 2]>, <Ad: self.title [test user 2]>]]


>>> for category in Category.objects.all():
...     filtered_ads = Ad.objects.filter(category=category)
...     if filtered_ads:
...         print(category)
...         print(filtered_ads)

test category 1
<QuerySet [<Ad: self.title [test user 1]>]>
test category 3
<QuerySet [<Ad: self.title [test user 2]>]>
test category 4
<QuerySet [<Ad: self.title [test user 0]>, <Ad: self.title [test user 0]>, <Ad: self.title [test user 1]>]>
test category 5
<QuerySet [<Ad: self.title [test user 2]>]>
test category 7
<QuerySet [<Ad: self.title [test user 2]>]>
test category 8
<QuerySet [<Ad: self.title [test user 1]>, <Ad: self.title [test user 2]>]>
test category 9
<QuerySet [<Ad: self.title [test user 0]>, <Ad: self.title [test user 0]>, <Ad: self.title [test user 2]>]>
