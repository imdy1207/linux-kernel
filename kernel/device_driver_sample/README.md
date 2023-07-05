# Sample Kernel Module
## 설명
### 목표
- kernel module의 이해
- 간단한 kernel module을 작성
- kernel messege를 확인
### 개요
#### kernel module
- 커널은 많은 기능들이 포함된 `monolothic kernel`과 필요한 기능만을 넣어 경량화 한 `micro kernel`이 존재한다.
- 만약 커널에 기능을 추가하고 싶을 경우에는 `kernel module`을 추가하여 기능을 확장 가능하다.
- 이러한 커널에 포함된 프로그램들은 사용자가 평소에 사용하는 프로그램과 같이 `user mode`에서 실행되는 것이 아니라 `kernel mode`로 동작하게 된다.
- user mode에서 프로그램이 동작 시 kernel에 요청을 하고 해당 결과를 로드하는 과정에서 오버헤드가 발생하여 느리다.
- 따라서 resource에 접근하는 경우 user application을 사용하여 실행하는 것 보다 kernel module을 사용하는 것이 더 효율적이다.
- 대표적인 커널 모듈은 `device driver`가 존재한다.
- 모듈파일은 확장자로 `.ko`를 사용한다.
#### mod
##### lsmod
##### insmod
##### rmmod
#### dmesg
### 실행 순서
#### 1. 컴파일 및 빌드
```
make
```
#### 2. 모듈 실행
```
insmod hello.ko
```
#### 3. 출력 결과 확인
```
dmesg | tail -1
```
#### 4. 모듈 제거
```
rmmod hello.c
```
