# ***참고자료***

## "HTTP range requests" *from Mozilla*
https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests

## "Range" *from Mozilla*
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range

## Downloading Files from URLs in Python
https://www.codementor.io/@aviaryan/downloading-files-from-urls-in-python-77q3bs0un

## Python을 사용하여, 일부 file만 Download 받는 방법 *from StackOverFlow*
https://stackoverflow.com/a/23602538/10445743


### 첫 100 byte 까지 Download 받기의 예시
```python
url = "http://download.thinkbroadband.com/5MB.zip"
headers = {"Range": "bytes=0-100"}  # first 100 bytes

r = get(url, headers=headers)
```

## Python으로 URL로 file을 Download 받기
https://xeros.dev/56

### 예시
```python
url = 'http://google.com/favicon.ico'
r = requests.get(url, allow_redirects=True)
open('google.ico', 'wb').write(r.content)
```