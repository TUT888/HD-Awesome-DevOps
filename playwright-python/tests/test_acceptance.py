# Acceptance test
# This is an example test file only, for demonstration of successful running the acceptance test
# Real test involves more complex end-to-end user interaction with frontend UI
import pytest
import os
from playwright.sync_api import Page, expect

FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
USERS_SERVICE_URL = os.getenv('USERS_SERVICE_URL', 'http://localhost:5000')
NOTES_SERVICE_URL = os.getenv('NOTES_SERVICE_URL', 'http://localhost:5001')

# Fixture should be outside the class
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }

@pytest.mark.acceptance
class TestEndToEndUserFlow:
    """Acceptance testing to verify correct end-to-end user flow."""
    
    def test_frontend_loads(self, page: Page):
        """Test that frontend page loads successfully"""
        # Navigate to frontend
        print(FRONTEND_URL)
        page.goto(FRONTEND_URL)
        
        # # Wait for page to load
        page.wait_for_load_state('networkidle')
        
        # Check page content
        expect(page.locator('text=Notes Application')).to_be_visible(timeout=5000)
    
    def test_add_user_workflow(self, page: Page):
        """Test complete add note workflow"""
        # Navigate to frontend
        page.goto(FRONTEND_URL)
        
        # Wait for page to load
        page.wait_for_load_state('networkidle')
        
        # Fill note form (adjust selectors to match your actual form)
        page.fill('input[id="user-username"]', 'User')
        page.fill('input[id="user-email"]', 'anotheruser@gmail.com')
        
        # Submit form
        page.click('button:has-text("Register User")')
        
        # Wait for response
        page.wait_for_timeout(1000)
        
        # Verify note appears in list (adjust selector based on your HTML)
        expect(page.locator('text=anotheruser@gmail.com')).to_be_visible(timeout=5000)

    def test_add_note_workflow(self, page: Page):
        """Test complete add note workflow"""
        # Navigate to frontend
        page.goto(FRONTEND_URL)
        
        # Wait for page to load
        page.wait_for_load_state('networkidle')
        
        # Fill note form (adjust selectors to match your actual form)
        page.fill('input[id="note-user-id"]', '1')
        page.fill('input[id="note-title"]', 'Test Note')
        page.fill('textarea[id="note-content"]', 'Test note content for acceptance testing')
        
        # Submit form
        page.click('button:has-text("Create Note")')
        # Wait for response
        page.wait_for_timeout(1000)
        
        page.fill('input[id="filter-user-id"]', '1')
        page.click('button[id="filter-btn"]')
        # Wait for response
        page.wait_for_timeout(1000)

        # Verify note appears in list (adjust selector based on your HTML)
        expect(page.locator('h3:has-text("Test Note")')).to_be_visible(timeout=5000)

    def test_notes_api_health_check(self, page: Page):
        """Test Notes API endpoint is accessible"""
        response = page.request.get(f"{NOTES_SERVICE_URL}/")
        assert response.status == 200
        
        data = response.json()
        assert 'message' in data or 'status' in data

    def test_users_api_health_check(self, page: Page):
        """Test Users API endpoint is accessible"""
        response = page.request.get(f"{USERS_SERVICE_URL}/")
        assert response.status == 200
        
        data = response.json()
        assert 'message' in data or 'status' in data

    def test_notes_service_health_endpoint(self, page: Page):
        """Test Notes service health endpoint"""
        response = page.request.get(f"{NOTES_SERVICE_URL}/health")
        assert response.status == 200
        
        data = response.json()
        assert data.get('status') == 'ok'

    def test_users_service_health_endpoint(self, page: Page):
        """Test Users service health endpoint"""
        response = page.request.get(f"{USERS_SERVICE_URL}/health")
        assert response.status == 200
        
        data = response.json()
        assert data.get('status') == 'ok'