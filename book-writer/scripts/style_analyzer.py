#!/usr/bin/env python3
"""
Book Writer - Phase 5-2: Style Analyzer (문체 편집)
원고의 문체를 분석하고 개선점을 제안합니다.

분석 항목:
- AI 특유 패턴 검출 & 제거
- 문장 길이 분포
- 어휘 다양성 (TTR)
- 반복 표현 검출
- 대화문 분석
- Show vs Tell 비율
- 감각 묘사 밀도
- 부사 과다 사용
- 감정 아크 분석 (Emotional Arc)
- 페이싱 분석 (Pacing)
- 번역투 검출 (한국어)
- Deep POV / 필터 단어 검출
- 챕터 후크 품질 분석
- 한국어 가독성 지수
- 웹소설 클리셰 검출
"""

import json
import re
import sys
import math
from pathlib import Path
from datetime import datetime
from collections import Counter


# AI 클리셰 패턴 (한국어)
AI_CLICHES = [
    # 감정 직접 서술
    "심장이 쿵 내려앉",
    "심장이 요동쳤",
    "심장이 멈추는 것 같",
    "가슴이 먹먹해",
    "가슴이 벅차올",
    "눈물이 볼을 타고",
    "눈물이 그렁그렁",
    "입술을 꽉 깨물",
    "주먹을 불끈 쥐",
    "숨이 멎을 듯",
    "온몸이 굳어",
    "온몸에 소름이",
    "피가 거꾸로 솟",
    # 과도한 묘사
    "시간이 멈춘 것 같",
    "세상이 무너지는 것 같",
    "마치 꿈을 꾸는 것 같",
    "마치 폭풍 같은",
    "파도처럼 밀려오",
    "소용돌이처럼",
    "불꽃처럼 타오르",
    "얼음처럼 차가",
    # 전환 클리셰
    "그 순간",
    "바로 그때",
    "문득 깨달",
    "불현듯",
    "어느새",
    # 묘사 클리셰
    "깊은 한숨을 내쉬",
    "고개를 끄덕",
    "눈을 크게 뜨",
    "입꼬리가 올라",
    "미간을 찌푸리",
]

# 과도한 부사 목록
EXCESSIVE_ADVERBS = [
    "매우", "정말", "너무", "아주", "굉장히", "엄청나게",
    "절대적으로", "완전히", "극도로", "몹시", "대단히",
    "무척", "상당히", "꽤나", "진심으로", "진정으로",
    "확실히", "분명히", "명백히", "틀림없이",
]

# 감각 묘사 키워드
SENSORY_KEYWORDS = {
    "시각": ["보이", "빛", "색", "밝", "어두", "그림자", "반짝", "흐릿", "선명", "눈앞"],
    "청각": ["소리", "들리", "울리", "속삭", "외치", "침묵", "고요", "시끄", "둔탁", "맑은"],
    "촉각": ["만지", "느끼", "차갑", "뜨거", "부드러", "거친", "날카로", "축축", "건조", "따끔"],
    "후각": ["냄새", "향기", "악취", "향", "풍기", "코끝", "상큼", "비릿", "달콤한 냄새"],
    "미각": ["맛", "쓴", "달콤", "시큼", "짠", "매운", "감칠맛", "혀끝"],
}

# Show vs Tell 패턴
TELL_PATTERNS = [
    r'[가-힣]+(?:이|가)\s*(?:슬[펐프]|기[뻤쁜]|화[났나]|두려[웠워]|행복[했해]|불안[했해])',
    r'(?:슬[픔퍼]|기[쁨뻐]|화[남나]|두려[움워]|행복[함해]|불안[함해])을?\s*느[꼈끼]',
    r'[가-힣]+(?:이|가)\s*(?:놀라|당황|감동|실망|후회)(?:했|한|하)',
]

# === 번역투 패턴 (Translation Artifacts) ===
TRANSLATION_ARTIFACTS = [
    {"pattern": r'하는\s*것을\s*발견했', "label": "~하는 것을 발견했다", "suggestion": "~을 보았다 / 직접 서술"},
    {"pattern": r'그것은\s*[가-힣]+[였이]', "label": "그것은 ~였다 (It was ~)", "suggestion": "구체적 주어 사용"},
    {"pattern": r'에\s*대해서', "label": "~에 대해서 남용", "suggestion": "~을/를, ~에 관해"},
    {"pattern": r'그녀의|그의', "label": "그녀의/그의 과다 사용", "suggestion": "소유격 생략 또는 이름 사용"},
    {"pattern": r'할\s*수\s*있었다', "label": "~할 수 있었다 (could)", "suggestion": "~했다, ~해냈다"},
    {"pattern": r'하기\s*시작했', "label": "~하기 시작했다 (started to)", "suggestion": "~했다 (직접 서술)"},
    {"pattern": r'인\s*것\s*같았', "label": "~인 것 같았다 (seemed to)", "suggestion": "단정적 표현 또는 묘사로 전환"},
    {"pattern": r'하지\s*않을\s*수\s*없었', "label": "~하지 않을 수 없었다 (couldn't help but)", "suggestion": "~했다"},
    {"pattern": r'중\s*하나였', "label": "~중 하나였다 (one of the ~)", "suggestion": "구체적 표현"},
    {"pattern": r'그\s*자신[을의]|그녀\s*자신[을의]', "label": "그 자신을/의 (himself/herself)", "suggestion": "재귀 표현 생략"},
    {"pattern": r'하는\s*데\s*성공했', "label": "~하는 데 성공했다", "suggestion": "~했다, ~해냈다"},
]

# === 필터 단어 (Deep POV 위반) ===
FILTER_WORDS = [
    {"pattern": r'을\s*느꼈|를\s*느꼈|고\s*느꼈', "label": "~을 느꼈다", "suggestion": "감각을 직접 묘사"},
    {"pattern": r'을\s*보았|를\s*보았|을\s*봤|를\s*봤', "label": "~을 보았다/봤다", "suggestion": "본 것을 직접 서술"},
    {"pattern": r'을\s*들었|를\s*들었|이\s*들렸|가\s*들렸', "label": "~을 들었다", "suggestion": "소리를 직접 서술"},
    {"pattern": r'라고\s*생각했|고\s*생각했', "label": "~라고 생각했다", "suggestion": "생각을 직접 서술 (Free Indirect Discourse)"},
    {"pattern": r'인\s*것을\s*알았|는\s*것을\s*알았|을\s*알\s*수\s*있었', "label": "~인 것을 알았다", "suggestion": "깨달음을 행동/반응으로"},
    {"pattern": r'인\s*것을\s*깨달았|는\s*것을\s*깨달았|을\s*깨달았', "label": "~인 것을 깨달았다", "suggestion": "깨달음의 결과를 직접 서술"},
    {"pattern": r'라는\s*사실을\s*알았', "label": "~라는 사실을 알았다", "suggestion": "결과를 직접 서술"},
    {"pattern": r'다는\s*것을\s*느', "label": "~다는 것을 느끼다", "suggestion": "감각/신체 반응으로 대체"},
]

