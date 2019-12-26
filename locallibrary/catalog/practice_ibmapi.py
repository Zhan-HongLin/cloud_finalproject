# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:12:56 2019

@author: User
"""

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('BDVepx7tCExuwYMxWdSyJhn8ahL3ZN-1AXMQkyXRyghp')
   
service = AssistantV2(
    version='2019-11-28',
    authenticator=authenticator
)

###找出session_id
service.set_service_url('https://gateway.watsonplatform.net/assistant/api')

session_response = service.create_session(
    assistant_id='a7d3a456-718f-4326-8c86-8200f06a9305'
).get_result()

s_id = session_response["session_id"]
# while True:
inputt = input("type something:")

x = service.message(assistant_id='a7d3a456-718f-4326-8c86-8200f06a9305',
                    session_id=s_id,
                    input={
                            'message_type': 'text',
                            'text': inputt
                            }
).get_result()

print(x)
y = x["output"]["generic"]
print(y)
z = y[0]["text"]
print(z)

# print(response("訂位"))



