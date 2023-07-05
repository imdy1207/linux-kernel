# Raspbian Linux Kernel Build
## Reference
### Raspberri Pi Documentation
#### The Linux kernel
https://www.raspberrypi.com/documentation/computers/linux_kernel.html
### 디버깅을 통해 배우는 리눅스 커널의 구조와 원리 1
#### 2.2.3 라즈비안 리눅스 커널 빌드
53 pages
## Description
### dependencies
- 빌드에 필요한 도구, 라이브러리 등을 설치한다.
  ```
  sudo apt install git bc bison flex libssl-dev make
  ```
- 리눅스 소스코드를 내려 받는다.
  ```
  sudo apt install git bc bison flex libssl-dev make
  ```
  -- 특정 버전을 사용할 경우 다음과 같이 특정 버전의 브랜치를 설정하여 내려 받는다.
  ```
  git clone --depth=1 --branch <branch> https://github.com/raspberrypi/linux
  ```
  --- 예) 4.19 버전의 경우
    ```
    git clone --depth=1 --branch rpi-4.19.y https://github.com/raspberrypi/linux
    ```
### Configuration
- 각각의 환경변수들에 라즈베리파이의 버전과 비트수에 따라 알맞은 값으로 설정해 준다.
#### 32bit
- Raspberry Pi 1, Zero and Zero W, and Raspberry Pi Compute Module 1 default (32-bit only)
  ```
  cd linux
  KERNEL=kernel
  make bcmrpi_defconfig
  ```
- Raspberry Pi 2, 3, 3+ and Zero 2 W, and Raspberry Pi Compute Modules 3 and 3+ default 32-bit
  ```
  cd linux
  KERNEL=kernel7
  make bcm2709_defconfig
  ```
- Raspberry Pi 4 and 400, and Raspberry Pi Compute Module 4 default 32-bit
  ```
  cd linux
  KERNEL=kernel7l
  make bcm2711_defconfig
  ```
#### 64bit
- Raspberry Pi 3, 3+, 4, 400 and Zero 2 W, and Raspberry Pi Compute Modules 3, 3+ and 4 default 64-bit
  ```
  cd linux
  KERNEL=kernel8
  make bcm2711_defconfig
  ```
