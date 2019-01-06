# openapi_client.DefaultApi

All URIs are relative to *https://localhost:32500/v0/sp/gateway*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_a_conenction_request_post**](DefaultApi.md#add_a_conenction_request_post) | **POST** /add_a_conenction_request | Add a connection request sent from meta server to specialist server.
[**delete_a_conenction_request_delete**](DefaultApi.md#delete_a_conenction_request_delete) | **DELETE** /delete_a_conenction_request | Delete a connection request sent from meta server to specialist server.
[**get_a_summary_get**](DefaultApi.md#get_a_summary_get) | **GET** /get_a_summary | Get summary of this specialist server.
[**retrieve_get**](DefaultApi.md#retrieve_get) | **GET** /retrieve | Retrieve search results.


# **add_a_conenction_request_post**
> InlineResponse200 add_a_conenction_request_post(connection_request_on_sp)

Add a connection request sent from meta server to specialist server.

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
connection_request_on_sp = openapi_client.ConnectionRequestOnSP() # ConnectionRequestOnSP | A connection request.

try:
    # Add a connection request sent from meta server to specialist server.
    api_response = api_instance.add_a_conenction_request_post(connection_request_on_sp)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->add_a_conenction_request_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_request_on_sp** | [**ConnectionRequestOnSP**](ConnectionRequestOnSP.md)| A connection request. | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_a_conenction_request_delete**
> InlineResponse200 delete_a_conenction_request_delete(me_host=me_host)

Delete a connection request sent from meta server to specialist server.

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
me_host = 'me_host_example' # str | A meta host name of the connection request to delete. (optional)

try:
    # Delete a connection request sent from meta server to specialist server.
    api_response = api_instance.delete_a_conenction_request_delete(me_host=me_host)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->delete_a_conenction_request_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **me_host** | **str**| A meta host name of the connection request to delete. | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_a_summary_get**
> Summary get_a_summary_get(me_host=me_host)

Get summary of this specialist server.

### Example
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openapi_client.DefaultApi()
me_host = 'me_host_example' # str | A host name of the meta server. (optional)

try:
    # Get summary of this specialist server.
    api_response = api_instance.get_a_summary_get(me_host=me_host)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->get_a_summary_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **me_host** | **str**| A host name of the meta server. | [optional] 

### Return type

[**Summary**](Summary.md)

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

