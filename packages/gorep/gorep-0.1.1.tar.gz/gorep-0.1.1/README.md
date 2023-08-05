# gorep - Gor Grep Middleware.

Gor Middleware, 过滤掉不符合 PATTERN 的 Request/Response。

## 安装

```bash
pip install gorep
```

## 使用

```bash
$gorep --help

Usage: gorep [OPTIONS] PATTERN

  仅输出匹配 PATTERN 的消息。

  默认情况下搜索 Request 和 Response。如果需要仅搜索其中一个，则需要明确指定（-Q, -S）。

  默认情况下搜素 HTTP Headers 和 Body 字段。如果需要搜索其他字段，则需要明确指定，比如 -mphb 表示搜索 Method,
  Path, Headers, Body。

  典型用法：

  gor --input-raw-track-response --input-raw :80 --output-stdout
  --middleware "gorep something"

Options:
  -Q, --request      搜索 HTTP Request.
  -S, --response     搜索 HTTP Response.
  -m, --method       搜索 HTTP Method.
  -p, --path         搜索 HTTP Path.
  -v, --version      搜索 HTTP Version.
  -c, --status-code  搜索 HTTP Status Code.
  -t, --status-text  搜索 HTTP Status Text.
  -h, --headers      搜索 HTTP Headers.
  -b, --body         搜索 HTTP Body.
  --help             Show this message and exit.
```
