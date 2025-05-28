from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import json
load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class KeywordGenerator:
    def __init__(self, max_keywords=100, min_keywords=10):
        self.max_keywords = max_keywords
        self.min_keywords = min_keywords
        self.past_keyword = ""

    def generate_traffic_keywords_auto_by_openai(self) -> list:
        """
        시스템 메시지만으로 교통사고 영상 검색에 쓸 수 있는
        최대한 많은 키워드를 max_keywords 개수만큼 생성하여 리스트로 반환합니다.
        """
        # 1) 함수 스펙 정의
        functions = [
            {
                "name": "extract_keywords",
                "description": "교통사고 영상 검색에 유용한 다양한 키워드를 생성합니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "maxItems": self.max_keywords,
                            "minItems": self.min_keywords,
                            "description": "생성된 키워드 목록"
                        }
                    },
                    "required": ["keywords"]
                }
            }
        ]

        # 2) ChatCompletion 호출: system 메시지만 던져서 모델이 extract_keywords 함수를 호출하도록
        response = openai.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "system",
                    "content":
                        f"교통사고 관련 영상을 최대한 많이 검색할 수 있도 할것, "
                        f"검색 쿼리에 쓸 수 있는 키워드를 다수 생성 할것. "
                        "키워드는 중복 없이 다양하게 뽑을것, "
                        "다음의 키워드는 이미 생성되었음으로 중복되지 않을것."
                        f"{self.past_keyword}"

                }
            ],
            functions=functions,
            function_call={"name": "extract_keywords"},  # 강제 호출
            temperature=1.2,
            timeout=60
        )

        msg = response.choices[0].message.function_call.arguments
        json_args = json.loads(msg)
        print(json_args)  # 실제 값 확인
        return json_args.get("keywords", "생성 실패")

# -- 사용 예시 --
if __name__ == "__main__":
    keywords = KeywordGenerator().generate_traffic_keywords_auto_by_openai()
    print(f"\n\n생성된 키워드({len(keywords)}개):")
    for kw in keywords:
        print("-", kw)
