"""Service availability smoke tests."""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
class TestServiceAvailability:
    """Quick smoke tests to verify all services are running."""

    def test_frontend_loads(self, page: Page, base_url: str):
        """Test frontend is accessible."""
        page.goto(base_url)
        expect(page).to_have_title("Notes Application")
        expect(page.locator("h1")).to_contain_text("Notes Application")

    def test_users_service_accessible(self, page: Page, base_url: str):
        """Test Users Service is responding."""
        page.goto(base_url)
        
        # Check that user list loads (not showing error)
        user_list = page.locator("#user-list")
        expect(user_list).not_to_contain_text("An error occurred", timeout=10000)

    def test_notes_service_accessible(self, page: Page, base_url: str):
        """Test Notes Service is responding."""
        page.goto(base_url)
        
        # Check that note list loads (not showing error)
        note_list = page.locator("#note-list")
        expect(note_list).not_to_contain_text("An error occurred", timeout=10000)

    def test_all_sections_visible(self, page: Page, base_url: str):
        """Test all major sections are rendered."""
        page.goto(base_url)

        expect(page.locator("h2:has-text('User Management')")).to_be_visible()
        expect(page.locator("h2:has-text('Notes Management')")).to_be_visible()
        expect(page.locator("#user-form")).to_be_visible()
        expect(page.locator("#note-form")).to_be_visible()