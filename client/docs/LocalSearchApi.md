# ds_search_service.LocalSearchApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**search_catalog**](LocalSearchApi.md#search_catalog) | **POST** /search-catalog/ | Search Local Catalog


# **search_catalog**
> str search_catalog(catalog_filters)

Search Local Catalog

Search the local catalog with dataset list.  The request accepts filters as a JSON-LD object in the body.  ### Format: Filters are structured as nested JSON-LD objects. Each filter defines the path to the field with optional operators or language annotations.  ```json {   \"@context\": {     \"@vocab\": \"http://data-space.org/\",     \"<namespace>\": \"<namespaceURL>\",     ...   }   \"@type\": \"Filters\",   \"filters\": [     {       [\"@type\": \"<[namespace:]Class>\",]       \"<[namespace:]attribute>[@<lang>]\": <nestedObject> | <value> | {         \"operation\": \"<operator>\",         \"operationValue\": <value>       }     },     ...   ] } ```  ### Supported operators: - `gte`, `lte` — range filtering - `in` — list filtering - `contains` — substring search  ### Example: ```json {   \"@context\": {     \"@vocab\": \"http://data-space.org/\",     \"dcat\": \"http://www.w3.org/ns/dcat#\",     \"med\": \"http://med.example.org/\"   },   \"@type\": \"Filters\",   \"filters\": [     {       \"dcat:dataset\": {         \"extraMetadata\": {           \"@type\": \"med:Diagnoses\",           \"med:hasDiagnosis\": {             \"med:code\": {               \"operation\": \"contains\",               \"operationValue\": \"I10\"             }           }         }       }     }   ] } ```  ### More filter examples: - ```json     {         \"dcat:dataset\": {             \"dcterms:title\": \"example\"         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"dcterms:title@en\": \"example\"         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"dcterms:title\": {                 \"@language\": \"en\"             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"dcterms:title\": {                 \"@value\": \"example\"             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"dcat:distribution\": {                 \"dcat:format\": \"PDF\"             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"extraMetadata\": {                 \"med:sex\": \"M\"             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"extraMetadata\": {                 \"@type\": \"med:Patient\",                 \"med:sex\": \"M\"             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"extraMetadata\": {                 \"med:weight\": 75             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"extraMetadata\": {                 \"med:weight\": {                     \"@value\": 75                 }             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"extraMetadata\": {                 \"med:weight\": {                     \"@type\": \"xsd:integer\"                 }             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"dcterms:datePublished\": {                 \"operationValue\": \"2021-01-01\",                 \"operation\": \"gte\"             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"dcterms:datePublished\": {                 \"operationValue\": \"2021-12-31\",                 \"operation\": \"lte\"             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"extraMetadata\": {                 \"med:weight\": {                     \"operationValue\": 70,                     \"operation\": \"gte\"                 }             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"extraMetadata\": {                 \"med:weight\": {                     \"operationValue\": 70,                     \"operation\": \"lte\"                 }             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"dcat:keyword\": {                 \"operationValue\": [\"science\", \"health\"],                 \"operation\": \"in\"             }         }     }   ``` - ```json     {         \"dcat:dataset\": {             \"dcterms:title@en\": {                 \"operationValue\": \"example\",                 \"operation\": \"contains\"             }         }     }   ```

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