# === 웹소설 클리셰 ===
WEBNOVEL_CLICHES = [
    {"pattern": r'상태창이\s*떴', "label": "상태창이 떴다", "category": "시스템"},
    {"pattern": r'레벨업\s*알림', "label": "레벨업 알림이", "category": "시스템"},
    {"pattern": r'스킬을\s*획득', "label": "스킬을 획득", "category": "시스템"},
    {"pattern": r'경험치를\s*획득', "label": "경험치를 획득", "category": "시스템"},
    {"pattern": r'미간을\s*찌푸리며', "label": "미간을 찌푸리며", "category": "묘사"},
    {"pattern": r'입꼬리가\s*올라갔', "label": "입꼬리가 올라갔다", "category": "묘사"},
    {"pattern": r'눈이\s*휘둥그레', "label": "눈이 휘둥그레", "category": "묘사"},
    {"pattern": r'살기가\s*느껴|살기를\s*내뿜', "label": "살기 묘사", "category": "묘사"},
    {"pattern": r'동공이\s*흔들', "label": "동공이 흔들렸다", "category": "묘사"},
    {"pattern": r'식은땀이\s*흘', "label": "식은땀이 흘렀다", "category": "묘사"},
    {"pattern": r'눈빛이\s*날카로|눈빛이\s*차가', "label": "눈빛 클리셰", "category": "묘사"},
    {"pattern": r'검은\s*안개|붉은\s*안개', "label": "색상 안개 클리셰", "category": "묘사"},
    {"pattern": r'이것은\s*사기|사기\s*스킬', "label": "사기 스킬/능력", "category": "시스템"},
    {"pattern": r'한\s*줄기\s*빛', "label": "한 줄기 빛", "category": "묘사"},
    {"pattern": r'공기가\s*무거워', "label": "공기가 무거워졌다", "category": "묘사"},
    {"pattern": r'분위기가\s*달라', "label": "분위기가 달라졌다", "category": "묘사"},
]

# === 감정 키워드 사전 (감정 아크 분석용) ===
EMOTION_KEYWORDS = {
    "positive": [
        "기쁘", "행복", "웃", "미소", "사랑", "희망", "감사", "평화", "편안",
        "즐거", "설레", "뿌듯", "따뜻", "환하", "밝", "좋", "기대", "신나",
        "만족", "축하", "축복", "승리", "성공", "감동", "아름다",
    ],
    "negative": [
        "슬프", "울", "눈물", "고통", "분노", "두려", "공포", "절망", "외로",
        "불안", "걱정", "후회", "죽", "피", "상처", "아프", "괴로", "비참",
        "증오", "원망", "배신", "실패", "좌절", "어두", "차가", "무서",
    ],
}

# === 긴장/갈등 키워드 (페이싱 분석용) ===
TENSION_KEYWORDS = [
    "갈등", "위기", "위험", "긴장", "충돌", "대립", "싸움", "전투", "도망",
    "추격", "비밀", "배신", "음모", "복수", "죽음", "생존", "함정", "위협",
    "폭발", "붕괴", "최후", "결전", "대결", "각오", "결심", "맹세",
]

# === 플랫폼별 적정 챕터 길이 (글자 수) ===
PLATFORM_CHAPTER_LENGTH = {
    "카카오페이지": (3000, 5000),
    "문피아": (4000, 6000),
    "노벨피아": (3000, 5000),
    "리디": (4000, 7000),
}


