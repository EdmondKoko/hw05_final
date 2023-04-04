from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, Comment, Follow
from ..views import PAGINATOR_POSTS

User = get_user_model()

PAGINATOR_COUNT = 13


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='StasBasov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',

            reverse('posts:group_list',
                    kwargs={
                        'slug': PostViewsTests.group.slug}
                    ): 'posts/group_list.html',

            reverse('posts:profile',
                    kwargs={
                        'username': PostViewsTests.user.username}
                    ): 'posts/profile.html',

            reverse('posts:post_create'): 'posts/create_post.html',

            reverse('posts:post_detail',
                    kwargs={
                        'post_id': PostViewsTests.post.id}
                    ): 'posts/post_detail.html',

            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}
                    ): 'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def post_fields(self, post):
        with self.subTest(post=post):
            self.assertEqual(post.text, self.post.text)
            self.assertEqual(post.id, self.post.id)
            self.assertEqual(post.author, self.post.author)
            self.assertEqual(post.group.id, self.post.group.id)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.post_fields(response.context['page_obj'][0])

    def test_groups_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug})
        )
        self.assertEqual(response.context['group'], self.group)
        self.post_fields(response.context['page_obj'][0])

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}))
        self.assertEqual(response.context['user'], self.user)
        self.post_fields(response.context['page_obj'][0])

    def test_detail_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}))
        self.post_fields(response.context['post'])


class PostPaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug'
        )
        for i in range(13):
            cls.post = Post.objects.create(
                text='Тестовый пост',
                author=cls.user,
                group=cls.group
            )

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_posts(self):
        paginator_list = {
            'posts:index': reverse('posts:index'),
            'posts:group_list': reverse(
                'posts:group_list',
                kwargs={'slug': PostPaginatorTests.group.slug}),
            'posts:profile': reverse(
                'posts:profile',
                kwargs={'username': PostPaginatorTests.user.username}),
        }
        for template, reverse_name in paginator_list.items():
            response = self.client.get(reverse_name)
            self.assertEqual(len(response.context['page_obj']),
                             PAGINATOR_POSTS)

    def test_second_page_contains_ten_posts(self):
        paginator_list = {
            'posts:index': reverse('posts:index') + '?page=2',
            'posts:group_list': reverse(
                'posts:group_list',
                kwargs={'slug': PostPaginatorTests.group.slug}) + '?page=2',
            'posts:profile': reverse(
                'posts:profile',
                kwargs={'username': PostPaginatorTests.user.username}
            ) + '?page=2',
        }
        for template, reverse_name in paginator_list.items():
            response = self.client.get(reverse_name)
            self.assertEqual(len(response.context['page_obj']),
                             PAGINATOR_COUNT - PAGINATOR_POSTS)


class PostCommentTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='StasBasov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_add_comment_authorized_client(self):
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Тестовый пост',
        }
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertTrue(
            Comment.objects.filter(text=self.post.text,
                                   ).exists())
        self.assertEqual(Comment.objects.count(), comment_count + 1)


class PostCacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_cache(self):
        Post.objects.create(
            author=self.user,
            text='Тестовый пост',
        )
        response = self.authorized_client.get(reverse("posts:index"))
        first_response = response.content

        Post.objects.all().delete

        response = self.authorized_client.get(reverse("posts:index"))
        second_response = response.content

        self.assertEqual(first_response, second_response)

        cache.clear()

        response = self.authorized_client.get(reverse("posts:index"))
        third_response = response.content

        self.assertEqual(first_response, third_response)


class PostFollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='StasBasov')
        cls.follower = User.objects.create_user(username='Follower')
        cls.follower_client = Client()
        cls.follower_client.force_login(cls.follower)
        cls.unfollower = User.objects.create_user(username='Unfollow')
        cls.unfollower_client = Client()
        cls.unfollower_client.force_login(cls.unfollower)
        cache.clear()

    def test_follow_and_unfollow(self):
        PostFollowTests.follower_client.get(
            (reverse('posts:profile_follow',
                     kwargs={'username': 'StasBasov'})),
        )
        self.assertEqual(
            Follow.objects.filter(
                user=PostFollowTests.follower,
            ).count(),
            1,
        )
        PostFollowTests.follower_client.get(
            (reverse('posts:profile_unfollow',
                     kwargs={'username': 'StasBasov'})),
        )
        self.assertEqual(
            Follow.objects.filter(user=PostFollowTests.follower).count(),
            0
        )

    def test_follow_index(self):
        Post.objects.create(
            author=PostFollowTests.author,
            text='Тестовый пост',
        )
        Follow.objects.create(
            user=PostFollowTests.follower, author=PostFollowTests.author
        )
        response_follower = PostFollowTests.follower_client.get(
            reverse('posts:follow_index')
        )
        self.assertEqual(
            len(response_follower.context['page_obj']),
            1
        )
        response_unfollower = PostFollowTests.unfollower_client.get(
            reverse('posts:follow_index')
        )
        self.assertEqual(
            len(response_unfollower.context['page_obj']),
            0
        )
