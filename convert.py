import os
from PIL import Image
import pillow_heif
from pathlib import Path

def convert_image(input_path, output_path=None, quality=80, output_format='WEBP'):
    """
    이미지를 다른 형식으로 변환하고 압축합니다.
    
    Args:
        input_path (str): 입력 이미지 파일 경로
        output_path (str, optional): 출력 파일 경로. 지정하지 않으면 입력 파일과 같은 이름으로 지정된 확장자 사용
        quality (int): 압축 품질 (0-100). 기본값 80
        output_format (str): 출력 형식 ('WEBP', 'JPEG', 'PNG'). 기본값 'WEBP'
    """
    # 출력 경로가 지정되지 않은 경우 입력 파일과 같은 이름으로 지정된 확장자 사용
    if output_path is None:
        output_path = str(Path(input_path).with_suffix(f'.{output_format.lower()}'))
    
    # HEIC/HEIF 파일인 경우 특별 처리
    if input_path.lower().endswith(('.heic', '.heif')):
        heif_file = pillow_heif.read_heif(input_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )
    else:
        # 다른 이미지 형식은 PIL로 직접 열기
        image = Image.open(input_path)
    
    # 이미지가 RGBA 모드인 경우 RGB로 변환 (JPEG는 알파 채널을 지원하지 않음)
    if output_format == 'JPEG' and image.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        image = background
    
    # 지정된 형식으로 저장 (압축 적용)
    image.save(output_path, output_format, quality=quality)
    print(f"변환 완료: {input_path} -> {output_path}")
    
    # 원본과 변환 후 파일 크기 비교
    original_size = os.path.getsize(input_path) / 1024  # KB
    converted_size = os.path.getsize(output_path) / 1024  # KB
    compression_ratio = (1 - converted_size / original_size) * 100
    
    print(f"원본 크기: {original_size:.2f}KB")
    print(f"변환 후 크기: {converted_size:.2f}KB")
    print(f"압축률: {compression_ratio:.1f}%")

def batch_convert_images(input_dir, output_dir=None, quality=80, output_format='WEBP'):
    """
    디렉토리 내의 모든 이미지 파일을 지정된 형식으로 변환합니다.
    
    Args:
        input_dir (str): 입력 디렉토리 경로
        output_dir (str, optional): 출력 디렉토리 경로. 지정하지 않으면 입력 디렉토리와 동일한 위치에 '{format}' 디렉토리 생성
        quality (int): 압축 품질 (0-100). 기본값 80
        output_format (str): 출력 형식 ('WEBP', 'JPEG', 'PNG'). 기본값 'WEBP'
    """
    if output_dir is None:
        output_dir = os.path.join(input_dir, output_format.lower())
    
    # 출력 디렉토리가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 지원하는 이미지 확장자
    supported_extensions = ('.heic', '.heif', '.jpg', '.jpeg', '.png', '.webp')
    
    # 이미지 파일 찾기
    image_files = [f for f in os.listdir(input_dir) 
                  if f.lower().endswith(supported_extensions)]
    
    if not image_files:
        print(f"'{input_dir}' 디렉토리에서 지원하는 이미지 파일을 찾을 수 없습니다.")
        return
    
    print(f"총 {len(image_files)}개의 이미지 파일을 변환합니다...")
    
    # 각 파일 변환
    for image_file in image_files:
        input_path = os.path.join(input_dir, image_file)
        output_path = os.path.join(output_dir, os.path.splitext(image_file)[0] + f'.{output_format.lower()}')
        convert_image(input_path, output_path, quality, output_format)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='이미지를 다른 형식으로 변환하고 압축합니다.')
    parser.add_argument('input', help='입력 이미지 파일 또는 디렉토리 경로')
    parser.add_argument('-o', '--output', help='출력 파일 또는 디렉토리 경로')
    parser.add_argument('-q', '--quality', type=int, default=80, help='압축 품질 (0-100)')
    parser.add_argument('-f', '--format', choices=['WEBP', 'JPEG', 'PNG'], default='WEBP',
                      help='출력 형식 (WEBP, JPEG, PNG)')
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        batch_convert_images(args.input, args.output, args.quality, args.format)
    else:
        convert_image(args.input, args.output, args.quality, args.format) 