

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [MINE POST (CSUOS capstone-project)]
  - [team Minerva]
    - [Contacts]
  - [SKT-AI/KoGPT2]
    - [GitHub]
    - [License]
  - [How to install]
    - [Requirements]
  - [How to use]
    - [Linux]
    - [Windows, MacOS]
  - [Main Big3 service]
    - [AI Writing]
    - [Image Recommendation]
    - [three-Line Summary]
  - [Fine Turning]
    - [fineturning]
    - [Function Info.]
    - [sample File Download]
  - [others]
  

<!-- /code_chunk_output -->

---

# MINE POST (CSUOS capstone-project)
* 인공지능 보조 뉴스 사이트
* django 사용



### ㅁ team Minerva

* 많이 부족한 하지만 꾸준한 개선 중에 있습니다.
* team Manager : So
* team Member : Jeong, Jee, Lee, Park 

#### Contacts

`MINE POST` 관련 이슈는 [이곳](https://github.com/ssorry123/capstone/issues)에 올려주세요.
* e-mail(So) : seokzin95@gmail.com



### ㅁ SKT-AI/KoGPT2

* `SKT Conv.AI`팀이 깃허브에 공개한 KoGPT2 모델 Korean GPT-2 pretrained cased (KoGPT2)을 사용하였습니다.

#### GitHub
* 해당 깃허브 주소는 다음과 같습니다. [KoGPT2](https://github.com/SKT-AI/KoGPT2)
* https://github.com/SKT-AI/KoGPT2

#### License
`KoGPT2`는 `modified MIT` 라이선스 하에 공개되어 있습니다. 모델 및 코드를 사용할 경우 라이선스 내용을 준수해주세요. 라이선스 전문은 `LICENSE` 파일에서 확인하실 수 있습니다.



### ㅁ How to install

```sh

&git init
&git clone https://github.com/ssorry123/capstone.git
&cd capstone
&pip3 install -r requirements.txt
```


##### Requirements

Python 버전 3.6 이상을 필요로 하며, 그 외 필요한 package는 모두 `requirements.txt` 에 정의되어있습니다.


* gluonnlp == 0.9.1
* mxnet == 1.6.0
* sentencepiece >= 0.1.85
* torch == 1.5.0
* transformers == 2.11.0
* django_extensions==2.2.9
* selenium==3.141.0
* Django==3.0.7
* minegpt2





### ㅁ How to use

####  Linux

```sh

&cd MXXXPXXX
&python3 manage.py runserver
```

```sh

anonymous:~/wwwww/capstone$ cd MXXXPXXX
anonymous:~/wwwww/capstone/MXXXPXXX$ python3 manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

server loading...
using cached model
using cached model
using cached model
System check identified no issues (0 silenced).
June 21, 2050 - 00:00:00
Django version 3.0.6, using settings 'MXXXPXXX.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```

Main Homepage 접속 경로는 언제든지 업데이트 될 수 있습니다.
```
localhost:8000/sg
```

#### Windows, MaxOS
`django`로 개발되었고, 꾸준한 업데이트 중에 있으며 해당 OS에도 얼마든지 django를 설치한 후 사용하실 수 있습니다.





### ㅁ Main Big3 service

#### 1. AI Writing
- 실시간 단어 추천
- 자동 기사 완성
- 글 스타일 선택(fine turning 적용)

#### 2. Image Recommendation
- 이미지 크롤링을 사용한 이미지 추천
- (chromedriver를 사용하므로 본인의 chrome 버전에 맞는 chromedriver를 설치해주세요.)

#### 3. three-Line Summary
- TextRank를 통한 핵심 문장 요약
- (패키지 문제로 개선 중에 있습니다.)






### ㅁ FineTurning
#### fineturning
- 직접 원하는 데이터를 수집한 후 fineturning을 진행하실 수 있습니다.
- fineturning은 `Google Colab`을 사용하였으며 수집한 데이터에 따라 완벽하지 않은 코드일 수 있습니다.
- fineturning 과정은 fineturning 폴더를 참조하세요.
- 학습을 마친 후 결과물은 `.tar` 파일로 저장되게 됩니다.(주의, 용량이 큼)

#### Function Info.
- fineturning을 완료 한 후 AI Writing에 `적용`하려면 간단한 함수 변경이 필요합니다.
- `capstone/MXXXPXXX/sg`에 위치한 `sw_gpt_function.py`를 약간 수정해야 합니다.
- `adaptFineTurning 함수`의 `load_path`를 자신이 학습완료한 파일의 경로에 맞게 수정한 후
- `serveral_sentence_generate 함수`에서 `adaptFineTurning 함수`를 주석처리를 해제해주세요.
- fineturning을 적용하게 되면 글 생성 속도에 약간의 영향을 미칠 수 있습니다.

#### sample File Download
- 서버를 배포하지 않았기 때문에 fineturning을 적용하려면 몇 개의 tar파일들을 로컬에 저장하여야 합니다.
- 용량 문제로 샘플 tar 파일 하나만을 제공하고 있습니다. (약 1.5GB) (333.tar) (김동인 작가의 단편소설)
- 다운로드 방법은 아래와 같습니다. (주소는 언제든지 변경될 수 있습니다.)

```sh

&pip3 install gdown

&gdown https://drive.google.com/uc?id=1-2bfIejzxDwT6xpZr64ujJwJsId_FtW9

```





### ㅁ others

#### 협업 방식: Forking
- 링크1: <https://gmlwjd9405.github.io/2017/10/28/how-to-collaborate-on-GitHub-2.html>
- 링크2: <https://andamiro25.tistory.com/193>




