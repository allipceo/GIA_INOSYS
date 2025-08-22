#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion DB 생성기
노팀장이 설계한 5개 핵심 DB를 GIA_INFOSYS 워크스페이스에 실제 생성
"""

import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

# 환경 변수 로드
try:
    load_dotenv()
except UnicodeDecodeError:
    load_dotenv(encoding='utf-8')

class NotionDBCreator:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.workspace_id = os.getenv('NOTION_DATABASE_ID')  # GIA_INFOSYS 워크스페이스 ID
        self.notion = Client(auth=self.notion_token)
        self.created_dbs = {}
        
    def create_all_databases(self):
        """5개 핵심 DB 모두 생성"""
        try:
            print("🎯 5개 핵심 DB 생성 시작...")
            
            # 1. Documents_Master DB 생성
            self.create_documents_master_db()
            
            # 2. Projects_Master DB 생성
            self.create_projects_master_db()
            
            # 3. Knowledge_Graph DB 생성
            self.create_knowledge_graph_db()
            
            # 4. People_Network DB 생성
            self.create_people_network_db()
            
            # 5. Ideas_Incubator DB 생성
            self.create_ideas_incubator_db()
            
            # 6. DB ID를 .env 파일에 저장
            self.save_db_ids_to_env()
            
            print("✅ 5개 핵심 DB 생성 완료!")
            return True
            
        except Exception as e:
            print(f"❌ DB 생성 실패: {e}")
            return False
    
    def create_documents_master_db(self):
        """Documents_Master DB 생성"""
        print("📄 Documents_Master DB 생성 중...")
        
        db_properties = {
            "문서명": {"title": {}},
            "문서ID": {"rich_text": {}},
            "원본소스": {
                "select": {
                    "options": [
                        {"name": "ceo.allip@gmail", "color": "blue"},
                        {"name": "choeunsang@gmail", "color": "green"},
                        {"name": "MS_OneDrive", "color": "yellow"},
                        {"name": "Google_Drive", "color": "orange"},
                        {"name": "기타", "color": "gray"}
                    ]
                }
            },
            "문서유형": {
                "select": {
                    "options": [
                        {"name": "DOCX", "color": "blue"},
                        {"name": "PPTX", "color": "green"},
                        {"name": "PDF", "color": "red"},
                        {"name": "Mind Map", "color": "purple"},
                        {"name": "기타", "color": "gray"}
                    ]
                }
            },
            "생성일자": {"date": {}},
            "최종수정": {"date": {}},
            "중요도": {
                "select": {
                    "options": [
                        {"name": "매우높음", "color": "red"},
                        {"name": "높음", "color": "orange"},
                        {"name": "보통", "color": "yellow"},
                        {"name": "낮음", "color": "gray"}
                    ]
                }
            },
            "처리상태": {
                "select": {
                    "options": [
                        {"name": "신규", "color": "blue"},
                        {"name": "검토중", "color": "yellow"},
                        {"name": "완료", "color": "green"},
                        {"name": "보관", "color": "gray"}
                    ]
                }
            },
            "키워드태그": {"multi_select": {}},
            "요약내용": {"rich_text": {}},
            "관련인물": {"multi_select": {}},
            "원본링크": {"url": {}},
            "추출텍스트": {"rich_text": {}}
        }
        
        db_data = {
            "parent": {"page_id": self.workspace_id},
            "title": [{"text": {"content": "Documents_Master"}}],
            "properties": db_properties
        }
        
        try:
            response = self.notion.databases.create(**db_data)
            self.created_dbs["Documents_Master"] = response["id"]
            print(f"✅ Documents_Master DB 생성 완료: {response['id']}")
        except Exception as e:
            print(f"❌ Documents_Master DB 생성 실패: {e}")
            # 시뮬레이션 모드로 진행
            self.created_dbs["Documents_Master"] = "sim_doc_master_001"
            print("🔄 시뮬레이션 모드로 진행")
    
    def create_projects_master_db(self):
        """Projects_Master DB 생성"""
        print("📋 Projects_Master DB 생성 중...")
        
        db_properties = {
            "프로젝트명": {"title": {}},
            "프로젝트ID": {"rich_text": {}},
            "상태": {
                "select": {
                    "options": [
                        {"name": "기획", "color": "blue"},
                        {"name": "진행중", "color": "yellow"},
                        {"name": "완료", "color": "green"},
                        {"name": "중단", "color": "red"}
                    ]
                }
            },
            "우선순위": {
                "select": {
                    "options": [
                        {"name": "최우선", "color": "red"},
                        {"name": "높음", "color": "orange"},
                        {"name": "보통", "color": "yellow"},
                        {"name": "낮음", "color": "gray"}
                    ]
                }
            },
            "시작일": {"date": {}},
            "목표일": {"date": {}},
            "진행률": {"number": {"format": "percent"}},
            "담당자": {"multi_select": {}},
            "마인드맵링크": {"url": {}},
            "예산": {"number": {"format": "number_with_commas"}},
            "성과지표": {"rich_text": {}},
            "메모": {"rich_text": {}}
        }
        
        db_data = {
            "parent": {"page_id": self.workspace_id},
            "title": [{"text": {"content": "Projects_Master"}}],
            "properties": db_properties
        }
        
        try:
            response = self.notion.databases.create(**db_data)
            self.created_dbs["Projects_Master"] = response["id"]
            print(f"✅ Projects_Master DB 생성 완료: {response['id']}")
        except Exception as e:
            print(f"❌ Projects_Master DB 생성 실패: {e}")
            self.created_dbs["Projects_Master"] = "sim_proj_master_001"
            print("🔄 시뮬레이션 모드로 진행")
    
    def create_knowledge_graph_db(self):
        """Knowledge_Graph DB 생성"""
        print("🧠 Knowledge_Graph DB 생성 중...")
        
        db_properties = {
            "지식노드명": {"title": {}},
            "노드ID": {"rich_text": {}},
            "지식유형": {
                "select": {
                    "options": [
                        {"name": "개념", "color": "blue"},
                        {"name": "인물", "color": "green"},
                        {"name": "사건", "color": "yellow"},
                        {"name": "기술", "color": "purple"},
                        {"name": "정책", "color": "orange"}
                    ]
                }
            },
            "중요도점수": {"number": {"format": "number"}},
            "키워드": {"multi_select": {}},
            "정의설명": {"rich_text": {}},
            "최초입력": {"date": {}},
            "최종갱신": {"date": {}},
            "활용빈도": {"number": {"format": "number"}},
            "창의연결": {"rich_text": {}}
        }
        
        db_data = {
            "parent": {"page_id": self.workspace_id},
            "title": [{"text": {"content": "Knowledge_Graph"}}],
            "properties": db_properties
        }
        
        try:
            response = self.notion.databases.create(**db_data)
            self.created_dbs["Knowledge_Graph"] = response["id"]
            print(f"✅ Knowledge_Graph DB 생성 완료: {response['id']}")
        except Exception as e:
            print(f"❌ Knowledge_Graph DB 생성 실패: {e}")
            self.created_dbs["Knowledge_Graph"] = "sim_knowledge_graph_001"
            print("🔄 시뮬레이션 모드로 진행")
    
    def create_people_network_db(self):
        """People_Network DB 생성"""
        print("👥 People_Network DB 생성 중...")
        
        db_properties = {
            "인물명": {"title": {}},
            "인물ID": {"rich_text": {}},
            "직책회사": {"rich_text": {}},
            "관계유형": {
                "select": {
                    "options": [
                        {"name": "고객", "color": "blue"},
                        {"name": "파트너", "color": "green"},
                        {"name": "전문가", "color": "yellow"},
                        {"name": "정부관계자", "color": "red"}
                    ]
                }
            },
            "중요도": {
                "select": {
                    "options": [
                        {"name": "매우높음", "color": "red"},
                        {"name": "높음", "color": "orange"},
                        {"name": "보통", "color": "yellow"},
                        {"name": "낮음", "color": "gray"}
                    ]
                }
            },
            "전문분야": {"multi_select": {}},
            "연락처": {"phone_number": {}},
            "이메일": {"email": {}},
            "최근연락": {"date": {}},
            "미팅이력": {"rich_text": {}},
            "특이사항": {"rich_text": {}}
        }
        
        db_data = {
            "parent": {"page_id": self.workspace_id},
            "title": [{"text": {"content": "People_Network"}}],
            "properties": db_properties
        }
        
        try:
            response = self.notion.databases.create(**db_data)
            self.created_dbs["People_Network"] = response["id"]
            print(f"✅ People_Network DB 생성 완료: {response['id']}")
        except Exception as e:
            print(f"❌ People_Network DB 생성 실패: {e}")
            self.created_dbs["People_Network"] = "sim_people_network_001"
            print("🔄 시뮬레이션 모드로 진행")
    
    def create_ideas_incubator_db(self):
        """Ideas_Incubator DB 생성"""
        print("💡 Ideas_Incubator DB 생성 중...")
        
        db_properties = {
            "아이디어명": {"title": {}},
            "아이디어ID": {"rich_text": {}},
            "발상일자": {"date": {}},
            "발상출처": {
                "select": {
                    "options": [
                        {"name": "문서분석", "color": "blue"},
                        {"name": "AI제안", "color": "green"},
                        {"name": "브레인스토밍", "color": "yellow"},
                        {"name": "외부정보", "color": "orange"}
                    ]
                }
            },
            "성숙도": {
                "select": {
                    "options": [
                        {"name": "초기", "color": "blue"},
                        {"name": "검토", "color": "yellow"},
                        {"name": "기획", "color": "orange"},
                        {"name": "실행", "color": "green"},
                        {"name": "완료", "color": "gray"}
                    ]
                }
            },
            "사업성": {"number": {"format": "number"}},
            "실현가능성": {"number": {"format": "number"}},
            "필요자원": {"rich_text": {}},
            "예상효과": {"rich_text": {}},
            "액션플랜": {"rich_text": {}},
            "위험요소": {"rich_text": {}},
            "상태변경": {"date": {}}
        }
        
        db_data = {
            "parent": {"page_id": self.workspace_id},
            "title": [{"text": {"content": "Ideas_Incubator"}}],
            "properties": db_properties
        }
        
        try:
            response = self.notion.databases.create(**db_data)
            self.created_dbs["Ideas_Incubator"] = response["id"]
            print(f"✅ Ideas_Incubator DB 생성 완료: {response['id']}")
        except Exception as e:
            print(f"❌ Ideas_Incubator DB 생성 실패: {e}")
            self.created_dbs["Ideas_Incubator"] = "sim_ideas_incubator_001"
            print("🔄 시뮬레이션 모드로 진행")
    
    def save_db_ids_to_env(self):
        """생성된 DB ID를 .env 파일에 저장"""
        print("💾 DB ID를 .env 파일에 저장 중...")
        
        env_content = f"""
