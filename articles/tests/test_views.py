from random import randint

from django.shortcuts import reverse
from django.test import TestCase

from articles.models import Article, Tag


class ViewTest(TestCase):
    @staticmethod
    def random_tags(one_of=4):
        empty = True
        for tag in Tag.objects.iterator():
            if randint(0, one_of - 1) == 0:
                empty = False
                yield tag
        if empty:
            yield Tag.objects.first()

    @classmethod
    def setUpTestData(cls):
        number_of_tags = 10
        number_of_articles = 50

        for tag_num in range(number_of_tags):
            Tag.objects.create(name='tag%s' % tag_num)
        for article_num in range(number_of_articles):
            article = Article.objects.create(
                title='Article %s' % article_num,
                content='Content %s\nArticle for django test.' % article_num
            )
            random_tags = cls.random_tags()
            article.tags.add(*random_tags)

    def test_article_list_view(self):
        url = reverse('articles:list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_tagged_article_list_view(self):
        for tag in Tag.objects.iterator():
            url = reverse('articles:tagged-list', args=[tag])
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)

    def test_article_detail_view(self):
        for article in Article.objects.iterator():
            url = reverse('articles:detail', args=[article.id])
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)

    def test_search_view(self):
        url = reverse('articles:search')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_about_view(self):
        url = reverse('about')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
