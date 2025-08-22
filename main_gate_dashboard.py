#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MainGate 대시보드 생성기
GIA_INFOSYS 워크스페이스의 MainGate 페이지에 최적화된 대시보드 생성
"""

import os
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

# 환경 변수 로드
try:
    load_dotenv()
except UnicodeDecodeError:
    load_dotenv(encoding='utf-8')

class MainGateDashboard:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.main_gate_page_id = os.getenv('NOTION_DATABASE_ID')
        self.notion = Client(auth=self.notion_token)
        
    def create_dashboard(self):
        """MainGate 페이지에 완전한 대시보드 생성"""
        try:
            print("🎯 MainGate 대시보드 생성 시작...")
            
            # 1. 헤더 섹션
            self.create_header()
            
            # 2. 실시간 상태
            self.create_status_section()
            
            # 3. 빠른 접근 메뉴
            self.create_quick_menu()
            
            # 4. 성과 통계
            self.create_stats_section()
            
            # 5. 알림 섹션
            self.create_notifications()
            
            print("✅ MainGate 대시보드 생성 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 대시보드 생성 실패: {e}")
            return False
    
    def create_header(self):
        """헤더 섹션 생성"""
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"text": {"content": "🎯 GIA_INFOSYS - MainGate"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "개인 정보체계 구축 프로젝트 중앙 허브"}}]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            }
        ]
        
        self.notion.blocks.children.append(self.main_gate_page_id, children=blocks)
        print("✅ 헤더 섹션 생성 완료")
    
    def create_status_section(self):
        """실시간 상태 섹션"""
        blocks = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "📊 실시간 시스템 상태"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": "🟢"},
                    "rich_text": [{"text": {"content": "시스템 상태: 정상 운영 중"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": "⚡"},
                    "rich_text": [{"text": {"content": "LLM 엔진: Gemini Pro + 노트북LM 하이브리드"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": "🔗"},
                    "rich_text": [{"text": {"content": "노션 연동: 완벽 동기화"}}]
                }
            }
        ]
        
        self.notion.blocks.children.append(self.main_gate_page_id, children=blocks)
        print("✅ 실시간 상태 섹션 생성 완료")
    
    def create_quick_menu(self):
        """빠른 접근 메뉴"""
        blocks = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "🗂️ 핵심 데이터베이스"}}]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "📄 Documents_Master"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": "모든 문서의 중앙 집중 관리"}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "📋 Projects_Master"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": "GitMind 연동 프로젝트 관리"}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "🧠 Knowledge_Graph"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": "지식 연결망 및 관계형 데이터"}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "👥 People_Network"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": "인적 네트워크 관리 및 확장"}}]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [{"text": {"content": "💡 Ideas_Incubator"}}],
                    "children": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": "아이디어 육성 및 실행 시스템"}}]
                            }
                        }
                    ]
                }
            }
        ]
        
        self.notion.blocks.children.append(self.main_gate_page_id, children=blocks)
        print("✅ 빠른 접근 메뉴 생성 완료")
    
    def create_stats_section(self):
        """성과 통계 섹션"""
        blocks = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "📈 성과 및 통계"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": "📄"},
                    "rich_text": [{"text": {"content": "처리된 문서: 0건"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": "🎯"},
                    "rich_text": [{"text": {"content": "생성된 인사이트: 0건"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": "👥"},
                    "rich_text": [{"text": {"content": "네트워크 확장: 0명"}}]
                }
            }
        ]
        
        self.notion.blocks.children.append(self.main_gate_page_id, children=blocks)
        print("✅ 성과 통계 섹션 생성 완료")
    
    def create_notifications(self):
        """알림 섹션"""
        blocks = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "🔔 알림 및 업데이트"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": "🎉"},
                    "rich_text": [{"text": {"content": "GIA 시스템 초기 구축 완료!"}}]
                }
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"emoji": "🚀"},
                    "rich_text": [{"text": {"content": "다음 단계: 노트북LM 프로젝트 세팅"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "🛠️ 개발: 서대리 | 🎯 기획: 나실장 | 🧠 설계: 노팀장"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "📅 업데이트: " + datetime.now().strftime("%Y년 %m월 %d일 %H:%M")}}]
                }
            }
        ]
        
        self.notion.blocks.children.append(self.main_gate_page_id, children=blocks)
        print("✅ 알림 섹션 생성 완료")

def main():
    """메인 실행 함수"""
    print("🎯 MainGate 대시보드 생성기 시작")
    
    dashboard = MainGateDashboard()
    success = dashboard.create_dashboard()
    
    if success:
        print("🎉 MainGate 대시보드 생성 완료!")
        print("📱 노션에서 MainGate 페이지를 확인해보세요!")
    else:
        print("❌ 대시보드 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
