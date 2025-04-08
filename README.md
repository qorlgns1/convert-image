# 이미지 변환기

다양한 이미지 형식을 다른 형식으로 변환하고 압축하는 Python 스크립트입니다.

## 기능

- HEIC/HEIF, JPEG, PNG, WebP 등 다양한 이미지 형식 지원
- WebP, JPEG, PNG 형식으로 변환 가능
- 이미지 압축 및 품질 조절
- 단일 파일 또는 디렉토리 일괄 변환 지원
- 변환 전후 파일 크기 비교 및 압축률 표시

## 설치 방법

1. 필요한 패키지 설치:

```bash
pip install -r requirements.txt
```

## 사용 방법

### 단일 파일 변환

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

### 디렉토리 일괄 변환

디렉토리 내의 모든 이미지 파일 변환:

```bash
python convert.py /path/to/directory
```

특정 형식으로 변환:

```bash
python convert.py /path/to/directory -f JPEG
```

출력 디렉토리 지정:

```bash
python convert.py /path/to/directory -o /path/to/output
```

## 매개변수

- `input`: 입력 이미지 파일 또는 디렉토리 경로 (필수)
- `-o, --output`: 출력 파일 또는 디렉토리 경로 (선택)
- `-q, --quality`: 압축 품질 (0-100, 기본값: 80)
- `-f, --format`: 출력 형식 (WEBP, JPEG, PNG 중 선택, 기본값: WEBP)

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

변환 시 다음 정보가 표시됩니다:

- 변환된 파일 경로
- 원본 파일 크기 (KB)
- 변환 후 파일 크기 (KB)
- 압축률 (%)

## 예시

```bash
# HEIC를 WebP로 변환
python convert.py photo.heic

# JPEG를 PNG로 변환
python convert.py photo.jpg -f PNG

# 고품질 JPEG 변환
python convert.py photo.png -f JPEG -q 90

# 디렉토리 일괄 변환
python convert.py ./photos -f JPEG
```

## 주의사항

- WebP 형식은 대부분의 최신 웹 브라우저에서 지원됩니다.
- JPEG 형식으로 변환 시 알파 채널(투명도)이 있는 이미지는 흰색 배경으로 변환됩니다.
- 품질 값이 낮을수록 파일 크기는 작아지지만 이미지 품질이 저하될 수 있습니다.
- 기본 품질 값(80)은 파일 크기와 이미지 품질의 균형을 고려하여 설정되었습니다.
