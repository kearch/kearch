---
title: kearch specialist search engine query processor API
language_tabs: []
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<h1 id="kearch-specialist-search-engine-query-processor-api">kearch specialist search engine query processor API v0.1.0</h1>

> Scroll down for example requests and responses.

kearch specialist search engine query processor API

Base URLs:

* <a href="{scheme}://{sp_host}:{port}/sp/query-processor">{scheme}://{sp_host}:{port}/sp/query-processor</a>

    * **scheme** -  Default: http

        * http

        * https

    * **sp_host** -  Default: sp-query-processor.kearch.svc.cluster.local

    * **port** -  Default: 10080

<h1 id="kearch-specialist-search-engine-query-processor-api-default">Default</h1>

## get__retrieve

`GET /retrieve`

<h3 id="get__retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|query|query|string|true|none|
|max_urls|query|integer|true|none|

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

