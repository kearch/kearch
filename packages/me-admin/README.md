---
title: kearch meta search engine admin API
language_tabs: []
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<h1 id="kearch-meta-search-engine-admin-api">kearch meta search engine admin API v0.1.0</h1>

> Scroll down for example requests and responses.

kearch meta search engine admin API

Base URLs:

* <a href="{scheme}://{me_host}:{port}/me/admin">{scheme}://{me_host}:{port}/me/admin</a>

    * **scheme** -  Default: http

        * http

        * https

    * **me_host** -  Default: localhost

    * **port** -  Default: 32600

<h1 id="kearch-meta-search-engine-admin-api-default">Default</h1>

## get__login

`GET /login`

<h3 id="get__login-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|username|query|string|true|none|
|password|query|string|true|none|

<h3 id="get__login-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## get__logout

`GET /logout`

<h3 id="get__logout-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__update_password

`POST /update_password`

> Body parameter

```json
{
  "required": null,
  "password": "string",
  "password_again": "string"
}
```

<h3 id="post__update_password-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="post__update_password-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## get__learn_params_for_evaluator

`GET /learn_params_for_evaluator`

<h3 id="get__learn_params_for_evaluator-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__approve_a_connection_request

`POST /approve_a_connection_request`

> Body parameter

```json
{
  "required": null,
  "sp_host": "string"
}
```

<h3 id="post__approve_a_connection_request-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="post__approve_a_connection_request-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## delete__delete_a_connection_request

`DELETE /delete_a_connection_request`

> Body parameter

```json
{
  "required": null,
  "sp_host": "string"
}
```

<h3 id="delete__delete_a_connection_request-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="delete__delete_a_connection_request-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

## post__send_a_connection_request

`POST /send_a_connection_request`

> Body parameter

```json
{
  "required": null,
  "sp_host": "string"
}
```

<h3 id="post__send_a_connection_request-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

<h3 id="post__send_a_connection_request-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|

<aside class="success">
This operation does not require authentication
</aside>

