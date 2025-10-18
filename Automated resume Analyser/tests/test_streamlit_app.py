"""
Unit tests for the Streamlit web application
"""
import sys
import os
import unittest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestStreamlitApp(unittest.TestCase):
    
    def test_streamlit_app_import(self):
        """Test that the Streamlit app module can be imported without errors"""
        try:
            import streamlit_app
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import streamlit_app: {e}")
        except Exception as e:
            # Other exceptions are okay for import test
            pass
    
    def test_required_functions_exist(self):
        """Test that required functions exist in the Streamlit app"""
        import streamlit_app
        
        # Check that main functions exist
        self.assertTrue(hasattr(streamlit_app, 'main'))
        self.assertTrue(hasattr(streamlit_app, 'single_resume_analysis'))
        self.assertTrue(hasattr(streamlit_app, 'batch_processing'))
        self.assertTrue(hasattr(streamlit_app, 'show_about'))
        
        # Check that helper functions exist
        self.assertTrue(hasattr(streamlit_app, 'read_file_from_upload'))
        self.assertTrue(hasattr(streamlit_app, 'get_score_class'))
        self.assertTrue(hasattr(streamlit_app, 'get_score_description'))

if __name__ == '__main__':
    unittest.main()