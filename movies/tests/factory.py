from factory.django import DjangoModelFactory
from movies.models import Collection
from django.contrib.auth.models import User
import factory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: 'madhan{0}nadar'.format(n))
    password = factory.Sequence(lambda n: 'madhannadar@{0}'.format(n))


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    collection_user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: 'Movie collection-{0})'.format(n))
    description = factory.Faker("sentence")
    movies = factory.List([
        factory.Dict({
            "title": factory.Sequence(lambda n: 'D%se' % ('o' * n)),
            "description": factory.Faker("sentence"),
            "genres": factory.Faker('random_element',
                                    elements=["Action", "Drama",
                                              "Thriller", "Mystery"]),
            "uuid": factory.Faker('uuid4')
        })
    ])
    created_by = 1
    created_at = 1
