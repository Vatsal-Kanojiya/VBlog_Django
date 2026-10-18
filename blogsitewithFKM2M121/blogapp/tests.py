from django.utils import timezone

from django.test import TestCase
from django.urls import reverse

from .models import Tag, blog, bloguser

BODY = 'word ' * 700  # content needs 3000+ characters


def make_user(email='writer@example.com', idu='1', **extra):
    user = bloguser.objects.create(email=email, idu=idu, first_name='Asha', last_name='Rao', **extra)
    user.set_password('pass12345')
    user.save()
    return user


def make_post(author, title='A post about tags', idb='1', **extra):
    return blog.objects.create(idb=idb, title=title, content=BODY, genre='Tech', author=author,
                               date_of_publish=timezone.now(), likes=0, views=0, **extra)


class TagParseTests(TestCase):
    def test_lowercases_trims_and_dedupes(self):
        self.assertEqual(Tag.parse(' Django,  ORM ,django,, '), ['django', 'orm'])

    def test_drops_names_without_a_slug(self):
        self.assertEqual(Tag.parse('!!!, python'), ['python'])

    def test_get_or_create_reuses_existing_tags(self):
        first = Tag.get_or_create_many(['django'])
        again = Tag.get_or_create_many(['django', 'orm'])
        self.assertEqual(first[0], again[0])
        self.assertEqual(Tag.objects.count(), 2)

    def test_slug_clash_gets_a_suffix(self):
        Tag.get_or_create_many(['c++'])
        tags = Tag.get_or_create_many(['c'])
        self.assertEqual(tags[0].slug, 'c-2')


class TagViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    def test_create_post_saves_tags(self):
        response = self.client.post(reverse('createblog'), {
            'title': 'Testing Django', 'content': BODY, 'genre': 'Tech', 'tags': 'Django, testing',
        })
        self.assertEqual(response.status_code, 200)
        post = blog.objects.get(title='Testing Django')
        self.assertEqual(sorted(t.name for t in post.tags.all()), ['django', 'testing'])

    def test_more_than_five_tags_is_rejected(self):
        self.client.post(reverse('createblog'), {
            'title': 'Too many tags', 'content': BODY, 'genre': 'Tech', 'tags': 'a, b, c, d, e, f',
        })
        self.assertFalse(blog.objects.filter(title='Too many tags').exists())

    def test_tag_page_lists_only_tagged_posts(self):
        tagged = make_post(self.user, title='Tagged post', idb='1')
        make_post(self.user, title='Other post', idb='2')
        tagged.tags.set(Tag.get_or_create_many(['django']))
        response = self.client.get(reverse('tagged', args=['django']))
        self.assertContains(response, 'Tagged post')
        self.assertNotContains(response, 'Other post')

    def test_unknown_tag_is_404(self):
        self.assertEqual(self.client.get(reverse('tagged', args=['nope'])).status_code, 404)

    def test_search_matches_tag_names(self):
        post = make_post(self.user, title='Unrelated title')
        post.tags.set(Tag.get_or_create_many(['postgres']))
        response = self.client.post(reverse('tag'), {'search': 'postgres'})
        self.assertContains(response, 'Unrelated title')
