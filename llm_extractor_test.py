#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm_extractor_test.py
- Gemini Pro API를 사용해 핵심 키워드, 요약, 관련 인물 추출 테스트
- google.generativeai 미설치/키 미설정 시 시뮬레이션 모드로 동작
"""

import os
import sys
from typing import Dict, Any

# 로깅
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 환경변수 로드 (인코딩 오류 무시)
try:
    from dotenv import load_dotenv
    try:
        load_dotenv(encoding='utf-8')
    except Exception as e:
        logger.warning(f".env 로드 중 인코딩/파싱 오류 무시: {e}")
except Exception as e:  # dotenv 자체가 없을 때
    logger.warning(f"python-dotenv 미설치: {e}")

GEMINI_KEY = os.getenv('GEMINI_API_KEY_1') or os.getenv('GEMINI_API_KEY_2')
MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')


def simulate_extract(text: str) -> Dict[str, Any]:
    return {
        'keywords': ['GIA_INFOSYS', '문서 파싱', 'Notion 연동'],
        'summary': '문서에서 핵심 내용을 추출하고 노션에 저장하는 파이프라인 테스트.',
        'entities': ['조대표', '나실장', '서대리']
    }


def real_extract(text: str) -> Dict[str, Any]:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        prompt = (
            "다음 텍스트의 핵심 키워드(최대 8개), 2문장 요약, 관련 인물(있으면) 리스트를 JSON으로만 출력하세요.\n"
            "필드: keywords(list), summary(str), entities(list). 텍스트:\n" + text
        )
        model = genai.GenerativeModel(MODEL)
        resp = model.generate_content(prompt)
        content = resp.text.strip()
        import json
        return json.loads(content)
    except Exception as e:
        logger.warning(f"Gemini 호출 실패, 시뮬레이션으로 대체: {e}")
        return simulate_extract(text)


def main():
    sample_text = (
        "GIA_INFOSYS 프로젝트는 DOCX, PPTX, PDF 문서에서 텍스트를 추출하고, 핵심 키워드와 요약을 생성하여 "
        "Notion 데이터베이스에 저장하는 시스템이다. 나실장은 기획, 노팀장은 기술자문, 서대리는 개발을 담당한다."
    )

    if not GEMINI_KEY:
        logger.info("GEMINI_API_KEY 미설정: 시뮬레이션 모드로 실행")
        result = simulate_extract(sample_text)
    else:
        result = real_extract(sample_text)

    print("=== LLM 추출 결과 ===")
    print(result)
    return True


if __name__ == '__main__':
    main()
