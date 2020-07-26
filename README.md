# About
This is download booster, with Python

**It sends HTML packets multiple times, allowing multi-threading to download at the maximum speed of the support network.**

---

# How to use
```Command
>   url [-f filename] [-d filedir] [-t thread_count] [-c cookie]
```
---

# **📋 Requirements**

- Python 3.7.4
- requests

## If you wnat run *test.py* you need to have that 
- Pandas
- Plotly

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

- [Reference](./Reference.md)
