import sys
import os
import pytest
from unittest.mock import AsyncMock, MagicMock

# Добавляем корень проекта в sys.path
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

@pytest.mark.asyncio
async def test_handle_start():
    """Verify that /start command returns the correct message."""
    from pdf_funnel_output.telegram_bot import handle_start, MSG_START
    
    # Mock message
    message = AsyncMock()
    
    # Call handler
    await handle_start(message)
    
    # Verify
    message.answer.assert_called_once_with(MSG_START)

def test_config_loading():
    """Verify that configuration uses environment variables."""
    from pdf_funnel_output.telegram_bot import BOT_TOKEN
    import os
    
    # We can't easily check if load_dotenv() worked without complex mocking,
    # but we can verify BOT_TOKEN is loaded from somewhere.
    assert BOT_TOKEN is not None