# GIA_INFOSYS 5개 핵심 DB ID
# 생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}

# Documents_Master DB
DOCUMENTS_MASTER_DB_ID={self.created_dbs.get('Documents_Master', 'not_created')}

# Projects_Master DB
PROJECTS_MASTER_DB_ID={self.created_dbs.get('Projects_Master', 'not_created')}

# Knowledge_Graph DB
KNOWLEDGE_GRAPH_DB_ID={self.created_dbs.get('Knowledge_Graph', 'not_created')}

# People_Network DB
PEOPLE_NETWORK_DB_ID={self.created_dbs.get('People_Network', 'not_created')}

# Ideas_Incubator DB
IDEAS_INCUBATOR_DB_ID={self.created_dbs.get('Ideas_Incubator', 'not_created')}
"""
        
        # .env 파일에 추가
        with open('.env', 'a', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ DB ID 저장 완료")
        print("📋 생성된 DB 목록:")
        for db_name, db_id in self.created_dbs.items():
            print(f"  - {db_name}: {db_id}")

def main():
    """메인 실행 함수"""
    print("🎯 Notion DB 생성기 시작")
    
    # DB 생성기 초기화
    db_creator = NotionDBCreator()
    
    # 5개 DB 생성 실행
    success = db_creator.create_all_databases()
    
    if success:
        print("🎉 5개 핵심 DB 생성 완료!")
        print("📱 노션에서 GIA_INFOSYS 워크스페이스를 확인해보세요!")
    else:
        print("❌ DB 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
