"""
파일명: main.py
useage: main.py url [-f filename] [-d dir path] [-t thread_count] [-c cookie]
동작: url의 파일을 다운로드합니다. 최대 thread_count(없을경우 DEFAULT_THREAD_COUNT)만큼의 스레드를 생성하여 각각 분할 다운로드를 합니다.

dir/filename에 최종적으로 파일이 합쳐집니다.

* filename이 없을 경우 사이트에서 지정하는 파일 이름으로 지정됩니다.
* dir이 없는 경우 현재 실행 위치를 나타냅니다.
* url가 Range Request를 지원하지 않을경우 thread_count = 1이 됩니다.

분할 다운로드 파일명: file name.download${thread_index}

분할 다운로드가 모두 끝날 경우 각 파일을 합쳐 하나의 파일로 합칩니다.

목표: 멀티스레딩과 HTTP Range Request를 활용하여 다운로드 속도를 증가시킵니다.

현재 샘플: python main.py https://files.cloud.naver.com/.fileLink/y6P8tahQ8JFyvWpcB%2BA4vSnOCCKTBIHyuxtJo43x7QBjpF43reXL5%2F%2Fj7R7UxyWKfPSOx3sp%2BMPl9SZxLG%2BjTgY%3D/%EB%93%A3%EA%B8%B0%20%EC%A2%8B%EC%9D%80%20%EB%B0%B0%EA%B2%BD%EC%9D%8C.mp4?authtoken=PtXHZHtMHzkScSHgWBo9MwI%3D -f test.rar -c "NNB=JJLUOBSC44DF6"
"""

DEFAULT_THREAD_COUNT = 8
FILE_BUFFER_SIZE = 256 * 1024

import sys
import os
import requests
import threading

def Debug(str):
    print(str)

def DownloadFile(url, cookie, dest):
    """
    범위없는 file을 경로 dest로 다운로드합니다.
    """
    Debug(f'다운로드 시작: {dest}')
    res = requests.get(url, headers={"Cookie": cookie}, allow_redirects=True)
    open(dest,'wb').write(res.content)

    content_len = res.headers['Content-Length']
    Debug(f'다운로드 완료: {dest}({content_len} bytes)')

def DownloadFileByRange(url, cookie, dest, begin, end):
    """
    경로 dest로 파일을 [begin,end)만큼 다운로드합니다.
    """
    try:
        if end is not '':
            end = end - 1
        Debug(f'다운로드 시작: {dest}')
        res = requests.get(url, headers={"Range": f"bytes={begin}-{end}", "Cookie": cookie}, allow_redirects=True)
        open(dest,'wb').write(res.content)

        content_len = res.headers['Content-Length']
        Debug(f'다운로드 완료: {dest}({content_len} bytes)')
    except:
        Debug(f'URL: {url}')
        Debug(f'Cookie: {cookie}')
        Debug(f'dest: {dest}')
        Debug(f'begin: {begin}')
        Debug(f'end: {end}')

def MergeFile(dest, filelist):
    """
    filelist의 파일들을 dest에 합칩니다.
    """
    global FILE_BUFFER_SIZE
    with open(dest, 'ab') as fd_dest: # append binary
        for filename in filelist:
            Debug(f'[{filename}] 합치는중..')
            with open(filename, 'rb') as src:
                buf = src.read(FILE_BUFFER_SIZE)
                while buf:
                    fd_dest.write(buf)
                    buf = src.read(FILE_BUFFER_SIZE)

def ParseArgv(argv):
    arg_map = {}
    arg_list = []
    reserved_label = None
    is_quoted = False
    
    for arg in argv:
        if reserved_label:
            if not is_quoted and arg.startswith('"') and arg_map[reserved_label] is None:
                is_quoted = True
                arg_map[reserved_label] = arg[1:]
            elif is_quoted:
                if arg.endsWith('"'):
                    arg_map[reserved_label] = arg[:-1]
                    is_quoted = False
                    reserved_label = None
                else:
                    arg_map[reserved_label] = arg_map[reserved_label] + " " + arg
            else:
                arg_map[reserved_label] = arg
                reserved_label = None
        
        elif arg.startswith("-"):
            reserved_label = arg
        else:
            arg_list.append(arg)

    return (arg_map,arg_list)

def ParseEQMap(content,sep):
    eq_map = {}
    for splited in content.split(sep):
        try:
            key, value = splited.split('=')
            eq_map[key.strip()] = value.strip()
        except:
            pass
    return eq_map

def Main(argv):
    thread_count = DEFAULT_THREAD_COUNT
    cookie = ""

    arg_map, arg_list = ParseArgv(argv)

    USEAGE = f'useage: {arg_list[0]} url [-f filename] [-d dir path] [-t thread_count] [-c cookie]'

    if len(arg_list) != 2:
        Debug(USEAGE)
        return
    
    url = arg_list[1]
    filedir = '.'
    filename = None

    for o, v in arg_map.items():
        if o == '-t':
            thread_count = v
        elif o == '-c':
            cookie = v
        elif o == '-f':
            filename = v
        elif o == '-d':
            filedir = v
        else:
            Debug(f'Unknown option: {(o,v)}')
            Debug(USEAGE)
            return

    res = requests.get(url, headers={"Range":"0-", "Cookie": cookie})
    res.encoding = 'UTF-8'   
    headers = res.headers
    Debug(headers)

    if 'Content-Disposition' in headers:
        server_file_name = ParseEQMap(headers['Content-Disposition'],';')['filename']

        if filename is None:
            filename = server_file_name
        else:
            Debug(f'{filename} <- Server: {server_file_name}')
    else:
        if filename is None:
            filename = 'download'
    
    dest = filedir + os.path.sep + filename

    if 'Accept-Ranges' not in headers or headers['Accept-Ranges'] == 'none' or 'Content-Length' not in headers or int(headers['Content-Length']) <= 1024:
        Debug('속도 증가 불가')
        DownloadFile(url, cookie, dest)
    else:
        content_len = int(headers['Content-Length'])
        chunk_size = content_len // thread_count
        if content_len % thread_count:
            chunk_size = chunk_size + 1
    
        threads = [threading.Thread(target=DownloadFileByRange,args=(url,cookie,dest+f'.fdown{i}',i*chunk_size,'' if i+1 == thread_count else (i+1)*chunk_size)) for i in range(thread_count)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        MergeFile(dest+'.fdown0',[dest+f'.fdown{i}' for i in range(1,thread_count)])
        os.rename(dest+'.fdown0',dest)

    Debug('다운로드 완료')

if __name__ == "__main__":
    Main(sys.argv)