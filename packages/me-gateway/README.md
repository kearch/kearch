---
title: kearch meta search engine gateway API
language_tabs: []
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<h1 id="kearch-meta-search-engine-gateway-api">kearch meta search engine gateway API v0.1.0</h1>

> Scroll down for example requests and responses.

kearch meta search engine gateway API

Base URLs:

* <a href="{scheme}://{me_host}:{port}/v0/me/gateway">{scheme}://{me_host}:{port}/v0/me/gateway</a>

    * **scheme** -  Default: https

        * http

        * https

    * **me_host** -  Default: localhost

    * **port** -  Default: 32400

<h1 id="kearch-meta-search-engine-gateway-api-default">Default</h1>

## post__add_a_summary

`POST /add_a_summary`

*Add a summary to meta server.*

> Body parameter

```json
{
  "sp_host": "string",
  "engine_name": "string",
  "dump": {
    "property1": 0,
    "property2": 0
  }
}
```

<h3 id="post__add_a_summary-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Summary](#schemasummary)|true|A summary of the specialist server.|

> Example responses

> 200 Response

```json
{
  "sp_host": "string",
  "engine_name": "string"
}
```

<h3 id="post__add_a_summary-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|An info about the specialist server of the added summary.|Inline|

<h3 id="post__add_a_summary-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» sp_host|string|false|none|none|
|» engine_name|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## post__add_a_connection_request

`POST /add_a_connection_request`

*Add a connection request sent from specialist server to meta server.*

> Body parameter

```json
{
  "sp_host": "string",
  "engine_name": "string",
  "scheme": "string"
}
```

<h3 id="post__add_a_connection_request-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ConnectionRequestOnME](#schemaconnectionrequestonme)|true|A connection request.|

> Example responses

> 200 Response

```json
{
  "sp_host": "string"
}
```

<h3 id="post__add_a_connection_request-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|An info about the specialist server that requested the connection.|Inline|

<h3 id="post__add_a_connection_request-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» sp_host|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## delete__delete_a_connection_request

`DELETE /delete_a_connection_request`

*Delete a connection request sent from specialist server to this meta server.*

<h3 id="delete__delete_a_connection_request-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|sp_host|query|string|false|A specialist host name of the connection request to delete.|

> Example responses

> 200 Response

```json
{
  "sp_host": "string"
}
```

<h3 id="delete__delete_a_connection_request-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|An info about the specialist server that requested the connection.|Inline|

<h3 id="delete__delete_a_connection_request-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» sp_host|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## get__retrieve

`GET /retrieve`

*Retrieve search results.*

<h3 id="get__retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|queries|query|string|false|Space-separated query words|
|max_urls|query|integer|false|Max number of URLs to retrive from specialist servers|
|sp_host|query|string|false|A host name to retrieve results from.|

> Example responses

> 200 Response

```json
[
  {
    "url": "string",
    "title": "string",
    "description": "string",
    "score": 0
  }
]
```

<h3 id="get__retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Search results.|Inline|

<h3 id="get__retrieve-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Document](#schemadocument)]|false|none|none|
|» url|string|false|none|none|
|» title|string|false|none|none|
|» description|string|false|none|none|
|» score|number|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocSconnectionrequestonme">ConnectionRequestOnME</h2>

<a id="schemaconnectionrequestonme"></a>

```json
{
  "sp_host": "string",
  "engine_name": "string",
  "scheme": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|sp_host|string|false|none|none|
|engine_name|string|false|none|none|
|scheme|string|false|none|none|

<h2 id="tocSsummary">Summary</h2>

<a id="schemasummary"></a>

```json
{
  "sp_host": "string",
  "engine_name": "string",
  "dump": {
    "property1": 0,
    "property2": 0
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|sp_host|string|false|none|none|
|engine_name|string|false|none|none|
|dump|object|false|none|none|
|» **additionalProperties**|integer|false|none|none|

<h2 id="tocSdocument">Document</h2>

<a id="schemadocument"></a>

```json
{
  "url": "string",
  "title": "string",
  "description": "string",
  "score": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|url|string|false|none|none|
|title|string|false|none|none|
|description|string|false|none|none|
|score|number|false|none|none|

