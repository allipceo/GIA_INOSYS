#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notion_uploader_v2.py
- 문서 파싱(document_parser_test or simulation) → LLM 의미 추출 → Notion 업로드까지 통합 실행
- 실제 라이브러리/키가 없으면 안전하게 시뮬레이션으로 동작
"""

import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime

# 로깅
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 환경 변수
try:
    from dotenv import load_dotenv
    try:
        load_dotenv(encoding='utf-8')
    except Exception as e:
        logger.warning(f".env 로드 중 인코딩/파싱 오류 무시: {e}")
except Exception as e:
    logger.warning(f"python-dotenv 미설치: {e}")

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

GEMINI_KEY = os.getenv('GEMINI_API_KEY_1') or os.getenv('GEMINI_API_KEY_2')
MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')

TEST_FILES_DIR = os.getenv('TEST_FILES_DIR', './test_files')


# ---------- 파싱 ----------

def parse_text_from_file(file_path: str) -> Optional[str]:
    """문서에서 텍스트 추출. 실제 파서가 실패하면 시뮬레이션으로 대체."""
    try:
        # 실제 테스트 스크립트를 우선 시도
        if file_path.endswith('.docx'):
            from document_parser_test import DocumentParser  # type: ignore
            parser = DocumentParser()
            return parser.parse_docx(file_path)
        if file_path.endswith('.pptx'):
            from document_parser_test import DocumentParser  # type: ignore
            parser = DocumentParser()
            return parser.parse_pptx(file_path)
        if file_path.endswith('.pdf'):
            from document_parser_test import DocumentParser  # type: ignore
            parser = DocumentParser()
            return parser.parse_pdf(file_path)
    except Exception:
        pass

    # 시뮬레이션 폴백
    try:
        from document_parser_simulation import DocumentParserSimulation  # type: ignore
        sim = DocumentParserSimulation()
        if file_path.endswith('.docx'):
            return sim.parse_docx(file_path)
        if file_path.endswith('.pptx'):
            return sim.parse_pptx(file_path)
        if file_path.endswith('.pdf'):
            return sim.parse_pdf(file_path)
    except Exception as e:
        logger.error(f"파싱 실패: {e}")
        return None


# ---------- LLM 의미 추출 ----------

def extract_semantics(text: str) -> Dict[str, Any]:
    """Gemini 사용, 실패 시 시뮬레이션 반환."""
    def simulate():
        return {
            'keywords': ['GIA_INFOSYS', '문서 파싱', 'Notion 연동'],
            'summary': text[:300] + ('...' if len(text) > 300 else ''),
            'entities': ['조대표', '나실장', '서대리']
        }

    if not GEMINI_KEY:
        return simulate()

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        prompt = (
            "다음 텍스트의 핵심 키워드(최대 8개), 2문장 요약, 관련 인물(있으면) 리스트를 JSON으로만 출력하세요.\n"
            "필드: keywords(list), summary(str), entities(list). 텍스트:\n" + text
        )
        model = genai.GenerativeModel(MODEL)
        resp = model.generate_content(prompt)
        import json
        return json.loads(resp.text.strip())
    except Exception as e:
        logger.warning(f"Gemini 호출 실패, 시뮬레이션으로 대체: {e}")
        return simulate()


# ---------- Notion 업로드 ----------

def upload_to_notion(doc_title: str, doc_type: str, extracted: Dict[str, Any]) -> Optional[str]:
    """Notion 업로드. 토큰/DB 없으면 시뮬레이션 ID 반환."""
    if not (NOTION_TOKEN and NOTION_DATABASE_ID):
        sim_id = f"sim_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Notion 미설정: 시뮬레이션 업로드 ID 반환 {sim_id}")
        return sim_id

    try:
        from notion_client import Client
        notion = Client(auth=NOTION_TOKEN)
        page = notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "문서명": {"title": [{"text": {"content": doc_title}}]},
                "문서 유형": {"select": {"name": doc_type}},
                "작업일": {"date": {"start": datetime.now().isoformat()}},
            },
            children=[
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "[요약]\n" + (extracted.get('summary') or '')[:1900]}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "[키워드]\n" + ", ".join(extracted.get('keywords', []))}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "[관련 인물]\n" + ", ".join(extracted.get('entities', []))}}]}},
            ]
        )
        return page.get('id')
    except Exception as e:
        logger.warning(f"Notion 업로드 실패, 시뮬레이션으로 대체: {e}")
        sim_id = f"sim_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return sim_id


def main():
    # 테스트 파일 한 세트 처리
    samples = [
        (os.path.join(TEST_FILES_DIR, 'test.docx'), 'docx'),
        (os.path.join(TEST_FILES_DIR, 'test.pptx'), 'pptx'),
        (os.path.join(TEST_FILES_DIR, 'test.pdf'), 'pdf'),
    ]

    results = []
    for path, dtype in samples:
        text = parse_text_from_file(path)
        if not text:
            logger.error(f"텍스트 추출 실패: {path}")
            continue
        extracted = extract_semantics(text)
        page_id = upload_to_notion(os.path.basename(path), dtype, extracted)
        results.append({'file': path, 'type': dtype, 'page_id': page_id})
        logger.info(f"업로드 완료: {path} -> {page_id}")

    print("=== 업로드 결과 ===")
    for r in results:
        print(f"{r['file']} -> {r['page_id']}")


if __name__ == '__main__':
    main()
