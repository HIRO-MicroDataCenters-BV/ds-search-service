# ds_search_service.DecentralizedSearchApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**decentralized_search**](DecentralizedSearchApi.md#decentralized_search) | **POST** /search/ | Decentralized Search Across Catalogs


# **decentralized_search**
> str decentralized_search(catalog_filters)

Decentralized Search Across Catalogs

Search the across catalogs with dataset list.  The request accepts filters as a JSON-LD object in the body.  ### Format: Filters are structured as nested JSON-LD objects. Each filter defines the path to the field with optional operators or language annotations.  for details, check ds-catalog-service documentation. https://hiro-microdatacenters-bv.github.io/ds-catalog/docs/index.html

### Example


```python
import ds_search_service
from ds_search_service.models.catalog_filters import CatalogFilters
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
    catalog_filters = ds_search_service.CatalogFilters() # CatalogFilters | 

    try:
        # Decentralized Search Across Catalogs
        api_response = api_instance.decentralized_search(catalog_filters)
        print("The response of DecentralizedSearchApi->decentralized_search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DecentralizedSearchApi->decentralized_search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **catalog_filters** | [**CatalogFilters**](CatalogFilters.md)|  | 

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

