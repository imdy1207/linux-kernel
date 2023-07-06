# GPIO 이해하기
## 실습 목표
- LED 2개를 동시에 켜보기
## Description
- github에서 WiringPi 모듈을 불러온다
    - git clone https://github.com/WiringPi/WiringPi
- 불러온 WiringPi 프로젝트 경로로 이동한다
    - cd WiringPi
- 환경을 빌드한다
    - ./build
- C 코드 작동시 gcc를 활용해 컴파일하여 실행한다
    - gcc -o led led.c -lwiringPi
