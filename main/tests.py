from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project, Position, Application, Transaction, Chat, Message
from decimal import Decimal

class ModelTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_project_creation(self):
        """Test Project model creation"""
        project = Project.objects.create(
            user=self.user,
            name='Test Project',
            description='A test project description',
            stage='Idea',
            category='Technology',
            funding_goal=Decimal('1000.00')
        )
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.user, self.user)
        self.assertEqual(project.funding_goal, Decimal('1000.00'))
        self.assertEqual(str(project), 'Test Project')
        
    def test_position_creation(self):
        """Test Position model creation"""
        project = Project.objects.create(
            user=self.user,
            name='Test Project',
            description='A test project description',
            stage='Idea',
            category='Technology'
        )
        position = Position.objects.create(
            project=project,
            title='Developer',
            description='Python developer needed',
            compensation_type='paid'
        )
        self.assertEqual(position.title, 'Developer')
        self.assertEqual(position.project, project)
        self.assertEqual(position.compensation_type, 'paid')
        
    def test_application_creation(self):
        """Test Application model creation"""
        project = Project.objects.create(
            user=self.user,
            name='Test Project',
            description='A test project description',
            stage='Idea',
            category='Technology'
        )
        position = Position.objects.create(
            project=project,
            title='Developer',
            description='Python developer needed',
            compensation_type='paid'
        )
        applicant = User.objects.create_user(
            username='applicant',
            email='applicant@example.com',
            password='testpass123'
        )
        application = Application.objects.create(
            position=position,
            applicant=applicant,
            reason='I want to contribute',
            experience='5 years of Python'
        )
        self.assertEqual(application.applicant, applicant)
        self.assertEqual(application.position, position)
        
    def test_transaction_creation(self):
        """Test Transaction model creation"""
        project = Project.objects.create(
            user=self.user,
            name='Test Project',
            description='A test project description',
            stage='Idea',
            category='Technology'
        )
        transaction = Transaction.objects.create(
            user_address='0x1234567890123456789012345678901234567890',
            tx_hash='0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            amount_eth=Decimal('0.5'),
            project=project
        )
        self.assertEqual(transaction.amount_eth, Decimal('0.5'))
        self.assertEqual(transaction.project, project)
        
    def test_chat_creation(self):
        """Test Chat model creation"""
        chat = Chat.objects.create(
            user=self.user,
            message='Hello AI',
            response='Hello! How can I help you?'
        )
        self.assertEqual(chat.user, self.user)
        self.assertEqual(chat.message, 'Hello AI')
        self.assertEqual(chat.response, 'Hello! How can I help you?')

class ViewTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_home_view(self):
        """Test home view loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
    def test_blog_view(self):
        """Test blog view loads correctly"""
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        
    def test_login_view(self):
        """Test login view loads correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
    def test_register_view(self):
        """Test register view loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

class ProjectFunctionalityTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_project_funding_calculation(self):
        """Test project funding calculation methods"""
        project = Project.objects.create(
            user=self.user,
            name='Test Project',
            description='A test project description',
            stage='Idea',
            category='Technology',
            funding_goal=Decimal('1000.00')
        )
        
        # Test with no transactions
        self.assertEqual(project.current_funding(), 0)
        self.assertEqual(project.funding_percentage(), 0)
        
        # Add a transaction
        Transaction.objects.create(
            user_address='0x1234567890123456789012345678901234567890',
            tx_hash='0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            amount_eth=Decimal('500.00'),
            project=project
        )
        
        # Test funding calculation
        self.assertEqual(project.current_funding(), Decimal('500.00'))
        self.assertEqual(project.funding_percentage(), 50)
        
        # Add another transaction to exceed goal
        Transaction.objects.create(
            user_address='0x1234567890123456789012345678901234567891',
            tx_hash='0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567891',
            amount_eth=Decimal('600.00'),
            project=project
        )
        
        # Test funding calculation (should cap at 100%)
        self.assertEqual(project.current_funding(), Decimal('1100.00'))
        self.assertEqual(project.funding_percentage(), 100)
