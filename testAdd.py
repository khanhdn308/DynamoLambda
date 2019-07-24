import unittest
from app import addMovie

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(addMovie(), {
  "ResponseMetadata": {
    "RequestId": "1RFVFCTD5C1CMFS2LNCHJPEGE7VV4KQNSO5AEMVJF66Q9ASUAAJG",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "server": "Server",
      "date": "Tue, 23 Jul 2019 10:00:55 GMT",
      "content-type": "application/x-amz-json-1.0",
      "content-length": "2",
      "connection": "keep-alive",
      "x-amzn-requestid": "1RFVFCTD5C1CMFS2LNCHJPEGE7VV4KQNSO5AEMVJF66Q9ASUAAJG",
      "x-amz-crc32": "2745614147"
    },
    "RetryAttempts": 0
  }
})

