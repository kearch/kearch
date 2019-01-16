---
title: kearch specialist search engine front API
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - javascript--nodejs: Node.JS
  - ruby: Ruby
  - python: Python
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<h1 id="kearch-specialist-search-engine-front-api">kearch specialist search engine front API v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

kearch specialist search engine front API

Base URLs:

* <a href="{scheme}://{sp_host}:{port}/sp/front">{scheme}://{sp_host}:{port}/sp/front</a>

    * **scheme** -  Default: http

        * http

        * https

    * **sp_host** -  Default: sp-front.kearch.svc.cluster.local

    * **port** -  Default: 10080

<h1 id="kearch-specialist-search-engine-front-api-default">Default</h1>

## get__search

`GET /search`

<h3 id="get__search-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|query|query|string|true|none|

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

<h3 id="get__search-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Search results.|Inline|

<h3 id="get__search-responseschema">Response Schema</h3>

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

