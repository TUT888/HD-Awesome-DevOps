"""Pytest configuration for Playwright tests."""
import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope='session')
def base_url():
    """Base URL for the application."""
    return "http://localhost:80"