class StyleAnalyzer:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.config = self._load_config()
        self.chapters = self._load_chapters()
        self.findings = []

    def _load_config(self) -> dict:
        config_path = self.project_dir / "project.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_chapters(self) -> list:
        chapters_dir = self.project_dir / "chapters"
        chapters = []
        for ch_file in sorted(chapters_dir.glob("ch*.md")):
            content = ch_file.read_text(encoding="utf-8")
            body = content
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
            chapters.append({
                "file": ch_file.name,
                "num": int(re.search(r'\d+', ch_file.stem).group()),
                "content": body,
            })
        return chapters

    def run_all_analyses(self) -> dict:
        """모든 문체 분석을 실행합니다."""
        results = {}

        results["ai_cliches"] = self.detect_ai_cliches()
        results["adverb_usage"] = self.analyze_adverb_usage()
        results["sentence_variety"] = self.analyze_sentence_variety()
        results["vocabulary_diversity"] = self.analyze_vocabulary_diversity()
        results["repetition"] = self.detect_repetition()
        results["dialogue_analysis"] = self.analyze_dialogue()
        results["show_vs_tell"] = self.analyze_show_vs_tell()
        results["sensory_detail"] = self.analyze_sensory_detail()
        results["paragraph_analysis"] = self.analyze_paragraphs()

        # 새로운 분석
        results["emotional_arc"] = self.analyze_emotional_arc()
        results["pacing"] = self.analyze_pacing()
        results["translation_artifacts"] = self.detect_translation_artifacts()
        results["deep_pov"] = self.analyze_deep_pov()
        results["hook_quality"] = self.analyze_hook_quality()
        results["readability_korean"] = self.calculate_readability_korean()
        results["webnovel_cliches"] = self.detect_webnovel_cliches()

        # 종합 점수
        score = self._calculate_score(results)
        results["overall_score"] = score

        report = {
            "title": self.config["title"],
            "analyzed_at": datetime.now().isoformat(),
            "chapters_analyzed": len(self.chapters),
            "score": score,
            "analyses": results,
            "recommendations": self._generate_recommendations(results),
        }

        self._save_report(report)
        return report

    # ===================================================================
    # 기존 분석 함수들
    # ===================================================================

    def detect_ai_cliches(self) -> dict:
        """AI 특유의 클리셰 표현을 검출합니다."""
        found = []
        for ch in self.chapters:
            for cliche in AI_CLICHES:
                count = ch["content"].count(cliche)
                if count > 0:
                    found.append({
                        "chapter": ch["num"],
                        "cliche": cliche,
                        "count": count,
                    })

        total = sum(f["count"] for f in found)
        return {
            "total_found": total,
            "unique_patterns": len(set(f["cliche"] for f in found)),
            "details": found[:30],  # 상위 30개만
            "severity": "high" if total > 20 else "medium" if total > 10 else "low",
        }

    def analyze_adverb_usage(self) -> dict:
        """부사 사용 빈도를 분석합니다."""
        all_text = " ".join(ch["content"] for ch in self.chapters)
        total_words = len(re.findall(r'[가-힣]+', all_text))

        adverb_counts = {}
        for adverb in EXCESSIVE_ADVERBS:
            count = all_text.count(adverb)
            if count > 0:
                adverb_counts[adverb] = count

        total_adverbs = sum(adverb_counts.values())
        ratio = total_adverbs / total_words * 100 if total_words > 0 else 0

        return {
            "total_excessive_adverbs": total_adverbs,
            "total_words": total_words,
            "ratio_pct": round(ratio, 2),
            "top_offenders": dict(sorted(adverb_counts.items(), key=lambda x: -x[1])[:10]),
            "severity": "high" if ratio > 2 else "medium" if ratio > 1 else "low",
        }

    def analyze_sentence_variety(self) -> dict:
        """문장 길이 분포를 분석합니다."""
        all_text = " ".join(ch["content"] for ch in self.chapters)
        sentences = re.split(r'[.!?。]+', all_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        lengths = [len(s) for s in sentences]
        if not lengths:
            return {"total_sentences": 0, "severity": "low"}

        avg_len = sum(lengths) / len(lengths)
        std_dev = math.sqrt(sum((l - avg_len) ** 2 for l in lengths) / len(lengths)) if len(lengths) > 1 else 0

        short = sum(1 for l in lengths if l < 20)
        medium = sum(1 for l in lengths if 20 <= l < 50)
        long = sum(1 for l in lengths if l >= 50)

        total = len(lengths)
        variety_score = std_dev / avg_len if avg_len > 0 else 0

        return {
            "total_sentences": total,
            "average_length": round(avg_len, 1),
            "std_deviation": round(std_dev, 1),
            "distribution": {
                "short_pct": round(short / total * 100, 1),
                "medium_pct": round(medium / total * 100, 1),
                "long_pct": round(long / total * 100, 1),
            },
            "variety_score": round(variety_score, 2),
            "severity": "high" if variety_score < 0.3 else "low",
        }

    def analyze_vocabulary_diversity(self) -> dict:
        """어휘 다양성 (TTR: Type-Token Ratio)을 측정합니다."""
        all_text = " ".join(ch["content"] for ch in self.chapters)
        words = re.findall(r'[가-힣]+', all_text)

        if not words:
            return {"ttr": 0, "severity": "low"}

        total_tokens = len(words)
        unique_types = len(set(words))
        ttr = unique_types / total_tokens if total_tokens > 0 else 0

        chapter_ttrs = []
        for ch in self.chapters:
            ch_words = re.findall(r'[가-힣]+', ch["content"])
            if ch_words:
                ch_ttr = len(set(ch_words)) / len(ch_words)
                chapter_ttrs.append({
                    "chapter": ch["num"],
                    "ttr": round(ch_ttr, 3),
                })

        return {
            "overall_ttr": round(ttr, 3),
            "total_tokens": total_tokens,
            "unique_types": unique_types,
            "chapter_ttrs": chapter_ttrs,
            "severity": "high" if ttr < 0.3 else "medium" if ttr < 0.4 else "low",
        }

    def detect_repetition(self) -> dict:
        """근거리 반복을 검출합니다."""
        repetitions = []

        for ch in self.chapters:
            paragraphs = ch["content"].split("\n\n")
            for para_idx, para in enumerate(paragraphs):
                words = re.findall(r'[가-힣]{2,}', para)
                word_counts = Counter(words)

                for word, count in word_counts.items():
                    if count >= 3 and len(word) >= 3:
                        repetitions.append({
                            "chapter": ch["num"],
                            "word": word,
                            "count": count,
                            "context": "paragraph",
                        })

        return {
            "total_repetitions": len(repetitions),
            "details": sorted(repetitions, key=lambda x: -x["count"])[:20],
            "severity": "high" if len(repetitions) > 30 else "medium" if len(repetitions) > 15 else "low",
        }

    def analyze_dialogue(self) -> dict:
        """대화문을 분석합니다."""
        all_text = " ".join(ch["content"] for ch in self.chapters)

        dialogues = re.findall(r'"([^"]+)"', all_text)
        dialogues += re.findall(r'\u201c([^\u201d]+)\u201d', all_text)

        total_text_len = len(all_text)
        dialogue_len = sum(len(d) for d in dialogues)
        dialogue_ratio = dialogue_len / total_text_len * 100 if total_text_len > 0 else 0

        fancy_tags = re.findall(r'(?:소리쳤|외쳤|속삭였|울부짖었|으르렁거렸|비명을 질렀)', all_text)
        simple_tags = re.findall(r'(?:말했|물었|대답했|답했)', all_text)

        tag_ratio = len(fancy_tags) / (len(fancy_tags) + len(simple_tags)) * 100 if (len(fancy_tags) + len(simple_tags)) > 0 else 0

        return {
            "total_dialogues": len(dialogues),
            "dialogue_ratio_pct": round(dialogue_ratio, 1),
            "avg_dialogue_length": round(sum(len(d) for d in dialogues) / len(dialogues), 1) if dialogues else 0,
            "tag_analysis": {
                "simple_tags": len(simple_tags),
                "fancy_tags": len(fancy_tags),
                "fancy_ratio_pct": round(tag_ratio, 1),
            },
            "severity": "high" if tag_ratio > 50 else "medium" if tag_ratio > 30 else "low",
        }

    def analyze_show_vs_tell(self) -> dict:
        """Show vs Tell 비율을 분석합니다."""
        all_text = " ".join(ch["content"] for ch in self.chapters)

        tell_count = 0
        tell_examples = []
        for pattern in TELL_PATTERNS:
            matches = re.findall(pattern, all_text)
            tell_count += len(matches)
            tell_examples.extend(matches[:3])

        total_sentences = len(re.split(r'[.!?。]+', all_text))
        tell_ratio = tell_count / total_sentences * 100 if total_sentences > 0 else 0

        return {
            "tell_instances": tell_count,
            "total_sentences": total_sentences,
            "tell_ratio_pct": round(tell_ratio, 1),
            "examples": tell_examples[:10],
            "severity": "high" if tell_ratio > 15 else "medium" if tell_ratio > 8 else "low",
        }

    def analyze_sensory_detail(self) -> dict:
        """감각 묘사 밀도를 분석합니다."""
        results = {}
        all_text = " ".join(ch["content"] for ch in self.chapters)

        for sense, keywords in SENSORY_KEYWORDS.items():
            count = sum(all_text.count(kw) for kw in keywords)
            results[sense] = count

        total = sum(results.values())
        total_words = len(re.findall(r'[가-힣]+', all_text))
        density = total / total_words * 100 if total_words > 0 else 0

        return {
            "by_sense": results,
            "total_sensory": total,
            "density_pct": round(density, 2),
            "dominant_sense": max(results, key=results.get) if results else "없음",
            "weakest_sense": min(results, key=results.get) if results else "없음",
            "severity": "high" if density < 0.5 else "medium" if density < 1 else "low",
        }

    def analyze_paragraphs(self) -> dict:
        """문단 길이 분포를 분석합니다."""
        all_text = " ".join(ch["content"] for ch in self.chapters)
        paragraphs = [p.strip() for p in all_text.split("\n\n") if p.strip()]

        if not paragraphs:
            return {"total_paragraphs": 0, "severity": "low"}

        lengths = [len(p) for p in paragraphs]
        avg = sum(lengths) / len(lengths)

        short = sum(1 for l in lengths if l < 50)
        medium = sum(1 for l in lengths if 50 <= l < 200)
        long = sum(1 for l in lengths if l >= 200)

        total = len(lengths)
        return {
            "total_paragraphs": total,
            "average_length": round(avg, 1),
            "distribution": {
                "short_pct": round(short / total * 100, 1),
                "medium_pct": round(medium / total * 100, 1),
                "long_pct": round(long / total * 100, 1),
            },
            "severity": "medium" if avg > 300 else "low",
        }

    # ===================================================================
    # 새로운 분석 함수들
    # ===================================================================

    def analyze_emotional_arc(self) -> dict:
        """감정 곡선을 분석합니다 (긍정/부정 키워드 기반).

        Vonnegut의 스토리 형태 이론 기반으로 각 챕터의 감정 극성을 추적하고
        전체 감정 곡선의 형태를 판별합니다.
        """
        chapter_emotions = []

        for ch in self.chapters:
            text = ch["content"]
            pos_count = sum(text.count(kw) for kw in EMOTION_KEYWORDS["positive"])
            neg_count = sum(text.count(kw) for kw in EMOTION_KEYWORDS["negative"])
            total = pos_count + neg_count

            if total > 0:
                polarity = (pos_count - neg_count) / total  # -1.0 ~ 1.0
            else:
                polarity = 0.0

            chapter_emotions.append({
                "chapter": ch["num"],
                "positive": pos_count,
                "negative": neg_count,
                "polarity": round(polarity, 3),
            })

        # 감정 곡선 형태 판별
        story_shape = self._classify_story_shape(chapter_emotions)

        # 감정 변화의 자연스러움 (인접 챕터 간 극성 차이)
        abrupt_changes = []
        for i in range(1, len(chapter_emotions)):
            diff = abs(chapter_emotions[i]["polarity"] - chapter_emotions[i - 1]["polarity"])
            if diff > 0.6:  # 급격한 감정 전환 임계값
                abrupt_changes.append({
                    "from_chapter": chapter_emotions[i - 1]["chapter"],
                    "to_chapter": chapter_emotions[i]["chapter"],
                    "polarity_diff": round(diff, 3),
                })

        # 절정 위치 분석
        if chapter_emotions:
            polarities = [ce["polarity"] for ce in chapter_emotions]
            # 가장 극단적인 감정의 위치
            abs_polarities = [abs(p) for p in polarities]
            max_idx = abs_polarities.index(max(abs_polarities))
            total_ch = len(chapter_emotions)
            peak_position_pct = round((max_idx + 1) / total_ch * 100, 1) if total_ch > 0 else 0
        else:
            peak_position_pct = 0

        return {
            "chapter_emotions": chapter_emotions,
            "story_shape": story_shape,
            "abrupt_changes": abrupt_changes,
            "peak_position_pct": peak_position_pct,
            "severity": "high" if len(abrupt_changes) > 3 else "medium" if len(abrupt_changes) > 1 else "low",
        }

    def _classify_story_shape(self, chapter_emotions: list) -> str:
        """Vonnegut의 스토리 형태를 판별합니다."""
        if len(chapter_emotions) < 3:
            return "판별 불가 (챕터 부족)"

        polarities = [ce["polarity"] for ce in chapter_emotions]
        n = len(polarities)

        # 시작/중간/끝 구간의 평균 극성
        q1 = max(1, n // 4)
        q3 = max(1, 3 * n // 4)
        start = sum(polarities[:q1]) / q1
        mid_slice = polarities[n // 3:2 * n // 3]
        mid = sum(mid_slice) / max(1, len(mid_slice))
        end_slice = polarities[q3:]
        end = sum(end_slice) / max(1, len(end_slice))

        # 단순 분류 로직
        if start < -0.1 and end > 0.1:
            if mid < start:
                return "Cinderella (상승-하강-상승)"
            return "Rags to Riches (상승)"
        elif start > 0.1 and end < -0.1:
            if mid > start:
                return "Oedipus (하강-상승-하강)"
            return "Riches to Rags (하강)"
        elif start > 0.1 and mid < -0.1 and end > 0.1:
            return "Man in a Hole (하강 후 상승)"
        elif start < -0.1 and mid > 0.1 and end < -0.1:
            return "Icarus (상승 후 하강)"
        else:
            # 전반적 추세 확인
            increasing = sum(1 for i in range(n - 1) if polarities[i + 1] > polarities[i])
            if increasing > n * 0.7:
                return "Steady Ascent (꾸준한 상승)"
            elif increasing < n * 0.3:
                return "Steady Descent (꾸준한 하강)"
            else:
                return "Complex (복합 형태)"

    def analyze_pacing(self) -> dict:
        """페이싱을 분석합니다 (액션/대화/묘사 비율, 긴장도 곡선).

        각 챕터의 씬 구성 요소 비율과 긴장도를 측정하여
        처진 구간(saggy middle)과 페이싱 문제를 검출합니다.
        """
        chapter_pacing = []

        action_keywords = [
            "달리", "뛰", "때리", "막", "피하", "던지", "잡", "밀",
            "쓰러", "일어나", "칼", "검", "마법", "공격", "방어",
            "폭발", "충돌", "추격", "도망", "싸우",
        ]

        for ch in self.chapters:
            text = ch["content"]
            total_len = len(text)
            if total_len == 0:
                continue

            # 대화문 비율
            dialogue_matches = re.findall(r'["\u201c][^\u201d"]+["\u201d]', text)
            dialogue_len = sum(len(d) for d in dialogue_matches)
            dialogue_ratio = dialogue_len / total_len * 100

            # 액션 키워드 기반 추정
            action_count = sum(text.count(kw) for kw in action_keywords)
            action_density = action_count / (total_len / 1000)  # per 1000 chars

            # 묘사 비율 (나머지)
            desc_ratio = 100 - dialogue_ratio - min(action_density * 5, 40)
            desc_ratio = max(0, desc_ratio)

            # 긴장도 측정
            tension_count = sum(text.count(kw) for kw in TENSION_KEYWORDS)
            tension_score = min(10, tension_count / max(1, total_len / 5000) * 10)

            chapter_pacing.append({
                "chapter": ch["num"],
                "length": total_len,
                "dialogue_pct": round(dialogue_ratio, 1),
                "action_density": round(action_density, 2),
                "description_pct": round(desc_ratio, 1),
                "tension_score": round(tension_score, 1),
            })

        # 씬 길이 분포 분석
        lengths = [cp["length"] for cp in chapter_pacing]
        length_std = 0
        if lengths:
            avg_len = sum(lengths) / len(lengths)
            length_std = math.sqrt(sum((l - avg_len) ** 2 for l in lengths) / len(lengths)) if len(lengths) > 1 else 0

        # 처진 구간 검출 (3연속 낮은 긴장도)
        saggy_sections = []
        if len(chapter_pacing) >= 3:
            for i in range(len(chapter_pacing) - 2):
                segment = chapter_pacing[i:i + 3]
                if all(s["tension_score"] < 3.0 for s in segment):
                    saggy_sections.append({
                        "start_chapter": segment[0]["chapter"],
                        "end_chapter": segment[2]["chapter"],
                        "avg_tension": round(sum(s["tension_score"] for s in segment) / 3, 1),
                    })

        # 전체 페이싱 균형
        if chapter_pacing:
            avg_dialogue = sum(cp["dialogue_pct"] for cp in chapter_pacing) / len(chapter_pacing)
            avg_action = sum(cp["action_density"] for cp in chapter_pacing) / len(chapter_pacing)
            avg_tension = sum(cp["tension_score"] for cp in chapter_pacing) / len(chapter_pacing)
        else:
            avg_dialogue = avg_action = avg_tension = 0

        return {
            "chapter_pacing": chapter_pacing,
            "scene_length_std": round(length_std, 1),
            "overall_dialogue_pct": round(avg_dialogue, 1),
            "overall_action_density": round(avg_action, 2),
            "overall_tension_avg": round(avg_tension, 1),
            "saggy_sections": saggy_sections,
            "severity": "high" if len(saggy_sections) > 2 else "medium" if len(saggy_sections) > 0 else "low",
        }

    def detect_translation_artifacts(self) -> dict:
        """번역투 패턴을 검출합니다 (한국어).

        영어 직역체 표현을 찾아내고 자연스러운 한국어 대안을 제안합니다.
        """
        found = []
        pattern_counts = Counter()

        for ch in self.chapters:
            text = ch["content"]
            for artifact in TRANSLATION_ARTIFACTS:
                matches = re.findall(artifact["pattern"], text)
                if matches:
                    count = len(matches)
                    pattern_counts[artifact["label"]] += count
                    found.append({
                        "chapter": ch["num"],
                        "pattern": artifact["label"],
                        "count": count,
                        "suggestion": artifact["suggestion"],
                    })

        total = sum(f["count"] for f in found)

        # 한국어 자연스러움 점수 (번역투가 적을수록 높음)
        all_text = " ".join(ch["content"] for ch in self.chapters)
        total_sentences = len(re.split(r'[.!?。]+', all_text))
        naturalness_score = max(0, 100 - (total / max(1, total_sentences) * 500))

        return {
            "total_found": total,
            "pattern_summary": dict(pattern_counts.most_common(10)),
            "details": sorted(found, key=lambda x: -x["count"])[:30],
            "naturalness_score": round(naturalness_score, 1),
            "severity": "high" if total > 30 else "medium" if total > 15 else "low",
        }

    def analyze_deep_pov(self) -> dict:
        """Deep POV / 필터 단어를 검출합니다.

        심리적 거리를 높이는 필터 단어를 찾아내고,
        Free Indirect Discourse로 전환할 수 있는 구간을 제안합니다.
        """
        found = []
        filter_counts = Counter()

        for ch in self.chapters:
            text = ch["content"]
            for fw in FILTER_WORDS:
                matches = re.findall(fw["pattern"], text)
                if matches:
                    count = len(matches)
                    filter_counts[fw["label"]] += count
                    found.append({
                        "chapter": ch["num"],
                        "filter_word": fw["label"],
                        "count": count,
                        "suggestion": fw["suggestion"],
                    })

        total = sum(f["count"] for f in found)

        # 심리적 거리 추정 (필터 단어가 적을수록 가까움)
        all_text = " ".join(ch["content"] for ch in self.chapters)
        total_sentences = len(re.split(r'[.!?。]+', all_text))
        filter_ratio = total / max(1, total_sentences) * 100

        if filter_ratio < 2:
            psychic_distance = "레벨 4-5 (매우 가까움 - Deep POV)"
        elif filter_ratio < 5:
            psychic_distance = "레벨 3-4 (보통)"
        else:
            psychic_distance = "레벨 2-3 (먼 거리 - 필터 단어 과다)"

        return {
            "total_filter_words": total,
            "filter_ratio_pct": round(filter_ratio, 2),
            "filter_summary": dict(filter_counts.most_common(10)),
            "psychic_distance": psychic_distance,
            "details": sorted(found, key=lambda x: -x["count"])[:30],
            "severity": "high" if filter_ratio > 5 else "medium" if filter_ratio > 2 else "low",
        }

    def analyze_hook_quality(self) -> dict:
        """챕터 시작/끝의 후크 품질을 분석합니다.

        각 챕터의 첫 3줄과 마지막 3줄을 분석하여
        독자의 관심을 끌고 유지하는 요소를 측정합니다.
        """
        hook_results = []

        # 후크 요소 키워드
        hook_keywords = {
            "질문": ["?", "무엇", "왜", "어떻게", "누가", "어디"],
            "긴장": TENSION_KEYWORDS[:10],
            "감정": EMOTION_KEYWORDS["negative"][:10] + EMOTION_KEYWORDS["positive"][:5],
            "대화": ['"', '\u201c'],
            "감각": ["소리", "냄새", "빛", "차가", "뜨거"],
        }

        for ch in self.chapters:
            lines = [l.strip() for l in ch["content"].split("\n") if l.strip()]
            if not lines:
                continue

            # 첫 3줄 분석 (opening hook)
            opening = " ".join(lines[:3])
            opening_score = 0
            opening_elements = []
            for element, keywords in hook_keywords.items():
                if any(kw in opening for kw in keywords):
                    opening_score += 2
                    opening_elements.append(element)

            # 첫 문장이 짧고 강렬한가 (20자 이하)
            if lines and len(lines[0]) <= 20:
                opening_score += 1
                opening_elements.append("짧은 첫 문장")

            # 마지막 3줄 분석 (closing hook / cliffhanger)
            closing = " ".join(lines[-3:])
            closing_score = 0
            closing_elements = []
            for element, keywords in hook_keywords.items():
                if any(kw in closing for kw in keywords):
                    closing_score += 2
                    closing_elements.append(element)

            # 마지막 문장이 질문이거나 미완결인가
            if lines[-1].endswith("?"):
                closing_score += 2
                closing_elements.append("질문형 종결")
            elif lines[-1].endswith("...") or lines[-1].endswith("\u2026"):
                closing_score += 1
                closing_elements.append("여운 종결")

            hook_results.append({
                "chapter": ch["num"],
                "opening_score": min(10, opening_score),
                "opening_elements": opening_elements,
                "closing_score": min(10, closing_score),
                "closing_elements": closing_elements,
                "first_line": lines[0][:50] + ("..." if len(lines[0]) > 50 else ""),
                "last_line": lines[-1][:50] + ("..." if len(lines[-1]) > 50 else ""),
            })

        # 전체 평균
        if hook_results:
            avg_opening = sum(h["opening_score"] for h in hook_results) / len(hook_results)
            avg_closing = sum(h["closing_score"] for h in hook_results) / len(hook_results)
            weak_openings = [h for h in hook_results if h["opening_score"] < 3]
            weak_closings = [h for h in hook_results if h["closing_score"] < 3]
        else:
            avg_opening = avg_closing = 0
            weak_openings = weak_closings = []

        # 첫 3화 몰입도 (웹소설 특화)
        first_three_score = 0
        if len(hook_results) >= 3:
            first_three_score = sum(
                h["opening_score"] + h["closing_score"]
                for h in hook_results[:3]
            ) / 6  # 평균 (3챕터 x 2(open+close))

        return {
            "chapter_hooks": hook_results[:20],  # 상위 20개만
            "avg_opening_score": round(avg_opening, 1),
            "avg_closing_score": round(avg_closing, 1),
            "weak_openings": [h["chapter"] for h in weak_openings],
            "weak_closings": [h["chapter"] for h in weak_closings],
            "first_three_immersion": round(first_three_score, 1),
            "severity": "high" if avg_closing < 3 else "medium" if avg_closing < 5 else "low",
        }

    def calculate_readability_korean(self) -> dict:
        """한국어 가독성 지수를 계산합니다.

        한국어에 맞는 가독성 지표들을 종합하여 점수를 산출합니다:
        - 평균 문장 길이 (짧을수록 가독성 높음)
        - 평균 문단 길이
        - 문장 종결 다양성
        - 의성어/의태어 활용도
        """
        all_text = " ".join(ch["content"] for ch in self.chapters)

        # 문장 분리
        sentences = re.split(r'[.!?。]+', all_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return {"readability_score": 0, "severity": "low"}

        # 1) 평균 문장 길이
        avg_sentence_len = sum(len(s) for s in sentences) / len(sentences)
        sentence_score = max(0, 100 - (avg_sentence_len - 25) * 2)  # 25자 기준

        # 2) 문장 종결 다양성
        endings = []
        for s in sentences:
            s = s.strip()
            if s:
                end = s[-3:] if len(s) >= 3 else s
                endings.append(end)
        unique_endings = len(set(endings))
        ending_diversity = unique_endings / max(1, len(endings)) * 100
        ending_score = min(100, ending_diversity * 5)

        # 3) 의성어/의태어 활용도
        common_mimetic = [
            "살살", "쿵쿵", "두근두근", "반짝반짝", "살랑살랑", "후두둑",
            "우르르", "와르르", "주르르", "뚝뚝", "찰칵", "쨍그랑",
            "살금살금", "슬금슬금", "엉금엉금", "데굴데굴", "빙글빙글",
            "꾸벅꾸벅", "끄덕끄덕", "허둥지둥", "아슬아슬", "조마조마",
            "울컥", "쿵", "탁", "쾅", "번쩍", "스르르", "후루룩", "삐걱",
            "사르르", "또각또각", "뒤뚱뒤뚱", "절레절레", "고개를 갸웃",
        ]
        mimetic_count = sum(all_text.count(m) for m in common_mimetic)
        total_words = len(re.findall(r'[가-힣]+', all_text))
        mimetic_ratio = mimetic_count / max(1, total_words) * 1000  # per 1000 words
        mimetic_score = min(100, mimetic_ratio * 20)

        # 4) 문단 길이 적절성
        paragraphs = [p.strip() for p in all_text.split("\n\n") if p.strip()]
        if paragraphs:
            avg_para_len = sum(len(p) for p in paragraphs) / len(paragraphs)
            para_score = max(0, 100 - abs(avg_para_len - 150) * 0.5)  # 150자 기준
        else:
            para_score = 50

        # 종합 가독성 점수
        readability_score = (
            sentence_score * 0.35 +
            ending_score * 0.20 +
            mimetic_score * 0.15 +
            para_score * 0.30
        )

        return {
            "readability_score": round(readability_score, 1),
            "avg_sentence_length": round(avg_sentence_len, 1),
            "sentence_length_score": round(sentence_score, 1),
            "ending_diversity_score": round(ending_score, 1),
            "mimetic_word_count": mimetic_count,
            "mimetic_score": round(mimetic_score, 1),
            "paragraph_score": round(para_score, 1),
            "severity": "high" if readability_score < 40 else "medium" if readability_score < 60 else "low",
        }

    def detect_webnovel_cliches(self) -> dict:
        """웹소설 클리셰를 검출합니다."""
        found = []
        category_counts = Counter()

        for ch in self.chapters:
            text = ch["content"]
            for cliche in WEBNOVEL_CLICHES:
                matches = re.findall(cliche["pattern"], text)
                if matches:
                    count = len(matches)
                    category_counts[cliche["category"]] += count
                    found.append({
                        "chapter": ch["num"],
                        "cliche": cliche["label"],
                        "category": cliche["category"],
                        "count": count,
                    })

        total = sum(f["count"] for f in found)

        return {
            "total_found": total,
            "by_category": dict(category_counts),
            "details": sorted(found, key=lambda x: -x["count"])[:20],
            "severity": "high" if total > 20 else "medium" if total > 10 else "low",
        }

    # ===================================================================
    # 점수 산출 및 리포트 생성
    # ===================================================================

    def _calculate_score(self, results: dict) -> int:
        """종합 문체 점수를 계산합니다 (0-100)."""
        score = 100
        severity_penalty = {"high": 15, "medium": 8, "low": 0}

        for key, analysis in results.items():
            if isinstance(analysis, dict) and "severity" in analysis:
                score -= severity_penalty.get(analysis["severity"], 0)

        return max(0, min(100, score))

    def _generate_recommendations(self, results: dict) -> list:
        """분석 결과를 바탕으로 개선 권고를 생성합니다."""
        recs = []

        if results["ai_cliches"]["severity"] != "low":
            recs.append({
                "priority": "high",
                "category": "AI 패턴",
                "message": f"AI 클리셰 {results['ai_cliches']['total_found']}건 검출. 독창적인 표현으로 교체하세요.",
            })

        if results["adverb_usage"]["severity"] != "low":
            recs.append({
                "priority": "medium",
                "category": "부사",
                "message": f"과도한 부사 {results['adverb_usage']['total_excessive_adverbs']}건. 강한 동사/명사로 대체하세요.",
            })

        if results["sentence_variety"]["severity"] != "low":
            recs.append({
                "priority": "medium",
                "category": "문장 다양성",
                "message": "문장 길이가 단조롭습니다. 단문과 장문을 섞어 리듬감을 주세요.",
            })

        if results["vocabulary_diversity"]["severity"] != "low":
            recs.append({
                "priority": "medium",
                "category": "어휘 다양성",
                "message": f"TTR {results['vocabulary_diversity']['overall_ttr']:.3f}. 유의어를 활용하여 어휘를 풍부하게 하세요.",
            })

        if results["show_vs_tell"]["severity"] != "low":
            recs.append({
                "priority": "high",
                "category": "Show vs Tell",
                "message": f"직접 감정 서술 {results['show_vs_tell']['tell_ratio_pct']:.1f}%. 행동/감각 묘사로 전환하세요.",
            })

        if results["sensory_detail"]["severity"] != "low":
            weakest = results["sensory_detail"]["weakest_sense"]
            recs.append({
                "priority": "medium",
                "category": "감각 묘사",
                "message": f"감각 묘사가 부족합니다. 특히 '{weakest}' 묘사를 보강하세요.",
            })

        if results["dialogue_analysis"]["severity"] != "low":
            recs.append({
                "priority": "medium",
                "category": "대화 태그",
                "message": "화려한 대화 태그가 많습니다. '말했다'를 기본으로 사용하세요.",
            })

        # 새로운 분석에 대한 권고
        if results["emotional_arc"]["severity"] != "low":
            changes = len(results["emotional_arc"]["abrupt_changes"])
            recs.append({
                "priority": "high",
                "category": "감정 아크",
                "message": f"급격한 감정 전환 {changes}건 검출. 전환에 충분한 동기/복선을 배치하세요.",
            })

        if results["pacing"]["severity"] != "low":
            saggy = len(results["pacing"]["saggy_sections"])
            recs.append({
                "priority": "high",
                "category": "페이싱",
                "message": f"처진 구간 {saggy}건 검출. 새로운 갈등/반전을 투입하세요.",
            })

        if results["translation_artifacts"]["severity"] != "low":
            total_ta = results["translation_artifacts"]["total_found"]
            recs.append({
                "priority": "high",
                "category": "번역투",
                "message": f"번역투 표현 {total_ta}건 검출. 자연스러운 한국어로 교체하세요.",
            })

        if results["deep_pov"]["severity"] != "low":
            total_fw = results["deep_pov"]["total_filter_words"]
            recs.append({
                "priority": "medium",
                "category": "Deep POV",
                "message": f"필터 단어 {total_fw}건 검출. 감각/행동을 직접 서술하여 심리적 거리를 줄이세요.",
            })

        if results["hook_quality"]["severity"] != "low":
            weak = len(results["hook_quality"]["weak_closings"])
            recs.append({
                "priority": "high",
                "category": "후크 품질",
                "message": f"약한 챕터 엔딩 {weak}건. 클리프행어/질문/반전을 추가하세요.",
            })

        if results["readability_korean"]["severity"] != "low":
            score = results["readability_korean"]["readability_score"]
            recs.append({
                "priority": "medium",
                "category": "가독성",
                "message": f"한국어 가독성 점수 {score}/100. 문장 길이 조절과 문단 나누기를 개선하세요.",
            })

        if results.get("webnovel_cliches", {}).get("severity", "low") != "low":
            wn_total = results["webnovel_cliches"]["total_found"]
            recs.append({
                "priority": "medium",
                "category": "웹소설 클리셰",
                "message": f"웹소설 클리셰 {wn_total}건 검출. 독창적인 표현으로 교체하세요.",
            })

        return sorted(recs, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])

    def _save_report(self, report: dict):
        report_dir = self.project_dir / "edits"
        report_dir.mkdir(parents=True, exist_ok=True)

        # JSON
        with open(report_dir / "style_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # Markdown
        md = self._report_to_markdown(report)
        with open(report_dir / "style_report.md", "w", encoding="utf-8") as f:
            f.write(md)

    def _report_to_markdown(self, report: dict) -> str:
        md = f"""# 문체 분석 리포트: {report['title']}

> 분석일시: {report['analyzed_at']}
> 분석 챕터: {report['chapters_analyzed']}개
> **종합 점수: {report['score']}/100**

---

## 개선 권고 사항

"""
        for rec in report["recommendations"]:
            icon = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
            md += f"- {icon} **[{rec['category']}]** {rec['message']}\n"

        md += "\n---\n\n## 상세 분석\n\n"

        analyses = report["analyses"]

        # AI 클리셰
        md += f"### AI 클리셰 검출\n"
        md += f"- 검출 건수: {analyses['ai_cliches']['total_found']}\n"
        md += f"- 고유 패턴 수: {analyses['ai_cliches']['unique_patterns']}\n\n"

        # 부사
        md += f"### 부사 사용\n"
        md += f"- 과도한 부사: {analyses['adverb_usage']['total_excessive_adverbs']}건\n"
        md += f"- 비율: {analyses['adverb_usage']['ratio_pct']}%\n\n"

        # 문장 다양성
        sv = analyses["sentence_variety"]
        if sv.get("total_sentences", 0) > 0:
            md += f"### 문장 다양성\n"
            md += f"- 평균 문장 길이: {sv['average_length']}자\n"
            md += f"- 표준편차: {sv['std_deviation']}\n"
            md += f"- 분포: 단문 {sv['distribution']['short_pct']}% / 중문 {sv['distribution']['medium_pct']}% / 장문 {sv['distribution']['long_pct']}%\n\n"

        # 어휘 다양성
        md += f"### 어휘 다양성 (TTR)\n"
        md += f"- TTR: {analyses['vocabulary_diversity']['overall_ttr']}\n"
        md += f"- 총 토큰: {analyses['vocabulary_diversity']['total_tokens']:,}\n"
        md += f"- 고유 어휘: {analyses['vocabulary_diversity']['unique_types']:,}\n\n"

        # Show vs Tell
        md += f"### Show vs Tell\n"
        md += f"- Tell 비율: {analyses['show_vs_tell']['tell_ratio_pct']}%\n\n"

        # 감각 묘사
        sd = analyses["sensory_detail"]
        md += f"### 감각 묘사\n"
        md += f"- 밀도: {sd['density_pct']}%\n"
        md += f"- 가장 많은 감각: {sd['dominant_sense']}\n"
        md += f"- 가장 부족한 감각: {sd['weakest_sense']}\n"
        for sense, count in sd["by_sense"].items():
            md += f"  - {sense}: {count}회\n"
        md += "\n"

        # === 새로운 분석 섹션 ===

        # 감정 아크
        ea = analyses.get("emotional_arc", {})
        if ea:
            md += f"### 감정 아크 분석\n"
            md += f"- 스토리 형태: {ea.get('story_shape', 'N/A')}\n"
            md += f"- 절정 위치: {ea.get('peak_position_pct', 0)}%\n"
            md += f"- 급격한 감정 전환: {len(ea.get('abrupt_changes', []))}건\n"
            if ea.get("chapter_emotions"):
                md += "- 챕터별 감정 극성:\n"
                for ce in ea["chapter_emotions"]:
                    bar_pos = "+" * max(0, int(ce["polarity"] * 10))
                    bar_neg = "-" * max(0, int(-ce["polarity"] * 10))
                    md += f"  - Ch{ce['chapter']}: {bar_neg}|{bar_pos} ({ce['polarity']:+.3f})\n"
            md += "\n"

        # 페이싱
        pac = analyses.get("pacing", {})
        if pac:
            md += f"### 페이싱 분석\n"
            md += f"- 전체 대화 비율: {pac.get('overall_dialogue_pct', 0)}%\n"
            md += f"- 전체 액션 밀도: {pac.get('overall_action_density', 0)}\n"
            md += f"- 평균 긴장도: {pac.get('overall_tension_avg', 0)}/10\n"
            md += f"- 씬 길이 표준편차: {pac.get('scene_length_std', 0)}\n"
            if pac.get("saggy_sections"):
                md += "- 처진 구간:\n"
                for ss in pac["saggy_sections"]:
                    md += f"  - Ch{ss['start_chapter']}~Ch{ss['end_chapter']} (긴장도 평균: {ss['avg_tension']})\n"
            md += "\n"

        # 번역투
        ta = analyses.get("translation_artifacts", {})
        if ta:
            md += f"### 번역투 검출\n"
            md += f"- 검출 건수: {ta.get('total_found', 0)}\n"
            md += f"- 한국어 자연스러움 점수: {ta.get('naturalness_score', 0)}/100\n"
            if ta.get("pattern_summary"):
                md += "- 상위 패턴:\n"
                for pattern, count in ta["pattern_summary"].items():
                    md += f"  - {pattern}: {count}건\n"
            md += "\n"

        # Deep POV
        dp = analyses.get("deep_pov", {})
        if dp:
            md += f"### Deep POV 분석\n"
            md += f"- 필터 단어 총 건수: {dp.get('total_filter_words', 0)}\n"
            md += f"- 필터 단어 비율: {dp.get('filter_ratio_pct', 0)}%\n"
            md += f"- 심리적 거리: {dp.get('psychic_distance', 'N/A')}\n"
            if dp.get("filter_summary"):
                md += "- 상위 필터 단어:\n"
                for fw, count in dp["filter_summary"].items():
                    md += f"  - {fw}: {count}건\n"
            md += "\n"

        # 후크 품질
        hq = analyses.get("hook_quality", {})
        if hq:
            md += f"### 후크 품질 분석\n"
            md += f"- 평균 오프닝 점수: {hq.get('avg_opening_score', 0)}/10\n"
            md += f"- 평균 클로징 점수: {hq.get('avg_closing_score', 0)}/10\n"
            md += f"- 첫 3화 몰입도: {hq.get('first_three_immersion', 0)}/10\n"
            if hq.get("weak_openings"):
                md += f"- 약한 오프닝 챕터: {', '.join(f'Ch{c}' for c in hq['weak_openings'])}\n"
            if hq.get("weak_closings"):
                md += f"- 약한 클로징 챕터: {', '.join(f'Ch{c}' for c in hq['weak_closings'])}\n"
            md += "\n"

        # 한국어 가독성
        rk = analyses.get("readability_korean", {})
        if rk:
            md += f"### 한국어 가독성 지수\n"
            md += f"- 종합 가독성 점수: {rk.get('readability_score', 0)}/100\n"
            md += f"- 평균 문장 길이: {rk.get('avg_sentence_length', 0)}자\n"
            md += f"- 문장 길이 점수: {rk.get('sentence_length_score', 0)}/100\n"
            md += f"- 종결 다양성 점수: {rk.get('ending_diversity_score', 0)}/100\n"
            md += f"- 의성어/의태어 활용: {rk.get('mimetic_word_count', 0)}개 (점수: {rk.get('mimetic_score', 0)}/100)\n"
            md += f"- 문단 적절성 점수: {rk.get('paragraph_score', 0)}/100\n"
            md += "\n"

        # 웹소설 클리셰
        wc = analyses.get("webnovel_cliches", {})
        if wc:
            md += f"### 웹소설 클리셰 검출\n"
            md += f"- 검출 건수: {wc.get('total_found', 0)}\n"
            if wc.get("by_category"):
                md += "- 카테고리별:\n"
                for cat, count in wc["by_category"].items():
                    md += f"  - {cat}: {count}건\n"
            md += "\n"

        return md


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python style_analyzer.py <project_dir>")
        sys.exit(1)

    analyzer = StyleAnalyzer(sys.argv[1])
    report = analyzer.run_all_analyses()
    print(json.dumps({"score": report["score"], "recommendations": report["recommendations"]}, ensure_ascii=False, indent=2))
