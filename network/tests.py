from django.test import Client, TestCase
from network.models import User, Post, Follow, Like
from django.urls import reverse
import json

# Create your tests here
class ModelsTestCase(TestCase):
    def setUp(self):
        #create users
        self.alice = User.objects.create_user(username="alice", password="test123")
        self.bob = User.objects.create_user(username="bob", password="test123")
        self.jane = User.objects.create_user(username='jane', password='test123')
        self.tereza = User.objects.create_user(username='tereza', password = 'test123')
        
        #field
        Follow.objects.create(follower = self.bob, following = self.jane)
        Follow.objects.create(follower = self.bob, following = self.tereza)
        Follow.objects.create(follower = self.tereza, following = self.jane)
        
        for i in range(13):
            Post.objects.create(user = self.alice, post_content = "Something...")
            
        Like.objects.create(post = Post.objects.get(pk=1), user = self.bob) #bob liked alice's post
        
    def test_new_post(self):
        self.client.login(username = self.alice.username, password = 'test123')
        response = self.client.post(
            reverse('new'),
            data=json.dumps({
                "post_content": "Something"
                }),
            content_type='application/json'      
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(Post.objects.filter(user = self.alice, post_content = data['post_content']).exists())
        
        
        
    def test_profile(self):
        response = self.client.get(reverse('profile', args = [self.alice.id]))
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username = 'tereza', password = 'test123')
        response = self.client.get(reverse('profile', args = [self.jane.id]))
        self.assertEqual(response.context['field'], 'true')
        #following
        self.assertEqual(response.context['followings'], 0)
        #follower
        self.assertEqual(response.context['followers'], 2)

        
         
        self.client.login(username = 'jane', password = 'test123')
        response = self.client.get(reverse('profile', args = [self.tereza.id]))
        self.assertEqual(response.context['field'], 'false')
        self.assertEqual(response.context['followings'], 1)
        self.assertEqual(response.context['followers'], 1)
        
        
        '''check_like'''
        
    def test_follow_unfollow(self):
        self.client.login(username = self.tereza.username, password = "test123")
        response = self.client.post(
            f"/follow_unfollow/{self.jane.id}",
            data = json.dumps({
                "message": "follow"
                }),
            content_type = "application/json"
        )
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], "You can't follow the same user twice")
        
        response = self.client.post(
            f"/follow_unfollow/{self.bob.id}",
            data=json.dumps({
                "message": "follow"
            }),
            content_type="application/json"
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['follower'], 1)
        self.assertEqual(data['following'], 2)
        
        response = self.client.post(
            reverse('follow', args=[self.jane.id]),
            data=json.dumps({
                "message": "unfollow"
            }),
            content_type="application/json"
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "You have unfollowed successfully")
        self.assertNotIn('error', data)
        self.assertEqual(data['follower'], 1)
        self.assertEqual(data['following'], 0)
        
        
        
    def test_pagination(self):
        response = self.client.get('/?page=1')
        page_obj = response.context["page_obj"]
        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())
        self.assertEqual(page_obj.number, 1)
        self.assertEqual(len(page_obj.object_list), 10)
        
        response = self.client.get("/?page=2")
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_next())
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(len(page_obj.object_list), 3) #change back to equal
        
        
        