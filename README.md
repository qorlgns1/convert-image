# 이미지 변환기

다양한 이미지 형식을 다른 형식으로 변환하고 압축하는 Python 스크립트입니다.

## 시스템 요구사항

- Python 3.8 ~ 3.10 (3.13 이상에서는 호환성 문제가 있을 수 있음)
- macOS 또는 Linux

## 기능

- HEIC/HEIF, JPEG, PNG, WebP 등 다양한 이미지 형식 지원
- WebP, JPEG, PNG 형식으로 변환 가능
- 이미지 압축 및 품질 조절
- 단일 파일 또는 디렉토리 일괄 변환 지원
- 변환 전후 파일 크기 비교 및 압축률 표시
- 얼굴 감지 및 모자이크 처리 기능

## 설치 방법

1. Python 버전 확인 및 설정:

```bash
# pyenv 사용 시
pyenv install 3.10.13
pyenv local 3.10.13

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

2. 필요한 패키지 설치:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 사용 방법

### 이미지 형식 변환

기본 설정(WebP, 품질 80)으로 변환:

```bash
python convert.py input.jpg
```

다른 형식으로 변환:

```bash
python convert.py input.jpg -f PNG
```

품질 지정하여 변환 (0-100):

```bash
python convert.py input.jpg -q 90
```

출력 경로 지정:

```bash
python convert.py input.jpg -o output.png
```

### 얼굴 모자이크 처리

단일 이미지 처리:

```bash
python mosaic.py input.jpg
```

모자이크 크기 지정 (픽셀):

```bash
python mosaic.py input.jpg -s 20
```

출력 경로 지정:

```bash
python mosaic.py input.jpg -o output_mosaic.jpg
```

### 디렉토리 일괄 처리

이미지 형식 변환:

```bash
python convert.py /path/to/directory
```

얼굴 모자이크 처리:

```bash
python mosaic.py /path/to/directory
```

## 매개변수

### 이미지 변환 (convert.py)

- `input`: 입력 이미지 파일 또는 디렉토리 경로 (필수)
- `-o, --output`: 출력 파일 또는 디렉토리 경로 (선택)
- `-q, --quality`: 압축 품질 (0-100, 기본값: 80)
- `-f, --format`: 출력 형식 (WEBP, JPEG, PNG 중 선택, 기본값: WEBP)

### 얼굴 모자이크 (mosaic.py)

- `input`: 입력 이미지 파일 또는 디렉토리 경로 (필수)
- `-o, --output`: 출력 파일 또는 디렉토리 경로 (선택)
- `-s, --size`: 모자이크 블록의 크기 (픽셀, 기본값: 10)

## 지원하는 형식

### 입력 형식

- HEIC/HEIF (.heic, .heif)
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

### 출력 형식

- WebP (.webp)
- JPEG (.jpg)
- PNG (.png)

## 출력 정보

### 이미지 변환

- 변환된 파일 경로
- 원본 파일 크기 (KB)
- 변환 후 파일 크기 (KB)
- 압축률 (%)

### 얼굴 모자이크

- 처리된 파일 경로
- 감지된 얼굴 개수

## 예시

```bash
# 이미지 형식 변환
python convert.py photo.heic
python convert.py photo.jpg -f PNG
python convert.py photo.png -f JPEG -q 90

# 얼굴 모자이크 처리
python mosaic.py photo.jpg
python mosaic.py photo.jpg -s 15
python mosaic.py ./photos
```

## 주의사항

- WebP 형식은 대부분의 최신 웹 브라우저에서 지원됩니다.
- JPEG 형식으로 변환 시 알파 채널(투명도)이 있는 이미지는 흰색 배경으로 변환됩니다.
- 품질 값이 낮을수록 파일 크기는 작아지지만 이미지 품질이 저하될 수 있습니다.
- 기본 품질 값(80)은 파일 크기와 이미지 품질의 균형을 고려하여 설정되었습니다.
- 얼굴 모자이크 처리는 얼굴이 명확하게 보이는 이미지에서 가장 잘 작동합니다.
- 모자이크 크기가 작을수록 더 뚜렷한 모자이크 효과를 얻을 수 있습니다.
- Python 3.13 이상에서는 일부 패키지와의 호환성 문제가 있을 수 있으므로 Python 3.8 ~ 3.10 버전 사용을 권장합니다.
