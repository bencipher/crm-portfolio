from django.test import TestCase, Client
from crm.models import Agent, Lead
from users.models import CustomUser

# Create your tests here.
client = Client()
content_type = "application/json"


class AgentsTest(TestCase):
    """pass"""

    @classmethod
    def setUpTestData(cls):
        user_data = {
            "id": 1,
            "password": "testuserpass",
            "username": "testusername",
            "first_name": "Benjamin",
            "last_name": "Cipher",
            "email": "testuseremail@mail.com"
        }
        user = CustomUser.objects.create_user(**user_data)
        agent = Agent.objects.create(user=user, id=1)
        agent.save()

        # factory = APIRequestFactory()

    def test_user_object(self):
        user = CustomUser.objects.get(id=1)
        expected_object_email = f"{user.email}"
        self.assertEqual(expected_object_email, 'testuseremail@mail.com')
        expected_object_name = f"{user.first_name} {user.last_name}"
        self.assertEqual(expected_object_name, 'Benjamin Cipher')

    def test_agent_object(self):
        agent = Agent.objects.get(id=1)
        expected_object_email = f"{agent.user.email}"
        self.assertEqual(expected_object_email, 'testuseremail@mail.com')
        expected_object_name = f"{agent.user.first_name} {agent.user.last_name}"
        self.assertEqual(expected_object_name, 'Benjamin Cipher')

    def test_retrieve_single_agent(self):
        browser = Client()
        login_payload = {
            "email": "testuseremail@mail.com",
            "password": "testuserpass",
        }

        login_response = browser.post(path="/gateway/login/", data=login_payload,
                                      content_type="application/json", follow=True,
                                      secure=False, HTTP_ACCEPT='application/json')
        agent_id = Agent.objects.first().id
        response = browser.get(path="/agents/{}".format(agent_id), follow=True,
                               secure=False,
                               HTTP_ACCEPT='application/json', content_type="application/json",
                               headers={'Authorization': login_response.data['access'].decode()}
                               )
        self.assertEqual(response.status_code, 200)

    def test_get_all_agents(self):
        browser = Client()
        login_payload = {
            "email": "testuseremail@mail.com",
            "password": "testuserpass",
        }

        login_response = browser.post(path="/gateway/login/", data=login_payload,
                                      content_type="application/json", follow=True,
                                      secure=False, HTTP_ACCEPT='application/json', )
        response = browser.get(path="/agents", follow=True,
                               secure=False,
                               HTTP_ACCEPT='application/json', content_type="application/json",
                               headers={'Authorization': login_response.data['access'].decode()}
                               )
        self.assertEqual(response.status_code, 200)

    def test_update_agent(self):
        browser = Client()
        login_payload = {
            "email": "testuseremail@mail.com",
            "password": "testuserpass",
        }
        agent_data = {
            "user": {
                "email": "testuseremail@mail.com",
                "password": "testuserpass",
                "username": "testuser2",
                "first_name": "Test two",
                "last_name": "User"
            }
        }
        login_response = browser.post(path="/gateway/login/", data=login_payload,
                                      content_type="application/json", follow=True,
                                      secure=False, HTTP_ACCEPT='application/json')
        agent_id = Agent.objects.first().id
        response = browser.put(path="/agents/{}".format(agent_id),
                               data=agent_data, follow=True,
                               secure=False,
                               HTTP_ACCEPT='application/json', content_type="application/json",
                               headers={'Authorization': login_response.data['access'].decode()})
        self.assertEqual(response.status_code, 200)


class LeadTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_data = {
            "id": 1,
            "password": "testuserpass",
            "username": "testusername",
            "first_name": "Benjamin",
            "last_name": "Cipher",
            "email": "test@mail.com"
        }
        user = CustomUser.objects.create_user(**user_data)
        agent = Agent.objects.create(user=user, id=1)
        agent.save()
        lead_data = {
            "first_name": "Lead",
            "last_name": "One",
            "email": "leadone@mail.com",
            "stage": "New",
            "source": "Facebook",
            "marital_status": "MARRIED",
            "gender": "FEMALE",
            "assignee": agent

        }
        lead = Lead.objects.create(**lead_data)
        lead.save()

    def test_get_all_leads(self):
        browser = Client()
        login_payload = {
            "email": "test@mail.com",
            "password": "testuserpass",
        }

        login_response = browser.post(path="/gateway/login/", data=login_payload,
                                      content_type="application/json", follow=True,
                                      secure=False, HTTP_ACCEPT='application/json')
        response = browser.get(path="/leads", follow=True,
                               secure=False,
                               HTTP_ACCEPT='application/json', content_type="application/json",
                               headers={'Authorization': login_response.data['access'].decode()}
                               )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_single_lead(self):
        browser = Client()
        login_payload = {
            "email": "test@mail.com",
            "password": "testuserpass",
        }

        login_response = browser.post(path="/gateway/login/", data=login_payload,
                                      content_type="application/json", follow=True,
                                      secure=False, HTTP_ACCEPT='application/json')
        lead_id = Lead.objects.first().id
        response = browser.get(path="/leads/{}".format(lead_id), follow=True,
                               secure=False,
                               HTTP_ACCEPT='application/json', content_type="application/json",
                               headers={'Authorization': login_response.data['access'].decode()})
        self.assertEqual(response.status_code, 200)

    def test_update_lead(self):
        browser = Client()
        login_payload = {
            "email": "test@mail.com",
            "password": "testuserpass",
        }
        agent = Agent.objects.first()
        lead_data = {
            "first_name": "Lead",
            "last_name": "One",
            "email": "leadone@mail.com",
            "stage": "New",
            "source": "Google",
            "marital_status": "SINGLE",
            "gender": "MALE",
            "assignee": agent.id
        }
        login_response = browser.post(path="/gateway/login/", data=login_payload,
                                      content_type="application/json", follow=True,
                                      secure=False, HTTP_ACCEPT='application/json')
        lead_id = Lead.objects.first().id
        response = browser.put(path="/leads/{}".format(lead_id),
                               data=lead_data, follow=True,
                               secure=False,
                               HTTP_ACCEPT='application/json', content_type="application/json",
                               headers={'Authorization': login_response.data['access'].decode()})
        self.assertEqual(response.status_code, 200)
