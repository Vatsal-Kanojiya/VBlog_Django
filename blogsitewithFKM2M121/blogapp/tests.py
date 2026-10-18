from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from . import richtext
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
        post = blog.objects.get(title='Testing Django')
        self.assertRedirects(response, reverse('blog', args=[post.idb]))
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


class RichTextTests(TestCase):
    def test_strips_scripts_handlers_and_bad_links(self):
        clean = richtext.clean_html(
            '<p onclick="x()">Hi<script>alert(1)</script> <a href="javascript:alert(1)">x</a></p>')
        self.assertNotIn('script', clean)
        self.assertNotIn('onclick', clean)
        self.assertNotIn('javascript:', clean)

    def test_links_get_safe_rel(self):
        clean = richtext.clean_html('<p><a href="https://example.com">x</a></p>')
        self.assertIn('rel="noopener noreferrer nofollow"', clean)

    def test_only_known_code_languages_keep_their_class(self):
        clean = richtext.clean_html('<pre><code class="language-python">a</code></pre>'
                                    '<pre><code class="language-evil x">b</code></pre>')
        self.assertIn('class="language-python"', clean)
        self.assertNotIn('evil', clean)

    def test_only_uploaded_images_are_kept(self):
        clean = richtext.clean_html('<p>x</p><img src="/mediaM/posts/a.png" alt="ok">'
                                    '<img src="https://tracker.example/p.gif"><img src="/mediaM/posts/../../x">')
        self.assertIn('/mediaM/posts/a.png', clean)
        self.assertNotIn('tracker', clean)
        self.assertNotIn('../', clean)
        self.assertEqual(clean.count('<img'), 1)

    def test_plain_text_becomes_paragraphs_and_is_escaped(self):
        clean = richtext.clean_html('one <b>\ntwo\n\nthree')
        self.assertEqual(clean, '<p>one &lt;b&gt;<br>two</p><p>three</p>')

    def test_code_blocks_are_highlighted_and_stay_escaped(self):
        html = richtext.render_html(richtext.clean_html(
            '<pre><code class="language-python">print("&lt;script&gt;")</code></pre>'))
        self.assertIn('<pre class="highlight" data-lang="Python">', html)
        self.assertIn('<span class="nb">print</span>', html)
        self.assertNotIn('<script>', html)


class PostEditorTests(TestCase):
    def setUp(self):
        self.author = make_user()
        self.post = make_post(self.author, idb='1')

    def form(self, **extra):
        data = {'title': 'Edited title', 'genre': 'Tech', 'tags': 'django',
                'content': '<h2>Intro</h2><p>' + 'word ' * 700 + '</p>'}
        data.update(extra)
        return data

    def test_old_plain_text_post_renders_as_paragraphs(self):
        response = self.client.get(reverse('blog', args=['1']))
        self.assertContains(response, '<article class="post-body">')
        self.assertContains(response, '<p>word word')

    def test_author_can_edit(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('editblog', args=['1']), self.form())
        self.assertRedirects(response, reverse('blog', args=['1']))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Edited title')
        self.assertIn('<h2>Intro</h2>', self.post.content_html)
        self.assertEqual([t.name for t in self.post.tags.all()], ['django'])

    def test_other_user_cannot_edit(self):
        self.client.force_login(make_user(email='other@example.com', idu='2'))
        self.assertEqual(self.client.get(reverse('editblog', args=['1'])).status_code, 403)
        self.assertEqual(self.client.post(reverse('editblog', args=['1']), self.form()).status_code, 403)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'A post about tags')

    def test_anonymous_is_sent_to_login(self):
        response = self.client.get(reverse('editblog', args=['1']))
        self.assertEqual(response.status_code, 302)
        self.assertIn('userlogin', response.url)

    def test_short_post_is_rejected_by_visible_length(self):
        self.client.force_login(self.author)
        # Lots of markup, little text: still too short
        response = self.client.post(reverse('createblog'), self.form(
            title='Short one', content='<p><strong>hi</strong></p>' * 400))
        self.assertContains(response, 'at least 3000 characters')
        self.assertFalse(blog.objects.filter(title='Short one').exists())

    def test_stored_body_is_sanitised(self):
        self.client.force_login(self.author)
        self.client.post(reverse('editblog', args=['1']), self.form(
            content='<p>' + 'word ' * 700 + '<img src=x onerror=alert(1)></p>'))
        self.post.refresh_from_db()
        self.assertNotIn('onerror', self.post.content)

    def test_viewing_counts_without_rerendering(self):
        self.client.get(reverse('blog', args=['1']))
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)
