#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GIA_INFOSYS Notion 연동 테스트 스크립트
Phase 2-1, 과업 1: Notion DB 연동 테스트

작성일: 2025년 8월 22일
작성자: 서대리 (Lead Developer)
목적: Notion 임시 테스트용 DB에 파싱된 문서 데이터 입력 테스트
"""

import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# Notion API
from notion_client import Client
from notion_client.errors import APIResponseError

# 환경 변수
from dotenv import load_dotenv

# 로깅 설정
import logging

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('notion_integration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class NotionIntegration:
    """Notion 연동 클래스"""
    
    def __init__(self):
        """초기화"""
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')
        
        if not self.notion_token:
            logger.error("Notion 토큰이 설정되지 않았습니다.")
            self.notion_client = None
            return
        
        if not self.notion_database_id:
            logger.error("Notion 데이터베이스 ID가 설정되지 않았습니다.")
            self.notion_client = None
            return
        
        try:
            self.notion_client = Client(auth=self.notion_token)
            logger.info("Notion 클라이언트 초기화 성공")
        except Exception as e:
            logger.error(f"Notion 클라이언트 초기화 실패: {str(e)}")
            self.notion_client = None
    
    def test_connection(self) -> bool:
        """
        Notion 연결을 테스트하는 함수
        
        Returns:
            bool: 연결 성공 여부
        """
        if not self.notion_client:
            return False
        
        try:
            # 데이터베이스 정보 조회
            database = self.notion_client.databases.retrieve(self.notion_database_id)
            logger.info(f"Notion 연결 성공: {database.get('title', [{}])[0].get('plain_text', 'Unknown')}")
            return True
        except APIResponseError as e:
            logger.error(f"Notion API 오류: {e.code} - {e.message}")
            return False
        except Exception as e:
            logger.error(f"Notion 연결 실패: {str(e)}")
            return False
    
    def get_database_schema(self) -> Optional[Dict[str, Any]]:
        """
        데이터베이스 스키마를 조회하는 함수
        
        Returns:
            Dict[str, Any]: 데이터베이스 스키마
        """
        if not self.notion_client:
            return None
        
        try:
            database = self.notion_client.databases.retrieve(self.notion_database_id)
            properties = database.get('properties', {})
            
            logger.info("=== 데이터베이스 스키마 ===")
            for prop_name, prop_info in properties.items():
                prop_type = prop_info.get('type', 'unknown')
                logger.info(f"  {prop_name}: {prop_type}")
            
            return properties
        except Exception as e:
            logger.error(f"스키마 조회 실패: {str(e)}")
            return None
    
    def add_document_to_notion(self, document_data: Dict[str, Any]) -> Optional[str]:
        """
        문서 데이터를 Notion DB에 추가하는 함수
        
        Args:
            document_data (Dict[str, Any]): 문서 데이터
                - title: 문서명
                - doc_type: 문서 유형 (docx, pptx, pdf)
                - content: 추출된 텍스트
                - file_path: 파일 경로
        
        Returns:
            str: 생성된 페이지 ID
        """
        if not self.notion_client:
            logger.error("Notion 클라이언트가 초기화되지 않았습니다.")
            return None
        
        try:
            # Notion 페이지 생성 데이터 준비
            page_data = {
                "parent": {"database_id": self.notion_database_id},
                "properties": {
                    "문서명": {
                        "title": [
                            {
                                "text": {
                                    "content": document_data.get('title', 'Unknown Document')
                                }
                            }
                        ]
                    },
                    "문서 유형": {
                        "select": {
                            "name": document_data.get('doc_type', 'unknown')
                        }
                    },
                    "작업일": {
                        "date": {
                            "start": datetime.now().isoformat()
                        }
                    }
                },
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": document_data.get('content', '')[:2000]  # Notion 제한
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
            
            # 페이지 생성
            response = self.notion_client.pages.create(**page_data)
            page_id = response.get('id')
            
            logger.info(f"문서 추가 성공: {document_data.get('title')} (ID: {page_id})")
            return page_id
            
        except APIResponseError as e:
            logger.error(f"Notion API 오류: {e.code} - {e.message}")
            return None
        except Exception as e:
            logger.error(f"문서 추가 실패: {str(e)}")
            return None
    
    def test_document_upload(self) -> Dict[str, Any]:
        """
        문서 업로드 테스트를 실행하는 함수
        
        Returns:
            Dict[str, Any]: 테스트 결과
        """
        logger.info("=== Notion 문서 업로드 테스트 시작 ===")
        
        # 연결 테스트
        if not self.test_connection():
            return {"success": False, "error": "Notion 연결 실패"}
        
        # 스키마 조회
        schema = self.get_database_schema()
        if not schema:
            return {"success": False, "error": "스키마 조회 실패"}
        
        # 테스트 문서 데이터
        test_documents = [
            {
                "title": "GIA_INFOSYS DOCX 테스트 문서",
                "doc_type": "docx",
                "content": "이것은 DOCX 파일 파싱 테스트를 위한 샘플 문서입니다. 다양한 내용을 포함하고 있습니다. 테스트 성공 시 Notion DB에 저장됩니다.",
                "file_path": "./test_files/test.docx"
            },
            {
                "title": "GIA_INFOSYS PPTX 테스트 프레젠테이션",
                "doc_type": "pptx",
                "content": "이것은 PPTX 파일 파싱 테스트를 위한 샘플 프레젠테이션입니다. 다양한 슬라이드 내용을 포함합니다. 테스트 성공 시 Notion DB에 저장됩니다.",
                "file_path": "./test_files/test.pptx"
            },
            {
                "title": "GIA_INFOSYS PDF 테스트 문서",
                "doc_type": "pdf",
                "content": "이것은 PDF 파일 파싱 테스트를 위한 샘플 문서입니다. 다양한 내용을 포함하고 있습니다. 테스트 성공 시 Notion DB에 저장됩니다.",
                "file_path": "./test_files/test.pdf"
            }
        ]
        
        results = []
        success_count = 0
        
        # 각 테스트 문서 업로드
        for doc_data in test_documents:
            logger.info(f"업로드 중: {doc_data['title']}")
            
            page_id = self.add_document_to_notion(doc_data)
            if page_id:
                results.append({
                    "title": doc_data["title"],
                    "doc_type": doc_data["doc_type"],
                    "success": True,
                    "page_id": page_id
                })
                success_count += 1
            else:
                results.append({
                    "title": doc_data["title"],
                    "doc_type": doc_data["doc_type"],
                    "success": False,
                    "error": "업로드 실패"
                })
        
        logger.info("=== Notion 문서 업로드 테스트 완료 ===")
        
        return {
            "success": success_count == len(test_documents),
            "total_documents": len(test_documents),
            "success_count": success_count,
            "results": results
        }

def main():
    """메인 실행 함수"""
    print("=== GIA_INFOSYS Notion 연동 테스트 시작 ===")
    
    # NotionIntegration 인스턴스 생성
    notion_integration = NotionIntegration()
    
    # 연결 테스트
    if not notion_integration.test_connection():
        print("❌ Notion 연결 실패")
        print("다음 사항을 확인하세요:")
        print("1. .env 파일에 NOTION_TOKEN이 설정되어 있는지 확인")
        print("2. .env 파일에 NOTION_DATABASE_ID가 설정되어 있는지 확인")
        print("3. Notion Integration이 올바르게 설정되어 있는지 확인")
        return False
    
    # 스키마 조회
    schema = notion_integration.get_database_schema()
    if not schema:
        print("❌ 데이터베이스 스키마 조회 실패")
        return False
    
    # 문서 업로드 테스트
    test_result = notion_integration.test_document_upload()
    
    # 결과 출력
    print("\n=== 테스트 결과 ===")
    print(f"전체 문서 수: {test_result['total_documents']}")
    print(f"성공한 문서 수: {test_result['success_count']}")
    print(f"성공률: {test_result['success_count']}/{test_result['total_documents']}")
    
    if test_result['success']:
        print("🎉 모든 문서 업로드 테스트가 성공했습니다!")
    else:
        print("⚠️ 일부 문서 업로드 테스트가 실패했습니다.")
    
    print("\n=== 상세 결과 ===")
    for result in test_result['results']:
        status = "✅ 성공" if result['success'] else "❌ 실패"
        print(f"{result['title']}: {status}")
        if result['success']:
            print(f"  - 페이지 ID: {result['page_id']}")
        else:
            print(f"  - 오류: {result.get('error', 'Unknown error')}")
    
    return test_result['success']

if __name__ == "__main__":
    main()
