#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GIA_INFOSYS 지식 그래프 통합 테스트 스크립트
Phase 2-2, 과업 1: 지식 그래프 및 인사이트 시스템 통합 테스트

작성일: 2025년 8월 22일
작성자: 서대리 (Lead Developer)
목적: 지식 그래프 시뮬레이터와 Notion 업로더 v3의 통합 테스트
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

# 로깅 설정
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('knowledge_graph_integration_test.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_knowledge_graph_simulator_test():
    """지식 그래프 시뮬레이터 테스트"""
    logger.info("=== 지식 그래프 시뮬레이터 테스트 시작 ===")
    
    try:
        from knowledge_graph_simulator import KnowledgeGraphSimulator
        
        simulator = KnowledgeGraphSimulator()
        
        # 1. DB 생성 테스트
        db_result = simulator.create_entity_database()
        logger.info(f"DB 생성 테스트 결과: {db_result['database_name']}")
        
        # 2. 문서 처리 테스트
        test_docs = [
            {
                "title": "GIA_INFOSYS 프로젝트 기획서",
                "content": "조대표님의 개인정보시스템 구축을 위한 GIA_INFOSYS 프로젝트입니다."
            },
            {
                "title": "AI 기술 적용 방안",
                "content": "Notion API와 Gemini Pro API를 연동하여 문서에서 의미를 추출합니다."
            }
        ]
        
        processing_results = []
        for doc in test_docs:
            result = simulator.simulate_document_processing(doc["title"], doc["content"])
            processing_results.append(result)
            logger.info(f"문서 처리 완료: {doc['title']}")
        
        # 3. 통계 확인
        stats = simulator.get_entity_statistics()
        logger.info(f"통계 정보: {stats}")
        
        return {
            "success": True,
            "database_created": True,
            "documents_processed": len(processing_results),
            "entities_created": stats['total_entities'],
            "insights_generated": stats['total_insights']
        }
        
    except Exception as e:
        logger.error(f"지식 그래프 시뮬레이터 테스트 실패: {str(e)}")
        return {"success": False, "error": str(e)}

def run_notion_uploader_v3_test():
    """Notion 업로더 v3 테스트"""
    logger.info("=== Notion 업로더 v3 테스트 시작 ===")
    
    try:
        from notion_uploader_v3 import NotionUploaderV3
        
        uploader = NotionUploaderV3()
        results = uploader.run_knowledge_graph_pipeline()
        
        logger.info(f"업로더 v3 테스트 결과: {results}")
        
        return results
        
    except Exception as e:
        logger.error(f"Notion 업로더 v3 테스트 실패: {str(e)}")
        return {"success": False, "error": str(e)}

def run_integration_test():
    """통합 테스트 실행"""
    logger.info("=== 지식 그래프 통합 테스트 시작 ===")
    
    # 1. 지식 그래프 시뮬레이터 테스트
    simulator_result = run_knowledge_graph_simulator_test()
    
    # 2. Notion 업로더 v3 테스트
    uploader_result = run_notion_uploader_v3_test()
    
    # 3. 통합 결과 분석
    overall_success = simulator_result.get('success', False) and uploader_result.get('success', False)
    
    integration_result = {
        "overall_success": overall_success,
        "simulator_test": simulator_result,
        "uploader_test": uploader_result,
        "test_timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"통합 테스트 완료: {'성공' if overall_success else '실패'}")
    
    return integration_result

def main():
    """메인 실행 함수"""
    print("=== GIA_INFOSYS 지식 그래프 통합 테스트 시작 ===")
    
    # 통합 테스트 실행
    result = run_integration_test()
    
    print("\n=== 통합 테스트 결과 ===")
    print(f"전체 성공: {'✅ 성공' if result['overall_success'] else '❌ 실패'}")
    
    print(f"\n📊 시뮬레이터 테스트:")
    simulator = result['simulator_test']
    if simulator.get('success'):
        print(f"  ✅ DB 생성: 성공")
        print(f"  ✅ 문서 처리: {simulator.get('documents_processed', 0)}개")
        print(f"  ✅ 개체 생성: {simulator.get('entities_created', 0)}개")
        print(f"  ✅ 인사이트 생성: {simulator.get('insights_generated', 0)}개")
    else:
        print(f"  ❌ 실패: {simulator.get('error', '알 수 없는 오류')}")
    
    print(f"\n📊 업로더 v3 테스트:")
    uploader = result['uploader_test']
    if uploader.get('success'):
        print(f"  ✅ 파이프라인 실행: 성공")
        print(f"  ✅ 파일 처리: {uploader.get('success_count', 0)}/{uploader.get('total_files', 0)}")
        print(f"  ✅ 총 개체: {uploader.get('total_entities', 0)}개")
        print(f"  ✅ 총 인사이트: {uploader.get('total_insights', 0)}개")
    else:
        print(f"  ❌ 실패: {uploader.get('error', '알 수 없는 오류')}")
    
    print(f"\n🎯 최종 결과: {'🎉 지식 그래프 시스템 통합 성공!' if result['overall_success'] else '⚠️ 통합 테스트 실패!'}")
    
    return result['overall_success']

if __name__ == "__main__":
    main()
