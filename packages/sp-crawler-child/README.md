---
title: kearch specialist search engine crawler-child API
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

<h1 id="kearch-specialist-search-engine-crawler-child-api">kearch specialist search engine crawler-child API v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

kearch specialist search engine crawler-child API

Base URLs:

* <a href="{scheme}://{sp_host}:{port}/sp/crawler-child">{scheme}://{sp_host}:{port}/sp/crawler-child</a>

    * **scheme** -  Default: http

        * http

        * https

    * **sp_host** -  Default: sp-crawler-child.kearch.svc.cluster.local

    * **port** -  Default: 10080

<h1 id="kearch-specialist-search-engine-crawler-child-api-default">Default</h1>

## get__crawl_a_page

`GET /crawl_a_page`

<h3 id="get__crawl_a_page-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|url|query|string|false|none|

> Example responses

> 200 Response

```json
{
  "url": "string",
  "title": "string",
  "text": "string",
  "tfidf": {
    "lisp": 0.91
  },
  "inner_links": [
    "string"
  ],
  "outer_links": [
    "string"
  ]
}
```

<h3 id="get__crawl_a_page-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="get__crawl_a_page-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» url|string|false|none|none|
|» title|string|false|none|none|
|» text|string|false|none|none|
|» tfidf|[Tfidf](#schematfidf)|false|none|none|
|»» **additionalProperties**|number(float)|false|none|none|
|» inner_links|[string]|false|none|none|
|» outer_links|[string]|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocStfidf">Tfidf</h2>

<a id="schematfidf"></a>

```json
{
  "lisp": 0.91
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|**additionalProperties**|number(float)|false|none|none|

