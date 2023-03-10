from factory.django import DjangoModelFactory
from movies.models import Collection
from factory import Faker, LazyAttribute, SubFactory, Sequence, Dict
from django.contrib.auth.models import User
import factory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = Sequence(lambda n: 'madhan{0}nadar'.format(n))
    password = Sequence(lambda n: 'madhannadar@{0}'.format(n))


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    collection_user = SubFactory(UserFactory)
    title = Sequence(lambda n: 'Movie collection-{0})'.format(n))
    description = Faker("sentence")
    movies = factory.List([
        factory.Dict({
            "title": Sequence(lambda n: 'D%se' % ('o' * n)),
            "description": Faker("sentence"),
            "genres": factory.Faker('random_element',elements=["Action","Drama","Thriller","Mystery"]),
            "uuid": Faker('uuid4')
        })
    ])
    created_by = 1
    created_at = 1
