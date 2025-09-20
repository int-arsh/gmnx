#!/usr/bin/env python3

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path so we can import ask
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ask import main


class TestAskCLI:
    """Test cases for the ask.py CLI application."""
    
    def test_missing_api_key(self, capsys):
        """Test that the script exits when GEMINI_API_KEY is not set."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            
            captured = capsys.readouterr()
            assert "GEMINI_API_KEY environment variable not set" in captured.out
    
    def test_no_arguments(self, capsys):
        """Test that the script shows usage when no arguments provided."""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'}):
            with patch('ask.genai.Client') as mock_client:
                with pytest.raises(SystemExit) as exc_info:
                    # Simulate no command line arguments
                    with patch.object(sys, 'argv', ['ask.py']):
                        main()
                assert exc_info.value.code == 0
                
                captured = capsys.readouterr()
                assert "Usage: ask" in captured.out
    
    @patch('ask.genai.Client')
    def test_successful_query(self, mock_client_class, capsys):
        """Test successful query execution."""
        # Mock the client and response
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.text = "This is a test response from Gemini"
        mock_client.models.generate_content.return_value = mock_response
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'}):
            with patch.object(sys, 'argv', ['ask.py', 'test question']):
                main()
        
        # Verify the client was called correctly
        mock_client_class.assert_called_once()
        mock_client.models.generate_content.assert_called_once()
        
        # Check that the response was printed (we can't easily test rich output)
        # But we can verify the generate_content was called with correct args
        call_args = mock_client.models.generate_content.call_args
        assert call_args[1]['contents'] == 'test question'
        assert hasattr(call_args[1]['config'], 'system_instruction')
    
    @patch('ask.genai.Client')
    def test_api_error_handling(self, mock_client_class, capsys):
        """Test error handling when API call fails."""
        # Mock client to raise an exception
        mock_client_class.side_effect = Exception("API connection failed")
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'}):
            with patch.object(sys, 'argv', ['ask.py', 'test question']):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                
                captured = capsys.readouterr()
                assert "Error initializing GenAI Client" in captured.out
    
    def test_system_prompt_content(self):
        """Test that the system prompt contains expected content."""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'}):
            with patch('ask.genai.Client') as mock_client_class:
                mock_client = MagicMock()
                mock_client_class.return_value = mock_client
                
                mock_response = MagicMock()
                mock_response.text = "Test response"
                mock_client.models.generate_content.return_value = mock_response
                
                with patch.object(sys, 'argv', ['ask.py', 'test question']):
                    main()
                
                # Check that system prompt contains expected elements
                call_args = mock_client.models.generate_content.call_args
                system_instruction = call_args[1]['config'].system_instruction
                
                assert "command-line assistant" in system_instruction
                assert "Zsh" in system_instruction
                assert "Ubuntu Linux" in system_instruction
                assert "short unless specified" in system_instruction


if __name__ == "__main__":
    pytest.main([__file__])
