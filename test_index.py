import json
import unittest
from unittest.mock import patch, MagicMock, Mock
import index

class TestLambdaFunction(unittest.TestCase):
    
    @patch('index.bedrock')
    def test_handler_success(self, mock_bedrock):
        """test successful api call with normal input"""
        # mock the response from the bedrock model
        mock_body = Mock()
        mock_body.read.return_value = json.dumps({
            "results": [
                {"outputText": "This is a test response"}
            ]
        })
        
        mock_bedrock.invoke_model.return_value = {
            "body": mock_body
        }
        
        # test event
        event = {
            "body": "Hello, how are you?"
        }
        
        # execute the handler
        response = index.handler(event, {})
        
        # verify the response
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["body"], "This is a test response")
        self.assertEqual(response["headers"]["Content-Type"], "text/plain")
        self.assertEqual(response["headers"]["Access-Control-Allow-Origin"], "*")
        
        # verify the bedrock model was called with the correct parameters
        mock_bedrock.invoke_model.assert_called_once()
        call_args = mock_bedrock.invoke_model.call_args[1]
        self.assertEqual(call_args["modelId"], "amazon.titan-text-premier-v1:0")
        self.assertEqual(call_args["contentType"], "application/json")
        self.assertEqual(call_args["accept"], "application/json")
        
        # verify payload structure
        payload = json.loads(call_args["body"])
        self.assertEqual(payload["inputText"], "Hello, how are you?")
        self.assertEqual(payload["textGenerationConfig"]["maxTokenCount"], 512)
        self.assertEqual(payload["textGenerationConfig"]["temperature"], 0.5)

    @patch('index.bedrock')
    def test_handler_with_empty_body(self, mock_bedrock):
        """test with empty or missing body"""
        # mock the response from the bedrock model
        mock_body = Mock()
        mock_body.read.return_value = json.dumps({
            "results": [
                {"outputText": "Response to empty input"}
            ]
        })
        
        mock_bedrock.invoke_model.return_value = {
            "body": mock_body
        }
        
        # test event with empty body
        event = {}
        
        # execute the handler
        response = index.handler(event, {})
        
        # verify the response
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["body"], "Response to empty input")
        
        # verify payload had empty string
        call_args = mock_bedrock.invoke_model.call_args[1]
        payload = json.loads(call_args["body"])
        self.assertEqual(payload["inputText"], "")

    @patch('index.bedrock')
    def test_handler_exception(self, mock_bedrock):
        """test exception handling"""
        # make the invoke_model method raise an exception
        mock_bedrock.invoke_model.side_effect = Exception("Test exception")
        
        # test event
        event = {
            "body": "Hello, how are you?"
        }
        
        # execute the handler
        response = index.handler(event, {})
        
        # verify the error response
        self.assertEqual(response["statusCode"], 500)
        self.assertEqual(response["headers"]["Content-Type"], "application/json")
        self.assertEqual(response["headers"]["Access-Control-Allow-Origin"], "*")
        
        # parse the body json and verify the message
        body = json.loads(response["body"])
        self.assertEqual(body["message"], "Internal server error")

    @patch('index.bedrock')
    def test_handler_malformed_response(self, mock_bedrock):
        """test handling of malformed response from bedrock"""
        # mock an incorrect response structure that will cause a keyerror
        mock_body = Mock()
        mock_body.read.return_value = json.dumps({
            "different_key": []  # missing the expected "results" key
        })
        
        mock_bedrock.invoke_model.return_value = {
            "body": mock_body
        }
        
        # test event
        event = {
            "body": "Hello, how are you?"
        }
        
        # execute the handler
        response = index.handler(event, {})
        
        # verify the error response
        self.assertEqual(response["statusCode"], 500)
        body = json.loads(response["body"])
        self.assertEqual(body["message"], "Internal server error")

if __name__ == '__main__':
    unittest.main()