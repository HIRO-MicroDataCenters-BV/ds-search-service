# ds_search_service.DecentralizedSearchApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**distributed_search**](DecentralizedSearchApi.md#distributed_search) | **POST** /distributed-search/ | Decentralized Search Across Catalogs


# **distributed_search**
> str distributed_search(request_body)

Decentralized Search Across Catalogs

Search the across catalogs with dataset list.  The request accepts filters as a JSON-LD object in the body.  ### Format: Filters are structured as nested JSON-LD objects. Each filter defines the path to the field with optional operators or language annotations.  for details, check ds-catalog-service documentation. https://hiro-microdatacenters-bv.github.io/ds-catalog/docs/index.html

### Example


```python
import ds_search_service
from ds_search_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = ds_search_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with ds_search_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ds_search_service.DecentralizedSearchApi(api_client)
    request_body = None # Dict[str, object] | 

    try:
        # Decentralized Search Across Catalogs
        api_response = api_instance.distributed_search(request_body)
        print("The response of DecentralizedSearchApi->distributed_search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DecentralizedSearchApi->distributed_search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/ld+json, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

