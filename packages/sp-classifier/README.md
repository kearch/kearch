---
title: kearch specialist search engine classifier API
language_tabs: []
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<h1 id="kearch-specialist-search-engine-classifier-api">kearch specialist search engine classifier API v0.1.0</h1>

> Scroll down for example requests and responses.

kearch specialist search engine classifier API

Base URLs:

* <a href="{scheme}://{sp_host}:{port}/sp/classifier">{scheme}://{sp_host}:{port}/sp/classifier</a>

    * **scheme** -  Default: http

        * http

        * https

    * **sp_host** -  Default: sp-classifier.kearch.svc.cluster.local

    * **port** -  Default: 10080

<h1 id="kearch-specialist-search-engine-classifier-api-default">Default</h1>

## post__classify

`POST /classify`

> Body parameter

```json
{
  "body_words": [
    "string"
  ],
  "title_words": [
    "string"
  ]
}
```

<h3 id="post__classify-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|A connection request.|

> Example responses

> 200 Response

```json
{
  "result": 0
}
```

<h3 id="post__classify-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="post__classify-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» result|integer|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

