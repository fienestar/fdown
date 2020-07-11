# About
This is download booster, with Python

**It sends HTML packets multiple times, allowing multi-threading to download at the maximum speed of the support network.**

---

# How to use
```Command
>   url -f filname -c cookie -d filedir -t thread_count
```
---

# **📋 Requirements**

- Python 3.6.8
- requests

---

# Function Description

- DownloadFile
    - 분할하지 않고, Download 받는 경우
    ```python
    def DownloadFile(url, cookie, dest):
    ```

- DownloadFileByRange
    - 분할하여, Download 받는 경우
    ```python
    def DownloadFileByRange(url, cookie, dest, begin, end):
    ```

- MergeFile
    - 다수의 File을 병합 하는 경우
    ```python
    def MergeFile(dest, filelist):
    ```

---

# ***여기에 자료와 링크를 두십시오***

---

# "HTTP range requests" *from Mozilla*
https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests

# "Range" *from Mozilla*
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range

# Downloading Files from URLs in Python
https://www.codementor.io/@aviaryan/downloading-files-from-urls-in-python-77q3bs0un

# Python을 사용하여, 일부 file만 Download 받는 방법 *from StackOverFlow*
https://stackoverflow.com/a/23602538/10445743


### 첫 100 byte 까지 Download 받기의 예시
```python
url = "http://download.thinkbroadband.com/5MB.zip"
headers = {"Range": "bytes=0-100"}  # first 100 bytes

r = get(url, headers=headers)
```

# Python으로 URL로 file을 Download 받기
https://xeros.dev/56

### 예시
```python
url = 'http://google.com/favicon.ico'
r = requests.get(url, allow_redirects=True)
open('google.ico', 'wb').write(r.content)
```

---
