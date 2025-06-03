# ds_search_service.LocalSearchApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**search_catalog**](LocalSearchApi.md#search_catalog) | **POST** /search-catalog/ | Search Local Catalog


# **search_catalog**
> str search_catalog(catalog_filters)

Search Local Catalog

Search the local catalog with dataset list.  The request accepts filters as a JSON-LD object in the body.  ### Format: Filters are structured as nested JSON-LD objects. Each filter defines the path to the field with optional operators or language annotations.  for details, check ds-catalog-service documentation.  https://hiro-microdatacenters-bv.github.io/ds-catalog/docs/index.html#tag/Catalog/operation/get_catalog

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
    api_instance = ds_search_service.LocalSearchApi(api_client)
    catalog_filters = ds_search_service.CatalogFilters() # CatalogFilters | 

    try:
        # Search Local Catalog
        api_response = api_instance.search_catalog(catalog_filters)
        print("The response of LocalSearchApi->search_catalog:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LocalSearchApi->search_catalog: %s\n" % e)
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

