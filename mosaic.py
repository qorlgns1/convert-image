import cv2
import numpy as np
import argparse
from pathlib import Path
import os

def detect_faces(image):
    """
    여러 얼굴 감지기를 사용하여 얼굴을 감지합니다.
    
    Args:
        image: OpenCV 이미지
    Returns:
        list: 감지된 얼굴 좌표 리스트
    """
    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 히스토그램 평활화로 대비 향상
    gray = cv2.equalizeHist(gray)
    
    # 여러 얼굴 감지기 로드
    cascades = [
        cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'),
        cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'),
        cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    ]
    
    all_faces = []
    
    # 각 감지기로 얼굴 검출 시도
    for cascade in cascades:
        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,  # 더 작은 스케일 변화
            minNeighbors=2,    # 더 낮은 임계값
            minSize=(20, 20),  # 더 작은 최소 크기
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        all_faces.extend(faces)
    
    # 중복 제거 및 병합
    if len(all_faces) > 0:
        all_faces = np.array(all_faces)
        # IoU(Intersection over Union) 기반으로 중복 제거
        final_faces = []
        while len(all_faces) > 0:
            current = all_faces[0]
            all_faces = all_faces[1:]
            
            # 현재 얼굴과 겹치는 다른 얼굴들 찾기
            i = 0
            while i < len(all_faces):
                x1, y1, w1, h1 = current
                x2, y2, w2, h2 = all_faces[i]
                
                # 겹치는 영역 계산
                x_left = max(x1, x2)
                y_top = max(y1, y2)
                x_right = min(x1 + w1, x2 + w2)
                y_bottom = min(y1 + h1, y2 + h2)
                
                if x_right > x_left and y_bottom > y_top:
                    intersection = (x_right - x_left) * (y_bottom - y_top)
                    union = w1 * h1 + w2 * h2 - intersection
                    iou = intersection / union
                    
                    if iou > 0.5:  # 50% 이상 겹치면 병합
                        # 더 큰 얼굴 영역 선택
                        if w1 * h1 < w2 * h2:
                            current = all_faces[i]
                        all_faces = np.delete(all_faces, i, 0)
                    else:
                        i += 1
                else:
                    i += 1
            
            final_faces.append(current)
        
        return np.array(final_faces)
    
    return np.array([])

def mosaic_face(image_path, output_path=None, mosaic_size=10):
    """
    이미지에서 얼굴을 감지하고 모자이크 처리합니다.
    
    Args:
        image_path (str): 입력 이미지 파일 경로
        output_path (str, optional): 출력 파일 경로
        mosaic_size (int): 모자이크 블록의 크기 (픽셀)
    """
    # 이미지 로드
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"이미지를 로드할 수 없습니다: {image_path}")
    
    # 얼굴 감지
    faces = detect_faces(image)
    
    if len(faces) == 0:
        print("이미지에서 얼굴을 감지할 수 없습니다.")
        return
    
    print(f"{len(faces)}개의 얼굴을 감지했습니다.")
    
    # 각 얼굴에 모자이크 처리
    for (x, y, w, h) in faces:
        # 얼굴 영역을 약간 확장
        x = max(0, x - int(w * 0.1))
        y = max(0, y - int(h * 0.1))
        w = min(image.shape[1] - x, int(w * 1.2))
        h = min(image.shape[0] - y, int(h * 1.2))
        
        # 얼굴 영역 추출
        face_image = image[y:y+h, x:x+w]
        
        # 모자이크 처리
        face_image = cv2.resize(face_image, (mosaic_size, mosaic_size))
        face_image = cv2.resize(face_image, (w, h), interpolation=cv2.INTER_NEAREST)
        
        # 모자이크 처리된 얼굴을 원본 이미지에 적용
        image[y:y+h, x:x+w] = face_image
    
    # 이미지 압축 설정
    if output_path.lower().endswith(('.jpg', '.jpeg')):
        # JPEG 압축
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
        _, encoded_image = cv2.imencode('.jpg', image, encode_param)
        with open(output_path, 'wb') as f:
            f.write(encoded_image.tobytes())
    elif output_path.lower().endswith('.png'):
        # PNG 압축
        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
        _, encoded_image = cv2.imencode('.png', image, encode_param)
        with open(output_path, 'wb') as f:
            f.write(encoded_image.tobytes())
    elif output_path.lower().endswith('.webp'):
        # WebP 압축 (품질 80)
        encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 80]
        _, encoded_image = cv2.imencode('.webp', image, encode_param)
        with open(output_path, 'wb') as f:
            f.write(encoded_image.tobytes())
    else:
        # 다른 형식은 기본 저장
        cv2.imwrite(output_path, image)
    
    print(f"모자이크 처리 완료: {output_path}")

def process_directory(input_dir, output_dir=None, mosaic_size=10):
    """
    디렉토리 내의 모든 이미지에서 얼굴을 감지하고 모자이크 처리합니다.
    
    Args:
        input_dir (str): 입력 디렉토리 경로
        output_dir (str, optional): 출력 디렉토리 경로
        mosaic_size (int): 모자이크 블록의 크기 (픽셀)
    """
    # 입력 디렉토리 내에 'mosaic' 폴더 생성
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'mosaic')
    
    # 출력 디렉토리가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 지원하는 이미지 확장자
    supported_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif')
    
    # 이미지 파일 찾기
    image_files = [f for f in os.listdir(input_dir) 
                  if f.lower().endswith(supported_extensions)]
    
    if not image_files:
        print(f"'{input_dir}' 디렉토리에서 지원하는 이미지 파일을 찾을 수 없습니다.")
        return
    
    print(f"총 {len(image_files)}개의 이미지 파일을 처리합니다...")
    
    # 각 파일 처리
    for image_file in image_files:
        input_path = os.path.join(input_dir, image_file)
        output_path = os.path.join(output_dir, image_file)  # 원본 파일명 유지
        try:
            mosaic_face(input_path, output_path, mosaic_size)
        except Exception as e:
            print(f"'{image_file}' 처리 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='이미지에서 얼굴을 감지하고 모자이크 처리합니다.')
    parser.add_argument('input', help='입력 이미지 파일 또는 디렉토리 경로')
    parser.add_argument('-o', '--output', help='출력 파일 또는 디렉토리 경로')
    parser.add_argument('-s', '--size', type=int, default=10, help='모자이크 블록의 크기 (픽셀)')
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        process_directory(args.input, args.output, args.size)
    else:
        # 단일 파일 처리 시에도 mosaic 폴더에 저장
        input_dir = os.path.dirname(args.input)
        output_dir = os.path.join(input_dir, 'mosaic')
        os.makedirs(output_dir, exist_ok=True)
        
        input_filename = os.path.basename(args.input)
        output_path = os.path.join(output_dir, input_filename)
        mosaic_face(args.input, output_path, args.size) 