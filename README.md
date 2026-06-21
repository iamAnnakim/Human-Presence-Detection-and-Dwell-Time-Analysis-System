# YOLOv8 Visitor Analytics System

YOLOv8과 ByteTrack을 활용한 방문자 분석 및 체류시간 측정 시스템

## 📌 프로젝트 소개

본 프로젝트는 영상 속 사람을 자동으로 검출하고 추적하여 방문자 수와 체류시간을 분석하는 시스템입니다.

Ultralytics YOLOv8을 이용하여 사람(Person)을 검출하고, ByteTrack을 이용하여 객체를 추적합니다.

분석 결과로 다음 정보를 제공합니다.

- 방문자 수 (Total Visitors)
- 평균 체류시간 (Average Stay Time)
- 최장 체류시간 (Longest Stay Time)
- 최단 체류시간 (Shortest Stay Time)

---

## 🎯 주요 기능

### 1. 사람 검출

YOLOv8을 사용하여 영상 속 사람을 검출합니다.

### 2. 객체 추적

ByteTrack을 사용하여 사람마다 고유 ID를 부여합니다.

### 3. 방문자 수 집계

객체 ID를 기반으로 방문자 수를 계산합니다.

### 4. 체류시간 분석

입장 시점과 퇴장 시점을 기록하여 체류시간을 계산합니다.

### 5. 결과 저장

- 분석 영상 저장
- 통계 결과 저장

---

## 🏗 시스템 구조

```text
입력 영상
    ↓
YOLOv8 사람 검출
    ↓
ByteTrack 객체 추적
    ↓
방문자 수 집계
    ↓
체류시간 계산
    ↓
통계 결과 생성
```

---

## 🛠 기술 스택

| 기술 | 역할 |
|--------|--------|
| Python | 전체 시스템 구현 |
| OpenCV | 영상 처리 |
| Ultralytics YOLOv8 | 사람 검출 |
| ByteTrack | 객체 추적 |

---

## 📂 프로젝트 구조

```text
person_dwell_time_project
│
├─ videos/
│   ├─ sample1.mp4
│   └─ sample2.mp4
│
├─ output/
│   └─ result.txt
│
├─ Result/
│   └─ sample1_result.mp4
│
├─ main.py
├─ requirements.txt
└─ README.md
```

---

## ⚙ 설치 방법

### 1. 저장소 복제

```bash
git clone https://github.com/your-id/visitor-analytics.git
cd visitor-analytics
```

### 2. 라이브러리 설치

```bash
pip install -r requirements.txt
```

---

## ▶ 실행 방법

```bash
python main.py
```

실행 후 분석할 영상 파일명을 입력합니다.

예시

```text
Video file:
videos/sample1.mp4
```

---

## 📊 출력 결과

### Result Video

- 사람 Bounding Box 표시
- 객체 ID 표시
- 방문자 수 표시

### Result Text

```text
Total Visitors : 12

SUMMARY
----------------

Average Stay : 15.3 sec
Longest Stay : 42.1 sec
Shortest Stay : 3.5 sec
```

---

## 📈 활용 분야

- CCTV 모니터링
- 매장 방문자 분석
- 강의실 이용 현황 분석
- 공공장소 인원 모니터링

---

## ⚠ 한계점

- 동일 인물이 재등장하면 새로운 ID가 부여될 수 있음
- 가림(Occlusion)에 취약
- 실시간 스트리밍 미지원

---

## 🚀 향후 개선 방향

- Flask 기반 웹 서비스 구축
- 실시간 CCTV 분석
- Re-ID 기반 동일 인물 재식별
- 혼잡도 분석 기능
- 방문자 행동 분석 기능

---

## 📚 Dataset

본 프로젝트는 직접 학습을 수행하지 않았으며,
COCO 데이터셋으로 사전학습된 Ultralytics YOLOv8 모델을 사용하였습니다.

COCO Dataset:
https://cocodataset.org

Ultralytics COCO Documentation:
https://docs.ultralytics.com/datasets/detect/coco/

---

## 👨‍💻 Author

김은결

Deep Learning Practice Project
