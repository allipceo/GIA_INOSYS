#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GIA_INFOSYS 통합 테스트 스크립트
Phase 2-1, 과업 1: 전체 시스템 통합 테스트

작성일: 2025년 8월 22일
작성자: 서대리 (Lead Developer)
목적: 문서 파싱 및 Notion 연동 전체 시스템 테스트
"""

import os
import sys
import subprocess
from datetime import datetime
from typing import Dict, Any

# 로깅 설정
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integration_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class IntegrationTest:
    """통합 테스트 클래스"""
    
    def __init__(self):
        """초기화"""
        self.test_results = {}
        self.start_time = datetime.now()
    
    def run_document_parser_test(self) -> bool:
        """
        문서 파싱 테스트 실행
        
        Returns:
            bool: 테스트 성공 여부
        """
        logger.info("=== 문서 파싱 테스트 실행 ===")
        
        try:
            # document_parser_test.py 실행
            result = subprocess.run(
                [sys.executable, "document_parser_test.py"],
                capture_output=True,
                text=True,
                timeout=300  # 5분 타임아웃
            )
            
            if result.returncode == 0:
                logger.info("✅ 문서 파싱 테스트 성공")
                self.test_results['document_parser'] = {
                    'success': True,
                    'output': result.stdout,
                    'error': result.stderr
                }
                return True
            else:
                logger.error(f"❌ 문서 파싱 테스트 실패: {result.stderr}")
                self.test_results['document_parser'] = {
                    'success': False,
                    'output': result.stdout,
                    'error': result.stderr
                }
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ 문서 파싱 테스트 타임아웃")
            self.test_results['document_parser'] = {
                'success': False,
                'error': 'Timeout'
            }
            return False
        except Exception as e:
            logger.error(f"❌ 문서 파싱 테스트 오류: {str(e)}")
            self.test_results['document_parser'] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    def run_notion_integration_test(self) -> bool:
        """
        Notion 연동 테스트 실행
        
        Returns:
            bool: 테스트 성공 여부
        """
        logger.info("=== Notion 연동 테스트 실행 ===")
        
        try:
            # notion_integration_test.py 실행
            result = subprocess.run(
                [sys.executable, "notion_integration_test.py"],
                capture_output=True,
                text=True,
                timeout=300  # 5분 타임아웃
            )
            
            if result.returncode == 0:
                logger.info("✅ Notion 연동 테스트 성공")
                self.test_results['notion_integration'] = {
                    'success': True,
                    'output': result.stdout,
                    'error': result.stderr
                }
                return True
            else:
                logger.error(f"❌ Notion 연동 테스트 실패: {result.stderr}")
                self.test_results['notion_integration'] = {
                    'success': False,
                    'output': result.stdout,
                    'error': result.stderr
                }
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Notion 연동 테스트 타임아웃")
            self.test_results['notion_integration'] = {
                'success': False,
                'error': 'Timeout'
            }
            return False
        except Exception as e:
            logger.error(f"❌ Notion 연동 테스트 오류: {str(e)}")
            self.test_results['notion_integration'] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    def check_environment(self) -> bool:
        """
        개발 환경 체크
        
        Returns:
            bool: 환경 체크 성공 여부
        """
        logger.info("=== 개발 환경 체크 ===")
        
        # 필요한 파일들 체크
        required_files = [
            "requirements.txt",
            "document_parser_test.py",
            "notion_integration_test.py"
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            logger.error(f"❌ 누락된 파일들: {missing_files}")
            return False
        
        # .env 파일 체크
        if not os.path.exists(".env"):
            logger.warning("⚠️ .env 파일이 없습니다. env_template.txt를 참조하여 생성하세요.")
        
        logger.info("✅ 개발 환경 체크 완료")
        return True
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        모든 테스트 실행
        
        Returns:
            Dict[str, Any]: 전체 테스트 결과
        """
        logger.info("=== GIA_INFOSYS 통합 테스트 시작 ===")
        
        # 환경 체크
        if not self.check_environment():
            return {"success": False, "error": "환경 체크 실패"}
        
        # 문서 파싱 테스트
        parser_success = self.run_document_parser_test()
        
        # Notion 연동 테스트 (문서 파싱이 성공한 경우에만)
        notion_success = False
        if parser_success:
            notion_success = self.run_notion_integration_test()
        else:
            logger.warning("문서 파싱 테스트가 실패하여 Notion 연동 테스트를 건너뜁니다.")
        
        # 전체 결과 계산
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        overall_success = parser_success and notion_success
        
        final_result = {
            "success": overall_success,
            "duration": str(duration),
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "test_results": self.test_results,
            "summary": {
                "document_parser": parser_success,
                "notion_integration": notion_success,
                "overall": overall_success
            }
        }
        
        logger.info("=== GIA_INFOSYS 통합 테스트 완료 ===")
        return final_result
    
    def print_results(self, results: Dict[str, Any]):
        """
        테스트 결과 출력
        
        Args:
            results (Dict[str, Any]): 테스트 결과
        """
        print("\n" + "="*60)
        print("GIA_INFOSYS 통합 테스트 결과")
        print("="*60)
        
        print(f"테스트 시작 시간: {results['start_time']}")
        print(f"테스트 종료 시간: {results['end_time']}")
        print(f"총 소요 시간: {results['duration']}")
        print()
        
        print("=== 개별 테스트 결과 ===")
        summary = results['summary']
        
        # 문서 파싱 테스트 결과
        parser_status = "✅ 성공" if summary['document_parser'] else "❌ 실패"
        print(f"문서 파싱 테스트: {parser_status}")
        
        # Notion 연동 테스트 결과
        notion_status = "✅ 성공" if summary['notion_integration'] else "❌ 실패"
        print(f"Notion 연동 테스트: {notion_status}")
        
        print()
        
        # 전체 결과
        overall_status = "🎉 모든 테스트 성공!" if results['success'] else "⚠️ 일부 테스트 실패"
        print(f"전체 결과: {overall_status}")
        
        print("\n" + "="*60)
        
        # 상세 결과 (실패한 경우)
        if not results['success']:
            print("\n=== 상세 오류 정보 ===")
            for test_name, test_result in results['test_results'].items():
                if not test_result['success']:
                    print(f"\n{test_name}:")
                    if 'error' in test_result:
                        print(f"  오류: {test_result['error']}")
                    if 'output' in test_result and test_result['output']:
                        print(f"  출력: {test_result['output'][:500]}...")

def main():
    """메인 실행 함수"""
    print("=== GIA_INFOSYS 통합 테스트 시작 ===")
    
    # IntegrationTest 인스턴스 생성
    integration_test = IntegrationTest()
    
    # 모든 테스트 실행
    results = integration_test.run_all_tests()
    
    # 결과 출력
    integration_test.print_results(results)
    
    return results['success']

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
