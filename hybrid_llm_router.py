#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
하이브리드 LLM 라우터
노트북LM과 Gemini Pro를 결합하여 문서의 민감도에 따라 최적의 LLM 선택
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv

# 환경 변수 로드
try:
    load_dotenv()
except UnicodeDecodeError:
    load_dotenv(encoding='utf-8')

class HybridLLMRouter:
    def __init__(self):
        self.gemini_api_key_1 = os.getenv('GEMINI_API_KEY_1')
        self.gemini_api_key_2 = os.getenv('GEMINI_API_KEY_2')
        self.sensitivity_keywords = {
            "high": ["비밀", "기밀", "내부", "전략", "재무", "인사", "계약", "특허"],
            "medium": ["분석", "보고서", "검토", "평가", "제안", "계획"],
            "low": ["뉴스", "공개", "일반", "참고", "정보"]
        }
        
    def analyze_sensitivity(self, text: str) -> Dict[str, Any]:
        """문서의 민감도를 분석"""
        print("🔍 문서 민감도 분석 중...")
        
        # 키워드 기반 민감도 분석
        high_count = sum(1 for keyword in self.sensitivity_keywords["high"] if keyword in text)
        medium_count = sum(1 for keyword in self.sensitivity_keywords["medium"] if keyword in text)
        low_count = sum(1 for keyword in self.sensitivity_keywords["low"] if keyword in text)
        
        # 민감도 점수 계산 (1-10점)
        sensitivity_score = 0
        
        if high_count > 0:
            sensitivity_score = 8 + min(high_count, 2)  # 8-10점
        elif medium_count > 0:
            sensitivity_score = 4 + min(medium_count, 3)  # 4-7점
        elif low_count > 0:
            sensitivity_score = 1 + min(low_count, 2)  # 1-3점
        else:
            sensitivity_score = 5  # 기본값
        
        # 민감도 레벨 결정
        if sensitivity_score >= 8:
            level = "high"
            recommended_llm = "notebooklm"
        elif sensitivity_score >= 4:
            level = "medium"
            recommended_llm = "hybrid"
        else:
            level = "low"
            recommended_llm = "gemini_pro"
        
        analysis_result = {
            "sensitivity_score": sensitivity_score,
            "sensitivity_level": level,
            "recommended_llm": recommended_llm,
            "keyword_counts": {
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ 민감도 분석 완료: {sensitivity_score}점 ({level})")
        print(f"🎯 권장 LLM: {recommended_llm}")
        
        return analysis_result
    
    def route_to_llm(self, text: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """분석 결과에 따라 적절한 LLM으로 라우팅"""
        print("🔄 LLM 라우팅 중...")
        
        recommended_llm = analysis_result["recommended_llm"]
        
        if recommended_llm == "notebooklm":
            return self.process_with_notebooklm(text, analysis_result)
        elif recommended_llm == "gemini_pro":
            return self.process_with_gemini_pro(text, analysis_result)
        else:  # hybrid
            return self.process_with_hybrid(text, analysis_result)
    
    def process_with_notebooklm(self, text: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """노트북LM으로 처리 (고민감도 문서)"""
        print("📱 노트북LM으로 처리 중...")
        
        # 시뮬레이션: 노트북LM 처리
        result = {
            "llm_used": "notebooklm",
            "processing_type": "local_secure",
            "extracted_data": {
                "keywords": ["내부전략", "기밀정보", "비즈니스모델"],
                "summary": "고민감도 문서로 인식되어 노트북LM에서 로컬 처리됨",
                "entities": ["내부인물1", "내부인물2"],
                "insights": "개인 경험 기반 분석으로 창의적 인사이트 생성"
            },
            "security_level": "maximum",
            "processing_time": "2.3초",
            "analysis_result": analysis_result
        }
        
        print("✅ 노트북LM 처리 완료")
        return result
    
    def process_with_gemini_pro(self, text: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Gemini Pro로 처리 (저민감도 문서)"""
        print("☁️ Gemini Pro로 처리 중...")
        
        # 시뮬레이션: Gemini Pro 처리
        result = {
            "llm_used": "gemini_pro",
            "processing_type": "cloud_public",
            "extracted_data": {
                "keywords": ["공개정보", "시장동향", "일반뉴스"],
                "summary": "저민감도 문서로 인식되어 Gemini Pro에서 클라우드 처리됨",
                "entities": ["공개인물1", "공개기업1"],
                "insights": "외부 정보 기반 객관적 분석으로 시장 인사이트 생성"
            },
            "security_level": "standard",
            "processing_time": "1.8초",
            "analysis_result": analysis_result
        }
        
        print("✅ Gemini Pro 처리 완료")
        return result
    
    def process_with_hybrid(self, text: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """하이브리드 처리 (중민감도 문서)"""
        print("🔄 하이브리드 처리 중...")
        
        # 시뮬레이션: 하이브리드 처리
        notebooklm_result = self.process_with_notebooklm(text, analysis_result)
        gemini_result = self.process_with_gemini_pro(text, analysis_result)
        
        # 결과 융합
        result = {
            "llm_used": "hybrid",
            "processing_type": "combined_analysis",
            "notebooklm_analysis": notebooklm_result["extracted_data"],
            "gemini_analysis": gemini_result["extracted_data"],
            "combined_insights": {
                "keywords": list(set(notebooklm_result["extracted_data"]["keywords"] + 
                                   gemini_result["extracted_data"]["keywords"])),
                "summary": f"하이브리드 분석: {notebooklm_result['extracted_data']['summary']} + {gemini_result['extracted_data']['summary']}",
                "entities": list(set(notebooklm_result["extracted_data"]["entities"] + 
                                   gemini_result["extracted_data"]["entities"])),
                "insights": "개인 경험과 외부 정보를 결합한 종합적 인사이트"
            },
            "security_level": "enhanced",
            "processing_time": "4.1초",
            "analysis_result": analysis_result
        }
        
        print("✅ 하이브리드 처리 완료")
        return result
    
    def test_hybrid_system(self) -> Dict[str, Any]:
        """하이브리드 시스템 테스트"""
        print("🧪 하이브리드 시스템 테스트 시작...")
        
        test_documents = [
            {
                "name": "고민감도_내부전략문서",
                "content": "이 문서는 회사의 비밀 전략과 기밀 정보를 포함하고 있습니다. 내부 인사 정책과 재무 계획이 담겨있어 외부에 유출되면 안 됩니다."
            },
            {
                "name": "중민감도_분석보고서",
                "content": "시장 분석 보고서입니다. 일반적인 분석 내용과 제안 사항이 포함되어 있으며, 참고 자료로 활용할 수 있습니다."
            },
            {
                "name": "저민감도_공개뉴스",
                "content": "일반적인 뉴스 기사입니다. 공개된 정보와 참고 자료를 바탕으로 작성되었으며, 누구나 접근할 수 있는 내용입니다."
            }
        ]
        
        test_results = []
        
        for doc in test_documents:
            print(f"\n📄 테스트 문서: {doc['name']}")
            
            # 민감도 분석
            sensitivity_analysis = self.analyze_sensitivity(doc["content"])
            
            # LLM 라우팅 및 처리
            processing_result = self.route_to_llm(doc["content"], sensitivity_analysis)
            
            test_result = {
                "document_name": doc["name"],
                "sensitivity_analysis": sensitivity_analysis,
                "processing_result": processing_result
            }
            
            test_results.append(test_result)
        
        overall_result = {
            "test_timestamp": datetime.now().isoformat(),
            "total_documents": len(test_documents),
            "test_results": test_results,
            "system_status": "operational"
        }
        
        print(f"\n✅ 하이브리드 시스템 테스트 완료: {len(test_documents)}개 문서 처리")
        return overall_result

def main():
    """메인 실행 함수"""
    print("🎯 하이브리드 LLM 라우터 시작")
    
    # 하이브리드 라우터 초기화
    router = HybridLLMRouter()
    
    # 하이브리드 시스템 테스트 실행
    test_result = router.test_hybrid_system()
    
    # 결과 저장
    with open('hybrid_system_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)
    
    print("🎉 하이브리드 시스템 테스트 완료!")
    print("📊 결과가 hybrid_system_test_results.json에 저장되었습니다.")

if __name__ == "__main__":
    main()
