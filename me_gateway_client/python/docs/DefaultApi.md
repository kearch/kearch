# openapi_client.DefaultApi

All URIs are relative to *https://localhost:32400/v0/me/gateway*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_a_conenction_request_post**](DefaultApi.md#add_a_conenction_request_post) | **POST** /add_a_conenction_request | Add a connection request sent from specialist server to meta server.
[**add_a_summary_post**](DefaultApi.md#add_a_summary_post) | **POST** /add_a_summary | Add a summary to meta server.
[**delete_a_conenction_request_delete**](DefaultApi.md#delete_a_conenction_request_delete) | **DELETE** /delete_a_conenction_request | Delete a connection request sent from specialist server to this meta server.
[**retrieve_get**](DefaultApi.md#retrieve_get) | **GET** /retrieve | Retrieve search results.


# **add_a_conenction_request_post**
> InlineResponse2001 add_a_conenction_request_post(connection_request_on_me)

Add a connection request sent from specialist server to meta server.

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
connection_request_on_me = openapi_client.ConnectionRequestOnME() # ConnectionRequestOnME | A connection request.

try:
    # Add a connection request sent from specialist server to meta server.
    api_response = api_instance.add_a_conenction_request_post(connection_request_on_me)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->add_a_conenction_request_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_request_on_me** | [**ConnectionRequestOnME**](ConnectionRequestOnME.md)| A connection request. | 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_a_summary_post**
> InlineResponse200 add_a_summary_post(summary)

Add a summary to meta server.

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
summary = openapi_client.Summary() # Summary | A summary of the specialist server.

try:
    # Add a summary to meta server.
    api_response = api_instance.add_a_summary_post(summary)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->add_a_summary_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **summary** | [**Summary**](Summary.md)| A summary of the specialist server. | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_a_conenction_request_delete**
> InlineResponse2001 delete_a_conenction_request_delete(sp_host=sp_host)

Delete a connection request sent from specialist server to this meta server.

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
sp_host = 'sp_host_example' # str | A specialist host name of the connection request to delete. (optional)

try:
    # Delete a connection request sent from specialist server to this meta server.
    api_response = api_instance.delete_a_conenction_request_delete(sp_host=sp_host)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->delete_a_conenction_request_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sp_host** | **str**| A specialist host name of the connection request to delete. | [optional] 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_get**
> list[Document] retrieve_get(queries=queries, max_urls=max_urls, sp_host=sp_host)

Retrieve search results.

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
queries = 'queries_example' # str | Space-separated query words (optional)
max_urls = 56 # int | Max number of URLs to retrive from specialist servers (optional)
sp_host = 'sp_host_example' # str | A host name to retrieve results from. (optional)

try:
    # Retrieve search results.
    api_response = api_instance.retrieve_get(queries=queries, max_urls=max_urls, sp_host=sp_host)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->retrieve_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queries** | **str**| Space-separated query words | [optional] 
 **max_urls** | **int**| Max number of URLs to retrive from specialist servers | [optional] 
 **sp_host** | **str**| A host name to retrieve results from. | [optional] 

### Return type

[**list[Document]**](Document.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

